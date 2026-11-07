#!/usr/bin/env python3
"""Measures an application from outside, without a probe in its code (SlimeEngine's ADR-0200;
docs/measurements.md, "The method checked against Slatty's probe"): it runs it in a headless sway
of its own and reads what the compositor shows and what the kernel counts.

    scripts/measure.py [options] <folder> -- <command> [<argument>...]

<command> starts the application and must become it (`exec`), so that its pid is the program's.
Its figures are printed and written, with every run's raw data, to <folder>/results.json.

- Start, `--runs` times (10) after one not counted: from the launch to the first frame of the
  application that the compositor shows, and to the first frame from which nothing changes until
  the application stays still ("still", below), each compared by its pixels' CRC-32; a start
  that is not still within `--still-limit` seconds (60) has no "still". `--no-warm-up` leaves out
  the start not counted, for a program whose tool builds it at its start, a reload's.
- Then, after one more start, the steps of `--steps <file>`, or by default: wait until still,
  3 s, the memory, 7 s, then 60 s at rest.
- `--xwayland`: once more, the program started with Xwayland's display alone, its rest for 60 s.
- `--power`: before and after, 60 s of sway alone, so that a window's GPU figures have a base.
- `--display`: on the session's own display instead of a sway of its own, the frames read on the
  output that holds the point `--at <x>,<y>` of the layout; with others' windows on that output,
  their changes count as frames too.

A step a line, `#` a comment:

    pointer <command>     scripts/wayland.py's pointer commands: move, click, wheel, scroll...;
                          a move is counted from the window's origin; a person's pointer
                          rests before it clicks, and a button shown on hover takes a click
                          only then: a `sleep` between a move and a click
    origin <command>      runs the shell command, which prints the window's box as
                          <width>x<height>+<x>+<y>, the window's origin in the layout (0, 0 at first)
    sleep <seconds>
    still [<seconds>]     waits until no frame comes for 1.5 s and the program's processes work no
                          more (at most two ticks in a second), at most <seconds> (60)
    shot <name>           an image of the output, a third of its size, <folder>/<name>.png (grim)
    memory <label>        resident (RSS, and PSS summed over the process's tree) and video memory
    measure <label> <seconds> [every <milliseconds> <pointer command>]
    save <label> <runs> <file> <text> <replacement> [--region <x>,<y>,<width>,<height>]
         [--in-place] [--then <command>] [--then-limit <seconds>] [--pause <seconds>]
         [--limit <seconds>]
                          a change saved and the first frame that shows it, below

`save` times a reload: it saves <file> with <text> replaced by <replacement>, as an editor saves,
written beside it and renamed over it, and waits for the first frame whose pixels differ from those
shown before the save, compared by their CRC-32. The time runs from just before the file changes on
disk. It saves <runs> + 1 times, the change and back in turn, the first apart (a session's first
reload, often slower), each once the program stood still, as `still` waits, at most `--limit`
seconds (60), and waits for the change at most as long.

- `--region`: only <region>'s pixels are compared, in logical pixels from the window's origin, so
  that a notice of the reload drawn elsewhere is not taken for the change; refused on `--display`.
- `--in-place`: the file written over itself instead, as some editors save, for a watcher that
  takes no file renamed.
- `--then`: a shell command run after each save, as an editor's action on save (Flutter reloads on
  a signal); failed past `--then-limit` seconds (10) or with a status not zero.
- `--pause`: that many seconds waited instead of the program standing still, for a program that
  draws or works without end.

Each run notes the first frame changed and the image the program settled on: a frame between them,
a blank one or a notice that goes, is counted apart. It notes whether the program kept its window
and its process, as sway lists them. Every save step's file and text are checked before the program
starts, and the file is saved back as it was, the way the step saved it, when the step ends or
stops. The step is parsed as a shell parses words, so that <text> may hold spaces; `#` still
begins a comment.

`measure` reads over its seconds, while the pointer command repeats if one is given: the frames
the compositor shows and the intervals between them, their median, 95th and 99th percentiles and
longest, and the refreshes missed in motion (an interval of n refreshes of 240 Hz misses n - 1;
one of 100 ms or more is counted as a pause instead; a program that draws at 60 a second by
design misses 3 a frame by this count); the processor's
ticks of each of the application's threads and its wake-ups (its context switches, voluntary and
not, as Slatty's own measure counts them); the compositor's
ticks, sway's and Xwayland's; and the GPU's load and power, which the card's driver gives
(amdgpu's `gpu_busy_percent` and `power1_average`), read ten times a second. The compositor's
ticks and the GPU's load include the copies that read the frames, which cost them most in motion
at the display's rate (docs/measurements.md, "Opium's songs, from outside").

sway's output is 3840 x 2160 at 240 Hz, scale 1.5, the window alone on it; drawn by sway's GL
renderer on the machine's GPU. The program runs without a session bus and behind a closed proxy,
its $HOME and XDG folders in <folder>/home, kept from one start to the next (a command may set
others). Run it inside the shell that
the command needs (for instance `nix develop .#hello-iced`), on a machine at rest: it refuses to
start while a game seems to run. sway, swaymsg and python3 must be on the PATH; the reference
shells and Opium's have them, else `nix shell nixpkgs#sway`.
"""

