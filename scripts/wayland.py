#!/usr/bin/env python3
"""A small Wayland client that measures an application from outside, through its compositor:
nothing runs in the application's process. Python's standard library alone; it speaks the
protocol's wire format itself. Two commands:

    scripts/wayland.py pointer
    scripts/wayland.py frames [--at <x>,<y>] [--region <x>,<y>,<width>,<height>] [--pixels] [--seconds <s>]

`pointer` holds one virtual pointer for as long as it runs (wlr-virtual-pointer-unstable-v1) and
reads commands on its standard input, one a line, answering `ok` once each has reached the
compositor:

    move <x> <y>          the pointer to a point of the layout, in logical pixels
    click [left|right]    a press and a release
    press|release [left|right]
    wheel <notches>       the wheel turned, positive downwards
    scroll <pixels>       a scroll in logical pixels, as a touchpad gives, positive downwards
    lift                  the fingers lifted from the touchpad: the scroll ends

A compositor without a physical pointer, as a headless sway, gives its seat a pointer only while a
virtual one exists. `wlrctl`, which makes one for each command and destroys it at once, takes the
pointer away before a client has bound it, and its events reach no window: hence one pointer held.

`frames` prints, one a line, each frame of the output in which something changed
(wlr-screencopy-unstable-v1, copies with damage): the time the compositor gives it, in
nanoseconds of CLOCK_MONOTONIC, and with `--pixels` a CRC-32 of the region's pixels, else `-`. It
copies the region given, in the output's logical pixels, the whole output by default, of the output
that holds the point `--at` in the layout, the first by default; a frame is
reported when anything of the output changed, whatever the region, which only sets what is copied
and hashed. It prints `ready` first, once the compositor answers, and stops after `--seconds` or
when it is sent SIGTERM, printing what it holds. The first frame copied is the output as it stood.

Both act on $WAYLAND_DISPLAY, in $XDG_RUNTIME_DIR.
"""

import argparse
import concurrent.futures
import mmap
import os
import select
import signal
import socket
import struct
import sys
import threading
import time
import zlib

BUTTONS = {"left": 0x110, "right": 0x111}
# wl_shm's formats that the copy may be given, all four bytes a pixel.
FOUR_BYTES = {0, 1, 0x34325241, 0x34325258, 0x34324241, 0x34324258, 0x30335241, 0x30335258}


class Connection:
    """The client's side of one Wayland connection: objects are numbers, messages are words."""

    def __init__(self):
        path = os.path.join(os.environ["XDG_RUNTIME_DIR"], os.environ.get("WAYLAND_DISPLAY", "wayland-0"))
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(path)
        self.next_id = 2  # 1 is wl_display
        self.handlers = {}
        self.buffer = b""
        self.globals = {}
        self.registry = self.new_id()
        self.send(1, 1, self.uint(self.registry))  # wl_display.get_registry
        self.on(self.registry, self.registry_event)
        self.on(1, self.display_event)
        self.roundtrip()

    @staticmethod
    def uint(value):
        return struct.pack("<I", value & 0xFFFFFFFF)

    @staticmethod
    def int(value):
        return struct.pack("<i", value)

    @staticmethod
    def fixed(value):
        return struct.pack("<i", round(value * 256))

    @staticmethod
    def string(text):
        data = text.encode() + b"\0"
        return struct.pack("<I", len(data)) + data + b"\0" * (-len(data) % 4)

    def new_id(self):
        self.next_id += 1
        return self.next_id - 1

    def on(self, object_id, handler):
        self.handlers[object_id] = handler

    def send(self, object_id, opcode, *arguments, fd=None):
        body = b"".join(arguments)
        message = struct.pack("<II", object_id, (8 + len(body)) << 16 | opcode) + body
        if fd is None:
            self.socket.sendall(message)
        else:
            self.socket.sendmsg([message], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack("<i", fd))])

    def bind(self, interface, version, index=0):
        if interface not in self.globals:
            sys.exit(f"the compositor has no {interface}")
        name, available = self.globals[interface][index]
        object_id = self.new_id()
        self.send(self.registry, 0, self.uint(name), self.string(interface),
                  self.uint(min(version, available)), self.uint(object_id))
        return object_id

    def registry_event(self, opcode, data):
        if opcode == 0:  # global
            name, length = struct.unpack_from("<II", data)
            interface = data[8:8 + length - 1].decode()
            version = struct.unpack_from("<I", data, 8 + length + (-length % 4))[0]
            self.globals.setdefault(interface, []).append((name, version))

    def display_event(self, opcode, data):
        if opcode == 0:  # error
            object_id, code, length = struct.unpack_from("<III", data)
            sys.exit(f"Wayland error {code} on object {object_id}: {data[12:12 + length - 1].decode()}")

    def dispatch(self, timeout=None):
        """Reads what the compositor sent, waiting at most `timeout` seconds, and handles it."""
        ready, _, _ = select.select([self.socket], [], [], timeout)
        if not ready:
            return False
        data = self.socket.recv(65536)
        if not data:
            sys.exit("the compositor closed the connection")
        self.buffer += data
        while len(self.buffer) >= 8:
            object_id, word = struct.unpack_from("<II", self.buffer)
            size = word >> 16
            if len(self.buffer) < size:
                break
            body, self.buffer = self.buffer[8:size], self.buffer[size:]
            handler = self.handlers.get(object_id)
            if handler is not None:
                handler(word & 0xFFFF, body)
        return True

    def roundtrip(self):
        callback = self.new_id()
        done = []
        self.on(callback, lambda opcode, data: done.append(True))
        self.send(1, 0, self.uint(callback))  # wl_display.sync
        while not done:
            self.dispatch()
        del self.handlers[callback]


