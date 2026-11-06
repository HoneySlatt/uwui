#!/usr/bin/env python3
"""Makes the fake music library of the screen of reference "Opium's songs" (docs/ROADMAP.md):
8,500 songs of 2,900 albums by 1,150 artists, as the owner's library is sized, laid out as
<artist>/<album>/<track> <title>.opus, each album with its cover.jpg.

usage: scripts/fake-music-library.py <folder>

Every song is three minutes of silence in Opus, tagged with its title, artist, album, album artist,
track number, year and genre: the players read it as music, play it, and draw its length. The
names are made from a fixed seed, the same on every machine: long and short, accented, and one in
six in another script than Latin (Japanese, Cyrillic, Greek, Arabic, Korean), every one marked
[FAKE]. Each cover is a gradient of 600 x 600 pixels, its colours drawn from the seed.

The folder must be missing or empty; the command writes into it a file that marks it as its own
(`fake-music-library`), and refuses any other folder that holds files. It needs ffmpeg, from
`nix shell nixpkgs#ffmpeg`, and runs one ffmpeg a core at a time: about two minutes on 16 threads.
"""

import concurrent.futures
import os
import random
import subprocess
import sys
import tempfile

SONGS, ALBUMS, ARTISTS = 8_500, 2_900, 1_150
SEED = 20261106
MARK = "fake-music-library"
LAYOUT = "1"

SYLLABLES = "ka lo mi ra ven sol dor ia nu el tor fae lin os mar ze qui bel run ash".split()
ACCENTED = "é è ü ö ñ å ç ø ß".split()
OTHER_SCRIPTS = [
    "夜の", "光", "海辺", "Ночной", "город", "Θάλασσα", "φως", "ليل", "قمر", "바다", "별빛",
]
GENRES = ["Pop", "Rock", "Jazz", "Electronic", "Classical", "Hip-Hop", "Folk", "Soul", "Ambient"]


def word(rng):
    text = "".join(rng.choice(SYLLABLES) for _ in range(rng.randint(1, 3)))
    if rng.random() < 0.15:
        at = rng.randrange(len(text))
        text = text[:at] + rng.choice(ACCENTED) + text[at + 1:]
    return text.capitalize()


def name(rng, shortest, longest):
    if rng.random() < 1 / 6:
        words = [rng.choice(OTHER_SCRIPTS) for _ in range(rng.randint(1, 3))]
    else:
        words = [word(rng) for _ in range(rng.randint(shortest, longest))]
    return " ".join(words) + " [FAKE]"


def safe(text):
    return text.replace("/", "-")


def run(command):
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: scripts/fake-music-library.py <folder>")
    folder = sys.argv[1]
    os.makedirs(folder, exist_ok=True)
    mark = os.path.join(folder, MARK)
    if os.listdir(folder) and not os.path.exists(mark):
        sys.exit(f"{folder} holds files that this command did not make")
    if os.path.exists(mark):
        sys.exit(f"{folder} is already made; delete it to make it again")

    rng = random.Random(SEED)
    artists = [name(rng, 1, 3) for _ in range(ARTISTS)]
    # Every artist has an album, the rest drawn at random; every album a song, the rest likewise.
    album_artist = list(range(ARTISTS)) + [rng.randrange(ARTISTS) for _ in range(ALBUMS - ARTISTS)]
    albums = [(name(rng, 1, 5), album_artist[i], rng.randint(1965, 2026), rng.choice(GENRES))
              for i in range(ALBUMS)]
    songs_of = [1] * ALBUMS
    for _ in range(SONGS - ALBUMS):
        songs_of[rng.randrange(ALBUMS)] += 1

    covers, songs = [], []
    for index, (title, artist, year, genre) in enumerate(albums):
        path = os.path.join(folder, safe(artists[artist])[:80], f"{safe(title)[:80]} ({index})")
        os.makedirs(path, exist_ok=True)
        colours = [f"0x{rng.randrange(1 << 24):06x}" for _ in range(2)]
        covers.append((os.path.join(path, "cover.jpg"), colours))
        for track in range(1, songs_of[index] + 1):
            song = name(rng, 1, 6)
            songs.append((os.path.join(path, f"{track:02} {safe(song)[:80]}.opus"), {
                "title": song, "artist": artists[artist], "album": title,
                "album_artist": artists[artist], "track": str(track), "date": str(year),
                "genre": genre,
            }))

    with tempfile.TemporaryDirectory() as scratch:
        silence = os.path.join(scratch, "silence.opus")
        run(["ffmpeg", "-nostdin", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "180",
             "-c:a", "libopus", "-b:a", "8k", silence])
        commands = [
            ["ffmpeg", "-nostdin", "-f", "lavfi", "-i",
             f"gradients=s=600x600:c0={c0}:c1={c1}:d=1:speed=0", "-frames:v", "1", path]
            for path, (c0, c1) in covers
        ] + [
            ["ffmpeg", "-nostdin", "-i", silence, "-c", "copy", "-map_metadata", "-1",
             *[part for key, value in tags.items() for part in ("-metadata", f"{key}={value}")],
             path]
            for path, tags in songs
        ]
        with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as pool:
            for _ in pool.map(run, commands):
                pass
    with open(mark, "w", encoding="utf-8") as file:
        file.write(f"layout {LAYOUT}\n")
    print(f"{len(songs)} songs, {len(covers)} albums, {ARTISTS} artists in {folder}")


if __name__ == "__main__":
    main()