import argparse
import itertools
import json
import os
import platform
import re
import shlex
import shutil
import signal
import socket
import statistics
import struct
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WAYLAND = os.path.join(HERE, "wayland.py")
OUTPUT = "3840x2160@240Hz"
REFRESH_MS = 1000 / 240
STILL_SECONDS = 1.5
# An interval this long is a pause of the program, not a presentation missed in motion.
PAUSE_MS = 100
CLOCK_TICKS = os.sysconf("SC_CLK_TCK")
GAMES = re.compile(r"(?i)^(wine.*|.*\.exe|gamescope.*|reaper|pressure-vessel.*|steam_app_\d+)$")


def now_ns():
    return time.monotonic_ns()


def nearest_rank(values, percent):
    ordered = sorted(values)
    return ordered[max(0, -(-len(ordered) * percent // 100) - 1)]


def spread(values):
    """The median and range of a series, as the figures are written."""
    values = [value for value in values if value is not None]
    if not values:
        return None
    return {"median": statistics.median(values), "min": min(values), "max": max(values), "n": len(values)}


def games_running():
    found = []
    for entry in os.listdir("/proc"):
        if entry.isdigit():
            try:
                with open(f"/proc/{entry}/comm", encoding="utf-8") as comm:
                    name = comm.read().strip()
            except OSError:
                continue
            if GAMES.search(name):
                found.append(f"{entry} {name}")
    return found


class Session:
    """A headless sway of its own, with Xwayland, in a runtime folder of its own."""

    def __init__(self, work):
        self.runtime = os.path.join(work, "runtime")
        os.mkdir(self.runtime, 0o700)
        display_file = os.path.join(work, "display")
        config = os.path.join(work, "sway.config")
        with open(config, "w", encoding="utf-8") as file:
            file.write(f"output HEADLESS-1 mode --custom {OUTPUT} scale 1.5\ndefault_border none\n"
                       f"xwayland enable\nexec sh -c 'printf %s \"$DISPLAY\" > {display_file}'\n")
        self.version = subprocess.run(["sway", "--version"], capture_output=True, text=True, check=False).stdout.strip()
        environment = {key: value for key, value in os.environ.items()
                       if key not in ("WAYLAND_DISPLAY", "DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "SWAYSOCK")}
        environment.update(XDG_RUNTIME_DIR=self.runtime, WLR_BACKENDS="headless", WLR_RENDERER="gles2",
                           WLR_LIBINPUT_NO_DEVICES="1")
        self.log = open(os.path.join(work, "sway.log"), "w", encoding="utf-8")
        # A process group of its own: nixpkgs' sway runs under dbus-run-session, which must stop too.
        self.process = subprocess.Popen(["sway", "-c", config], env=environment, stdin=subprocess.DEVNULL,
                                        stdout=self.log, stderr=subprocess.STDOUT, process_group=0)
        deadline = time.monotonic() + 20
        self.wayland = self.x11 = None
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                sys.exit(f"sway stopped: see {self.log.name}")
            sockets = [name for name in os.listdir(self.runtime)
                       if name.startswith("wayland-") and not name.endswith(".lock")]
            if sockets and os.path.exists(display_file) and os.path.getsize(display_file):
                self.wayland = sockets[0]
                with open(display_file, encoding="utf-8") as file:
                    self.x11 = file.read()
                if self.refresh() == 240000:
                    break
            time.sleep(0.1)
        else:
            sys.exit(f"sway did not start at 240 Hz within 20 s: see {self.log.name}")

    def ipc(self, *arguments):
        sockets = [name for name in os.listdir(self.runtime) if name.startswith("sway-ipc.")]
        if not sockets:
            return None
        result = subprocess.run(["swaymsg", "-s", os.path.join(self.runtime, sockets[0]), "-r", *arguments],
                                capture_output=True, text=True, check=False)
        return json.loads(result.stdout) if result.returncode == 0 else None

    def refresh(self):
        outputs = self.ipc("-t", "get_outputs")
        return outputs[0]["current_mode"]["refresh"] if outputs else None

    def client_environment(self):
        return {"XDG_RUNTIME_DIR": self.runtime, "WAYLAND_DISPLAY": self.wayland}

    def compositor_pids(self):
        return compositor_pids(self.runtime, self.wayland)

    def stop(self):
        try:
            os.killpg(self.process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        self.process.wait()


def compositor_pids(runtime, wayland):
    """The compositor that serves the Wayland socket, as the socket's peer tells, and its Xwayland."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.connect(os.path.join(runtime, wayland))
        server = struct.unpack("3i", connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))[0]
    pids = [server]
    for member in process_tree(server)[1:]:
        try:
            with open(f"/proc/{member}/comm", encoding="utf-8") as file:
                if file.read().strip() == "Xwayland":
                    pids.append(member)
        except OSError:
            continue
    return pids


class Display:
    """The session's own display, for a measure on the owner's screen: nothing is started."""

    def __init__(self):
        self.runtime = os.environ["XDG_RUNTIME_DIR"]
        self.wayland = os.environ.get("WAYLAND_DISPLAY", "wayland-0")
        self.x11 = os.environ.get("DISPLAY", "")
        self.version = "the session's compositor"

    def client_environment(self):
        return {"XDG_RUNTIME_DIR": self.runtime, "WAYLAND_DISPLAY": self.wayland}

    def compositor_pids(self):
        return compositor_pids(self.runtime, self.wayland)

    def stop(self):
        pass


class Helper:
    """scripts/wayland.py, run in the session."""

    def __init__(self, session, *arguments):
        environment = {**os.environ, **session.client_environment()}
        self.process = subprocess.Popen([sys.executable, "-I", WAYLAND, *arguments], env=environment,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)


class Frames(Helper):
    """The frames that the compositor shows, read in a thread: (time in ns, CRC-32 or None). With
    `pixels`, a CRC of `region` (the output's logical pixels, "<x>,<y>,<width>,<height>"), the whole
    output by default; without, a copy of one pixel, which only tells that a frame came."""

    def __init__(self, session, pixels, region=None):
        arguments = ["frames"] + (["--pixels"] + (["--region", region] if region else []) if pixels
                                  else ["--region", "0,0,1,1"])
        if getattr(session, "at", None):
            arguments += ["--at", session.at]
        super().__init__(session, *arguments)
        if self.process.stdout.readline().strip() != "ready":
            sys.exit("scripts/wayland.py frames did not start")
        self.frames = []
        self.thread = threading.Thread(target=self.read, daemon=True)
        self.thread.start()

    def read(self):
        for line in self.process.stdout:
            stamp, crc = line.split()
            self.frames.append((int(stamp), None if crc == "-" else crc))

    def wait_first(self):
        deadline = time.monotonic() + 10
        while not self.frames and time.monotonic() < deadline:
            time.sleep(0.01)
        if not self.frames:
            sys.exit("the compositor sent no first frame")

    def wait_still(self, pids, limit=60):
        """Waits until no frame came for STILL_SECONDS and the program's tree used at most two
        processor ticks in the last second; False if `limit` seconds passed first."""
        deadline = time.monotonic() + limit
        history = []
        previous, worked = {}, 0
        while time.monotonic() < deadline:
            current = threads(pids())
            worked += ticks_since(previous, current)
            previous = current
            history = [(moment, count) for moment, count in history if moment > time.monotonic() - 1.05]
            history.append((time.monotonic(), worked))
            quiet = history[0][0] <= time.monotonic() - 0.95 and worked - history[0][1] <= 2
            last = self.frames[-1][0] if self.frames else 0
            if quiet and (now_ns() - last) / 1e9 >= STILL_SECONDS:
                return True
            time.sleep(0.05)
        return False

    def stop(self):
        self.process.send_signal(signal.SIGTERM)
        self.process.wait()
        self.thread.join()


class Pointer(Helper):
    def __init__(self, session):
        super().__init__(session, "pointer")

    def send(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        if self.process.stdout.readline().strip() != "ok":
            sys.exit(f"the pointer did not take: {command}")

    def stop(self):
        self.process.stdin.close()
        self.process.wait()


def process_tree(pid):
    """The process and its descendants, now."""
    parents = {}
    for entry in os.listdir("/proc"):
        if entry.isdigit():
            try:
                with open(f"/proc/{entry}/stat", encoding="utf-8") as file:
                    parents.setdefault(int(file.read().rsplit(")", 1)[1].split()[1]), []).append(int(entry))
            except OSError:
                continue
    tree, queue = [], [pid]
    while queue:
        current = queue.pop()
        tree.append(current)
        queue.extend(parents.get(current, []))
    return tree


def kilobytes(text, name):
    match = re.search(rf"^{name}:[ \t]+(\d+)[ \t]*(\w*)", text, re.MULTILINE)
    if not match:
        return None
    factor = {"": 1 / 1024, "kB": 1, "KiB": 1, "MiB": 1024, "GiB": 1024 * 1024}[match.group(2)]
    return int(match.group(1)) * factor


def memory(pid):
    """RSS of the program, PSS and RSS summed over its tree, and the video memory its GPU clients
    asked for (drm-memory-vram, else drm-total-vram), each client of a device once; in MB."""
    rss_program = rss_tree = pss_tree = 0
    clients = {}
    for member in process_tree(pid):
        try:
            with open(f"/proc/{member}/status", encoding="utf-8") as file:
                rss = kilobytes(file.read(), "VmRSS") or 0
            with open(f"/proc/{member}/smaps_rollup", encoding="utf-8") as file:
                pss = kilobytes(file.read(), "Pss") or 0
            descriptors = os.listdir(f"/proc/{member}/fd")
        except OSError:
            continue
        rss_program += rss if member == pid else 0
        rss_tree += rss
        pss_tree += pss
        for descriptor in descriptors:
            try:
                if not os.readlink(f"/proc/{member}/fd/{descriptor}").startswith("/dev/dri"):
                    continue
                with open(f"/proc/{member}/fdinfo/{descriptor}", encoding="utf-8") as file:
                    info = file.read()
            except OSError:
                continue
            client = re.search(r"^drm-client-id:\s+(\d+)", info, re.MULTILINE)
            device = re.search(r"^drm-pdev:\s+(\S+)", info, re.MULTILINE)
            video = kilobytes(info, "drm-memory-vram")
            video = kilobytes(info, "drm-total-vram") if video is None else video
            if client and video is not None:
                clients[(device.group(1) if device else "", client.group(1))] = video
    megabytes = 1024 / 1e6
    return {"rss_program_mb": round(rss_program * megabytes, 1), "rss_tree_mb": round(rss_tree * megabytes, 1),
            "pss_tree_mb": round(pss_tree * megabytes, 1),
            "video_mb": round(sum(clients.values()) * megabytes, 1) if clients else None,
            "processes": len(process_tree(pid))}


def threads(pids):
    """Each thread's processor ticks, context switches and name, by (pid, tid)."""
    counts = {}
    for pid in pids:
        try:
            tids = os.listdir(f"/proc/{pid}/task")
        except OSError:
            continue
        for tid in tids:
            try:
                with open(f"/proc/{pid}/task/{tid}/stat", encoding="utf-8") as file:
                    head, tail = file.read().rsplit(")", 1)
                with open(f"/proc/{pid}/task/{tid}/status", encoding="utf-8") as file:
                    status = file.read()
            except OSError:
                continue
            fields = tail.split()
            switches = sum(int(re.search(rf"^{kind}_ctxt_switches:\s+(\d+)", status, re.MULTILINE).group(1))
                           for kind in ("voluntary", "nonvoluntary"))
            counts[(pid, int(tid))] = (head.split("(", 1)[1], int(fields[11]) + int(fields[12]), switches)
    return counts


def ticks_since(before, after):
    """The processor ticks worked between two readings of threads(): each thread's growth, a new
    thread's whole count. A thread that ended takes its ticks with it, so the totals of the two
    readings cannot be subtracted: a program that ends a busy thread would seem to work less than
    nothing. A thread whose count fell is another that took its number: new."""
    worked = 0
    for key, (_, ticks, _) in after.items():
        earlier = before.get(key, (None, 0, 0))[1]
        worked += ticks - earlier if ticks >= earlier else ticks
    return worked


class Gpu:
    """The first card that reports its load, read ten times a second while a window lasts."""

    def __init__(self):
        self.device = next((f"/sys/class/drm/{card}/device" for card in sorted(os.listdir("/sys/class/drm"))
                            if os.path.exists(f"/sys/class/drm/{card}/device/gpu_busy_percent")), None)
        hwmon = f"{self.device}/hwmon" if self.device else None
        self.power = None
        if hwmon and os.path.isdir(hwmon):
            for name in os.listdir(hwmon):
                for sensor in ("power1_average", "power1_input"):
                    if os.path.exists(f"{hwmon}/{name}/{sensor}"):
                        self.power = self.power or f"{hwmon}/{name}/{sensor}"

    def sample(self, stop, samples):
        while not stop.wait(0.1):
            try:
                with open(f"{self.device}/gpu_busy_percent", encoding="utf-8") as file:
                    busy = int(file.read())
                with open(self.power, encoding="utf-8") as file:
                    watts = int(file.read()) / 1e6
            except (OSError, TypeError, ValueError):
                continue
            samples.append((busy, watts))


def frame_figures(stamps, start, end):
    """What the frames shown between two times say: rate, intervals, refreshes missed."""
    inside = [stamp for stamp in stamps if start <= stamp <= end]
    intervals = [(later - earlier) / 1e6 for earlier, later in itertools.pairwise(inside)]
    figures = {"frames": len(inside), "rate": round(len(inside) / ((end - start) / 1e9), 1)}
    if intervals:
        figures.update({
            "p50_ms": round(nearest_rank(intervals, 50), 2), "p95_ms": round(nearest_rank(intervals, 95), 2),
            "p99_ms": round(nearest_rank(intervals, 99), 2), "max_ms": round(max(intervals), 2),
            "over_4_17": sum(interval > 4.17 for interval in intervals),
            "over_6_25": sum(interval > 6.25 for interval in intervals),
            "over_16_7": sum(interval > 16.7 for interval in intervals),
            "missed": sum(max(0, round(interval / REFRESH_MS) - 1) for interval in intervals if interval < PAUSE_MS),
            "pauses": sum(interval >= PAUSE_MS for interval in intervals),
        })
    return figures


def first_change(frames, after, baseline):
    """The first frame shown after the time `after` whose CRC is not `baseline`: (time, CRC) or None."""
    return next(((stamp, crc) for stamp, crc in frames if stamp > after and crc != baseline), None)


def replace_once(content, text, replacement):
    """`content` with its one `text` replaced; refuses a text absent or there more than once, which
    would make the step change something other than it says."""
    count = content.count(text)
    if count != 1:
        raise ValueError(f"{text!r} is in the file {count} times, not once")
    return content.replace(text, replacement)


def read_text(path):
    """The file's text as it is on disk, its line endings kept."""
    with open(path, encoding="utf-8", newline="") as file:
        return file.read()


def save_as_an_editor(path, content):
    """Writes `content` to a file beside `path`, then renames it over `path`, as editors save: the
    file is whole at every instant, and a watcher sees it created or moved, not written in parts.
    The file keeps its mode and its line endings. Returns the time, in ns, just before the rename,
    when a watcher may first see the change."""
    folder, name = os.path.split(os.path.abspath(path))
    mode = os.stat(path).st_mode & 0o7777
    descriptor, temporary = tempfile.mkstemp(prefix=f".{name}.", dir=folder)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        os.chmod(temporary, mode)
        saved = now_ns()
        os.replace(temporary, path)
        return saved
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def save_in_place(path, content):
    """Writes `content` over the file at `path`, the same file: a watcher sees its data modified.
    Returns the time, in ns, just before the write, when a watcher may first see the change."""
    with open(path, "r+", encoding="utf-8", newline="") as file:
        saved = now_ns()
        file.write(content)
        file.truncate()
        file.flush()
        os.fsync(file.fileno())
    return saved


def restore(path, original, in_place):
    """Saves the file back to `original` if it differs, the way the step saved it, so that a watcher
    that takes only one way sees it too."""
    if read_text(path) != original:
        (save_in_place if in_place else save_as_an_editor)(path, original)


def region_in_layout(region, origin):
    """A step's region, "<x>,<y>,<width>,<height>" from the window's origin, moved to the output's
    logical pixels."""
    x, y, width, height = (int(part) for part in region.split(","))
    return f"{x + origin[0]},{y + origin[1]},{width},{height}"


SAVE = argparse.ArgumentParser(prog="save", add_help=False, exit_on_error=False)
SAVE.add_argument("label")
SAVE.add_argument("runs", type=int)
SAVE.add_argument("file")
SAVE.add_argument("text")
SAVE.add_argument("replacement")
SAVE.add_argument("--region")
SAVE.add_argument("--in-place", action="store_true")
SAVE.add_argument("--then")
SAVE.add_argument("--then-limit", type=float, default=10)
SAVE.add_argument("--pause", type=float)
SAVE.add_argument("--limit", type=float, default=60)


def save_step(line):
    """The words of a `save` step, as a shell splits them, read into its arguments."""
    try:
        arguments = SAVE.parse_args(shlex.split(line)[1:])
    except (argparse.ArgumentError, ValueError) as error:
        sys.exit(f"a save step not understood: {line}: {error}")
    if arguments.region and not re.fullmatch(r"\d+,\d+,\d+,\d+", arguments.region):
        sys.exit(f"a region is <x>,<y>,<width>,<height>: {line}")
    if arguments.runs < 1 or arguments.text == arguments.replacement:
        sys.exit(f"a save step needs a run at least, and a replacement that differs: {line}")
    if (arguments.pause is not None and arguments.pause < 0) or arguments.limit <= 0:
        sys.exit(f"a pause is not negative, and a limit is positive: {line}")
    return arguments


def check_save_steps(steps):
    """Every `save` step read and its file checked before the program starts: its text there once.
    A mistake then stops the measure at once, not after the program's tool has built it."""
    for line in steps:
        if line.split()[0] == "save":
            step = save_step(line)
            try:
                replace_once(read_text(step.file), step.text, step.replacement)
            except (OSError, ValueError) as error:
                sys.exit(f"a save step cannot change its file: {line}: {error}")


def views(session):
    """The windows that sway shows, as (id, pid) pairs; None on a display that is not sway's."""
    if not hasattr(session, "ipc"):
        return None
    found, queue = [], [session.ipc("-t", "get_tree")]
    while queue:
        node = queue.pop()
        if not node:
            continue
        if node.get("pid") and node.get("type") in ("con", "floating_con"):
            found.append((node["id"], node["pid"]))
        queue.extend(node.get("nodes", []) + node.get("floating_nodes", []))
    return sorted(found)


class Run:
    """The program, started in the session with its display, and what reads it."""

    def __init__(self, session, command, folder, name, x11_only=False):
        home = os.path.join(folder, "home")
        environment = dict(os.environ)
        for key in ("WAYLAND_DISPLAY", "DISPLAY", "SWAYSOCK"):
            environment.pop(key, None)
        environment.update(HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_CACHE_HOME=f"{home}/.cache",
                           XDG_DATA_HOME=f"{home}/.local/share", XDG_STATE_HOME=f"{home}/.local/state",
                           XDG_RUNTIME_DIR=session.runtime, DISPLAY=session.x11,
                           DBUS_SESSION_BUS_ADDRESS="unix:path=/nonexistent")
        for proxy in ("HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "https_proxy", "http_proxy", "all_proxy"):
            environment[proxy] = "http://127.0.0.1:9"
        if x11_only:
            environment["XDG_SESSION_TYPE"] = "x11"
        else:
            environment.update(WAYLAND_DISPLAY=session.wayland, XDG_SESSION_TYPE="wayland")
        self.output = open(os.path.join(folder, f"{name}.log"), "w", encoding="utf-8")
        self.launched = now_ns()
        # A process group of its own, so that its helpers end with it (a renderer, a web process).
        self.process = subprocess.Popen(command, env=environment, stdin=subprocess.DEVNULL, stdout=self.output,
                                        stderr=subprocess.STDOUT, process_group=0)

    def stop(self):
        """Ends the program's process group: SIGTERM, then SIGKILL to what is left after 5 s."""
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
            self.process.wait(5)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            pass
        time.sleep(0.5)  # its helpers end a moment after it
        try:
            os.killpg(self.process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        self.process.wait()
        self.output.close()


def start_once(session, command, folder, name, still_limit):
    """One start: the first frame and the first still frame, in ms after the launch."""
    frames = Frames(session, pixels=True)
    frames.wait_first()
    time.sleep(0.2)
    background = frames.frames[-1][1]
    run = Run(session, command, folder, name)
    still = frames.wait_still(lambda: process_tree(run.process.pid), still_limit) and len(frames.frames) > 1
    run.stop()
    frames.stop()
    with open(os.path.join(folder, f"{name}-frames.txt"), "w", encoding="utf-8") as file:
        file.writelines(f"{stamp} {crc}\n" for stamp, crc in frames.frames)
    after = [(stamp, crc) for stamp, crc in frames.frames if stamp > run.launched]
    shown = [frame for frame in after if frame[1] != background]
    result = {"pid": run.process.pid, "launched_ns": run.launched, "frames": len(after), "first_ms": None,
              "still_ms": None}
    if shown:
        result["first_ms"] = round((shown[0][0] - run.launched) / 1e6, 1)
        if still:
            final = shown[-1][1]
            index = len(shown)
            while index > 0 and shown[index - 1][1] == final:
                index -= 1
            result["still_ms"] = round((shown[index][0] - run.launched) / 1e6, 1)
    return result


def window(session, gpu, frames, pids, seconds, pointer=None, repeat=None, every_ms=None):
    """What a window of `seconds` shows, while `repeat` is sent to the pointer every `every_ms`."""
    stop = threading.Event()
    samples = []
    sampler = threading.Thread(target=gpu.sample, args=(stop, samples), daemon=True)
    compositor = session.compositor_pids()
    before, compositor_before = threads(pids()), threads(compositor)
    start = now_ns()
    sampler.start()
    if repeat:
        step = every_ms * 1e6
        count = 0
        while now_ns() - start < seconds * 1e9:
            pointer.send(repeat)
            count += 1
            delay = (start + count * step - now_ns()) / 1e9
            if delay > 0:
                time.sleep(delay)
    else:
        time.sleep(seconds)
    end = now_ns()
    after, compositor_after = threads(pids()), threads(compositor)
    stop.set()
    sampler.join()
    elapsed = (end - start) / 1e9
    by_name, wakes_by_name = {}, {}
    for key, (name, ticks, switches) in after.items():
        by_name[name] = by_name.get(name, 0) + ticks - before.get(key, (name, 0, 0))[1]
        wakes_by_name[name] = wakes_by_name.get(name, 0) + switches - before.get(key, (name, 0, 0))[2]
    ticks = sum(value[1] - before.get(key, (0, 0, 0))[1] for key, value in after.items())
    switches = sum(value[2] - before.get(key, (0, 0, 0))[2] for key, value in after.items())
    compositor_ticks = sum(value[1] - compositor_before.get(key, (0, 0, 0))[1]
                           for key, value in compositor_after.items())

    def core(count):
        return round(100 * count / CLOCK_TICKS / elapsed, 1)

    figures = frame_figures([stamp for stamp, _ in frames.frames], start, end)
    figures.update({
        "start_ns": start, "end_ns": end, "seconds": round(elapsed, 2), "cpu_ticks": ticks, "cpu_core_percent": core(ticks),
        "wake_ups": switches, "wake_ups_per_second": round(switches / elapsed, 1),
        "threads_core_percent": {name: core(count) for name, count in
                                 sorted(by_name.items(), key=lambda item: -item[1]) if count > 0},
        "threads_wake_ups": {name: count for name, count in
                             sorted(wakes_by_name.items(), key=lambda item: -item[1]) if count > 0},
        "compositor_core_percent": core(compositor_ticks),
    })
    if repeat:
        figures["inputs"] = f"{repeat}, every {every_ms} ms"
    if samples:
        figures["gpu_busy_percent"] = round(statistics.mean(busy for busy, _ in samples), 1)
        figures["gpu_watts"] = round(statistics.mean(watts for _, watts in samples), 1)
    return figures


class Program:
    """The program started once more for its steps, with the frames and the pointer held."""

    def __init__(self, session, command, folder, name, gpu, x11_only=False):
        self.session, self.gpu, self.folder, self.name = session, gpu, folder, name
        self.frames = Frames(session, pixels=False)
        self.frames.wait_first()
        self.pointer = Pointer(session)
        self.run = Run(session, command, folder, name, x11_only)
        self.results = {"pid": self.run.process.pid, "launched_ns": self.run.launched}
        self.origin = (0, 0)

    def pids(self):
        return process_tree(self.run.process.pid)

    def measure(self, label, seconds, repeat=None, every_ms=None):
        self.results[label] = window(self.session, self.gpu, self.frames, self.pids, seconds,
                                     self.pointer, repeat, every_ms)
        print(f"  {label}: {summary(self.results[label])}", flush=True)

    def step(self, line):
        words = line.split()
        if words[0] == "pointer":
            if words[1] == "move":
                words[2:4] = [str(float(words[2]) + self.origin[0]), str(float(words[3]) + self.origin[1])]
            self.pointer.send(" ".join(words[1:]))
        elif words[0] == "origin":
            text = subprocess.run(" ".join(words[1:]), shell=True, capture_output=True, text=True, check=False).stdout
            box = re.search(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)", text)
            if not box:
                sys.exit(f"no <width>x<height>+<x>+<y> in what this printed: {line}")
            self.origin = (int(box.group(3)), int(box.group(4)))
            self.results["window"] = box.group(0)
            print(f"  window: {box.group(0)}", flush=True)
        elif words[0] == "shot":
            environment = {**os.environ, **self.session.client_environment()}
            subprocess.run(["grim", "-s", "0.33", os.path.join(self.folder, f"{words[1]}.png")], env=environment,
                           check=True)
        elif words[0] == "sleep":
            time.sleep(float(words[1]))
        elif words[0] == "still":
            limit = float(words[1]) if len(words) > 1 else 60
            if not self.frames.wait_still(self.pids, limit):
                print(f"  still: never, within {limit:g} s", flush=True)
        elif words[0] == "save":
            self.save(save_step(line))
        elif words[0] == "memory":
            self.results[f"memory {words[1]}"] = memory(self.run.process.pid)
            print(f"  memory {words[1]}: {self.results[f'memory {words[1]}']}", flush=True)
        elif words[0] == "measure":
            label, seconds = words[1], float(words[2])
            if len(words) > 3:
                if words[3] != "every":
                    sys.exit(f"a step not understood: {line}")
                self.measure(label, seconds, " ".join(words[5:]), float(words[4]))
            else:
                self.measure(label, seconds)
        else:
            sys.exit(f"a step not understood: {line}")
        if self.run.process.poll() is not None:
            sys.exit(f"the program ended during the steps, at: {line}")

    def save(self, step):
        """The `save` step: the change saved and back, each time to its first frame shown."""
        region = None
        if step.region:
            if isinstance(self.session, Display):
                sys.exit("a save step's region is not read on --display: the output may not start at "
                         "the layout's origin")
            region = region_in_layout(step.region, self.origin)
        original = read_text(step.file)
        changed = replace_once(original, step.text, step.replacement)
        save_file = save_in_place if step.in_place else save_as_an_editor
        frames = Frames(self.session, pixels=True, region=region)
        runs = []
        try:
            frames.wait_first()
            for number in range(step.runs + 1):
                if step.pause is not None:
                    time.sleep(step.pause)
                elif not frames.wait_still(self.pids, step.limit):
                    print(f"  {step.label} {number}: not still within {step.limit:g} s before the save", flush=True)
                time.sleep(0.2)  # the copy of the last frame, which may still be hashed
                baseline = frames.frames[-1][1]
                windows = views(self.session)
                saved = save_file(step.file, changed if number % 2 == 0 else original)
                then_failed = False
                if step.then:
                    try:
                        then_failed = subprocess.run(step.then, shell=True, check=False,
                                                     timeout=step.then_limit).returncode != 0
                    except subprocess.TimeoutExpired:
                        then_failed = True
                shown = None
                deadline = time.monotonic() + step.limit
                while shown is None and time.monotonic() < deadline:
                    time.sleep(0.005)
                    shown = first_change(list(frames.frames), saved, baseline)
                if step.pause is not None:
                    time.sleep(step.pause)
                    settled = None
                else:
                    settled = frames.wait_still(self.pids, step.limit)
                image = frames.frames[-1][1]
                run = {"saved_ns": saved, "shown_ms": round((shown[0] - saved) / 1e6, 1) if shown else None,
                       "first_image": shown[1] if shown else None, "settled": settled, "image": image,
                       "window_kept": None if windows is None else windows == views(self.session)}
                if then_failed:
                    run["then_failed"] = True
                runs.append(run)
                print(f"  {step.label} {'first' if number == 0 else number}: {run}", flush=True)
                if self.run.process.poll() is not None:
                    break
        finally:
            frames.stop()
            restore(step.file, original, step.in_place)
        counted = runs[1:]
        # A steady reload settles on two images alone, the change's and the original's, and shows its
        # change at once: its first frame changed is the image it settles on, not one between.
        self.results[step.label] = {
            "file": step.file, "text": step.text, "replacement": step.replacement, "region": region,
            "in_place": step.in_place, "then": step.then, "first_ms": runs[0]["shown_ms"] if runs else None,
            "shown_ms": spread([run["shown_ms"] for run in counted]),
            "not_shown": sum(run["shown_ms"] is None for run in counted),
            "shown_between": sum(run["first_image"] not in (None, run["image"]) for run in counted),
            "then_failed": sum(run.get("then_failed", False) for run in counted),
            "window_kept": all(run["window_kept"] is not False for run in runs),
            "images": sorted({run["image"] for run in counted}), "runs": runs}
        result = self.results[step.label]
        print(f"  {step.label}: {result['shown_ms']}, {result['not_shown']} not shown, "
              f"{result['shown_between']} first shown as another image, {len(result['images'])} images", flush=True)

    def stop(self):
        self.pointer.stop()
        self.run.stop()
        self.frames.stop()
        with open(os.path.join(self.folder, f"{self.name}-frames.txt"), "w", encoding="utf-8") as file:
            file.writelines(f"{stamp}\n" for stamp, _ in self.frames.frames)


def summary(figures):
    keys = ("frames", "rate", "p50_ms", "p95_ms", "p99_ms", "max_ms", "missed", "cpu_core_percent",
            "wake_ups_per_second", "compositor_core_percent", "gpu_busy_percent", "gpu_watts")
    text = ", ".join(f"{key} {figures[key]}" for key in keys if key in figures)
    top = list(figures.get("threads_core_percent", {}).items())[:4]
    return text + (f"; threads {top}" if top else "")


def machine():
    with open("/proc/cpuinfo", encoding="utf-8") as file:
        cpu = re.search(r"^model name\s*:\s*(.+)$", file.read(), re.MULTILINE).group(1)
    return {"cpu": cpu, "kernel": platform.release()}


def alone(session, gpu, label):
    """60 s of sway without the program: the base of the GPU's figures."""
    print(label, flush=True)
    frames = Frames(session, pixels=False)
    try:
        figures = window(session, gpu, frames, list, 60)
    finally:
        frames.stop()
    print(f"  {label}: {summary(figures)}", flush=True)
    return figures


DEFAULT_STEPS = ["still", "sleep 3", "memory still", "sleep 7", "measure rest 60"]


def main():
    parser = argparse.ArgumentParser(usage="scripts/measure.py [options] <folder> -- <command> [<argument>...]")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--steps")
    parser.add_argument("--xwayland", action="store_true")
    parser.add_argument("--power", action="store_true")
    parser.add_argument("--still-limit", type=float, default=60)
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--no-warm-up", action="store_true")
    parser.add_argument("--at")
    parser.add_argument("folder")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    arguments = parser.parse_args()
    command = arguments.command[1:] if arguments.command[:1] == ["--"] else arguments.command
    if not command:
        parser.error("no command")
    for tool in ("sway", "swaymsg"):
        if shutil.which(tool) is None:
            sys.exit(f"{tool} is missing from the PATH")
    games = games_running()
    if games:
        sys.exit(f"a game seems to run, which the GPU's figures would include: {games}")
    steps = DEFAULT_STEPS
    if arguments.steps:
        with open(arguments.steps, encoding="utf-8") as file:
            steps = [line.split("#", 1)[0].strip() for line in file]
        steps = [line for line in steps if line]
    check_save_steps(steps)
    # SIGTERM ends the measure as Ctrl-C does, through each step's cleanup: a file saved back.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit("stopped by SIGTERM"))
    os.makedirs(arguments.folder, exist_ok=True)
    folder = os.path.abspath(arguments.folder)
    results = {"command": command, "machine": machine(), "date": time.strftime("%Y-%m-%d"),
               "output": f"{OUTPUT}, scale 1.5",
               # CLOCK_REALTIME minus CLOCK_MONOTONIC, to compare with a log in the time of day.
               "realtime_minus_monotonic_ns": time.time_ns() - time.monotonic_ns()}
    gpu = Gpu()
    with tempfile.TemporaryDirectory(prefix="measure-") as work:
        session = Display() if arguments.display else Session(work)
        session.at = arguments.at
        if arguments.display:
            results["output"] = "the session's display"
        results["compositor"] = session.version
        try:
            if arguments.power:
                results["sway alone, before"] = alone(session, gpu, "sway alone, before")
            if arguments.display and arguments.runs:
                sys.exit("--display measures no start: the output's other windows change its pixels; use --runs 0")
            if not any(line.split()[0] == "origin" for line in steps) and arguments.display:
                sys.exit("--display needs an `origin` step: the window is not at the layout's origin")
            if not arguments.display and not arguments.no_warm_up:
                print("start, not counted", flush=True)
                start_once(session, command, folder, "start-0", arguments.still_limit)
            runs = []
            for number in range(1, arguments.runs + 1):
                runs.append(start_once(session, command, folder, f"start-{number}", arguments.still_limit))
                print(f"start {number}: {runs[-1]}", flush=True)
                time.sleep(1)
            results["starts"] = runs
            results["start"] = {"first_ms": spread([run["first_ms"] for run in runs]),  # empty with --runs 0
                                "still_ms": spread([run["still_ms"] for run in runs])}
            print("steps", flush=True)
            program = Program(session, command, folder, "steps", gpu)
            try:
                for line in steps:
                    program.step(line)
            finally:
                program.stop()
            results["steps"] = program.results
            if arguments.xwayland:
                print("Xwayland", flush=True)
                program = Program(session, command, folder, "xwayland", gpu, x11_only=True)
                try:
                    for line in DEFAULT_STEPS:
                        program.step(line)
                finally:
                    program.stop()
                results["xwayland"] = program.results
            if arguments.power:
                results["sway alone, after"] = alone(session, gpu, "sway alone, after")
        finally:
            session.stop()
    with open(os.path.join(folder, "results.json"), "w", encoding="utf-8") as file:
        json.dump(results, file, indent=1, ensure_ascii=False)
    print(json.dumps(results.get("start"), ensure_ascii=False))


if __name__ == "__main__":
    main()