def outputs(connection):
    """Every output: its wl_output and its place in the layout, in logical pixels (xdg-output)."""
    manager = connection.bind("zxdg_output_manager_v1", 2)
    found = []
    for index in range(len(connection.globals.get("wl_output", []))):
        output = {"id": connection.bind("wl_output", 1, index)}
        xdg_output = connection.new_id()
        connection.send(manager, 1, connection.uint(xdg_output), connection.uint(output["id"]))

        def xdg_output_event(opcode, data, output=output):
            if opcode == 0:  # logical_position
                output["x"], output["y"] = struct.unpack_from("<ii", data)
            elif opcode == 1:  # logical_size
                output["width"], output["height"] = struct.unpack_from("<ii", data)

        connection.on(xdg_output, xdg_output_event)
        found.append(output)
    connection.roundtrip()
    return found


def pointer(connection):
    manager = connection.bind("zwlr_virtual_pointer_manager_v1", 1)
    device = connection.new_id()
    connection.send(manager, 0, connection.uint(0), connection.uint(device))  # the seat's default
    # Absolute positions are fractions of the layout, every output's box.
    layout = outputs(connection)
    left, top = min(output["x"] for output in layout), min(output["y"] for output in layout)
    width = max(output["x"] + output["width"] for output in layout) - left
    height = max(output["y"] + output["height"] for output in layout) - top

    def now():
        return time.monotonic_ns() // 1_000_000 & 0xFFFFFFFF

    def button(name, state):
        connection.send(device, 2, connection.uint(now()), connection.uint(BUTTONS[name]), connection.uint(state))
        connection.send(device, 4)

    for line in sys.stdin:
        words = line.split()
        if not words:
            continue
        command = words[0]
        if command == "move":
            x, y = float(words[1]), float(words[2])
            connection.send(device, 1, connection.uint(now()), connection.uint(round(x - left)),
                            connection.uint(round(y - top)), connection.uint(width), connection.uint(height))
            connection.send(device, 4)
        elif command == "click":
            button(words[1] if len(words) > 1 else "left", 1)
            button(words[1] if len(words) > 1 else "left", 0)
        elif command in ("press", "release"):
            button(words[1] if len(words) > 1 else "left", 1 if command == "press" else 0)
        elif command == "wheel":
            notches = int(words[1])
            connection.send(device, 5, connection.uint(0))  # axis_source: wheel
            connection.send(device, 7, connection.uint(now()), connection.uint(0),
                            connection.fixed(15.0 * notches), connection.int(notches))
            connection.send(device, 4)
        elif command == "scroll":
            connection.send(device, 5, connection.uint(1))  # axis_source: finger
            connection.send(device, 3, connection.uint(now()), connection.uint(0), connection.fixed(float(words[1])))
            connection.send(device, 4)
        elif command == "lift":
            connection.send(device, 6, connection.uint(now()), connection.uint(0))  # axis_stop
            connection.send(device, 4)
        else:
            sys.exit(f"unknown command: {line.strip()}")
        connection.roundtrip()
        print("ok", flush=True)
    connection.send(device, 8)
    connection.roundtrip()


def frames(connection, region, pixels, seconds, at):
    manager = connection.bind("zwlr_screencopy_manager_v1", 3)
    layout = outputs(connection)
    output = next((output["id"] for output in layout if at is None or (
        output["x"] <= at[0] < output["x"] + output["width"] and output["y"] <= at[1] < output["y"] + output["height"])),
        None)
    if output is None:
        sys.exit(f"no output holds the point {at}")
    shm = connection.bind("wl_shm", 1)
    connection.roundtrip()
    hashes = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    lines = []
    printer_lock = threading.Lock()
    state = {"buffer": None, "size": None, "memory": None, "info": None, "done": False}
    deadline = None if seconds is None else time.monotonic() + seconds

    def emit(text):
        with printer_lock:
            sys.stdout.write(text + "\n")
            sys.stdout.flush()

    def make_buffer(format_, width, height, stride):
        if state["size"] == (format_, width, height, stride):
            return
        if format_ not in FOUR_BYTES:
            sys.exit(f"the compositor offers no copy in four bytes a pixel (format {format_:#x})")
        fd = os.memfd_create("wayland-frames")
        os.ftruncate(fd, stride * height)
        pool = connection.new_id()
        connection.send(shm, 0, connection.uint(pool), connection.int(stride * height), fd=fd)
        buffer = connection.new_id()
        connection.send(pool, 0, connection.uint(buffer), connection.int(0), connection.int(width),
                        connection.int(height), connection.int(stride), connection.uint(format_))
        connection.send(pool, 1)  # destroy: the buffer keeps the memory
        state["memory"] = mmap.mmap(fd, stride * height, prot=mmap.PROT_READ)
        os.close(fd)
        state["buffer"], state["size"] = buffer, (format_, width, height, stride)

    def capture():
        frame = connection.new_id()
        x, y, width, height = region if region else (0, 0, 0, 0)
        if region:
            connection.send(manager, 1, connection.uint(frame), connection.int(0), connection.uint(output),
                            connection.int(x), connection.int(y), connection.int(width), connection.int(height))
        else:
            connection.send(manager, 0, connection.uint(frame), connection.int(0), connection.uint(output))

        def frame_event(opcode, data):
            if opcode == 0:  # buffer, in shared memory
                state["info"] = struct.unpack_from("<IIII", data)
            elif opcode == 6:  # buffer_done
                make_buffer(*state["info"])
                connection.send(frame, 2, connection.uint(state["buffer"]))  # copy_with_damage
            elif opcode == 2:  # ready
                high, low, nanoseconds = struct.unpack_from("<III", data)
                stamp = ((high << 32 | low) * 1_000_000_000) + nanoseconds
                if pixels:
                    copy = state["memory"][:]
                    lines.append(hashes.submit(lambda: f"{stamp} {zlib.crc32(copy):08x}"))
                else:
                    lines.append(f"{stamp} -")
                connection.send(frame, 1)  # destroy
                del connection.handlers[frame]
                state["done"] = True
            elif opcode == 3:  # failed
                sys.exit("the compositor failed to copy a frame")

        connection.on(frame, frame_event)

    emit("ready")
    stop = threading.Event()
    for number in (signal.SIGTERM, signal.SIGINT):
        signal.signal(number, lambda *_: stop.set())
    capture()
    while not stop.is_set() and (deadline is None or time.monotonic() < deadline):
        connection.dispatch(0.05)
        if state["done"]:
            state["done"] = False
            capture()
        while lines and (isinstance(lines[0], str) or lines[0].done()):
            line = lines.pop(0)
            emit(line if isinstance(line, str) else line.result())
    for line in lines:
        emit(line if isinstance(line, str) else line.result())


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("pointer")
    frame_parser = commands.add_parser("frames")
    frame_parser.add_argument("--region", type=lambda text: tuple(int(part) for part in text.split(",")))
    frame_parser.add_argument("--pixels", action="store_true")
    frame_parser.add_argument("--seconds", type=float)
    frame_parser.add_argument("--at", type=lambda text: tuple(int(part) for part in text.split(",")))
    arguments = parser.parse_args()
    connection = Connection()
    if arguments.command == "pointer":
        pointer(connection)
    else:
        frames(connection, arguments.region, arguments.pixels, arguments.seconds, arguments.at)


if __name__ == "__main__":
    main()
