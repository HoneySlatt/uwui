#!/usr/bin/env python3
"""Makes the thumbnails of a folder of images in a profile's cache, as GNOME's applications make
them, so that Nautilus and gThumb open the folder with their thumbnails ready, as a user's are
after a first visit (scripts/market.sh).

    scripts/thumbnails.py <thumbnailer> <size> <folder> <cache>

<thumbnailer> is gdk-pixbuf's `gdk-pixbuf-thumbnailer`, the one those applications call for JPEG
and PNG images; <size> one of the cache's sizes, `normal`, `large`, `x-large` or `xx-large`;
<cache> the profile's cache folder, whose `thumbnails/<size>` receives them. Each thumbnail is
named and labelled as the freedesktop.org specification asks: the MD5 of the image's URI, and the
image's URI and modification time in the PNG, which the applications check before they use it.
Those already made are left alone; an image that the thumbnailer cannot read is named, and
skipped.
"""

import concurrent.futures
import hashlib
import os
import struct
import subprocess
import sys
import tempfile
import urllib.parse
import zlib

PIXELS = {"normal": 128, "large": 256, "x-large": 512, "xx-large": 1024}


def labelled(png, uri, mtime):
    """The PNG with its text chunks Thumb::URI and Thumb::MTime, after its header."""
    chunks = b""
    for key, value in ((b"Thumb::URI", uri.encode()), (b"Thumb::MTime", str(mtime).encode()),
                       (b"Software", b"uwui scripts/thumbnails.py")):
        data = key + b"\0" + value
        chunks += struct.pack(">I", len(data)) + b"tEXt" + data + struct.pack(">I", zlib.crc32(b"tEXt" + data))
    header_end = 8 + 8 + 13 + 4  # the signature, then IHDR's length, type, data and CRC
    return png[:header_end] + chunks + png[header_end:]


def make(thumbnailer, pixels, image, target):
    """True once the image's thumbnail is made, False if it was there, None if it could not be."""
    # The URI as GLib writes it, whose MD5 names the thumbnail: only what a URI cannot hold escaped.
    uri = "file://" + urllib.parse.quote(image, safe="/!$&'()*+,;=:@~")
    name = os.path.join(target, hashlib.md5(uri.encode()).hexdigest() + ".png")
    if os.path.exists(name):
        return False
    with tempfile.NamedTemporaryFile(suffix=".png", dir=target) as made:
        result = subprocess.run([thumbnailer, "-s", str(pixels), uri, made.name],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=False)
        if result.returncode != 0:
            print(f"no thumbnail for {image}: {result.stderr.strip()}", file=sys.stderr)
            return None
        with open(made.name, "rb") as file:
            png = file.read()
    # Private to its user, as the specification asks.
    descriptor = os.open(name + ".part", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "wb") as file:
        file.write(labelled(png, uri, int(os.stat(image).st_mtime)))
    os.replace(name + ".part", name)
    return True


def main():
    if len(sys.argv) != 5 or sys.argv[2] not in PIXELS:
        sys.exit(__doc__)
    thumbnailer, size, folder, cache = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3]), sys.argv[4]
    target = os.path.join(cache, "thumbnails", size)
    os.makedirs(target, mode=0o700, exist_ok=True)
    images = sorted(os.path.join(folder, name) for name in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, name)))
    with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as pool:
        results = list(pool.map(lambda image: make(thumbnailer, PIXELS[size], image, target), images))
    print(f"{results.count(True)} thumbnails made, {results.count(False)} already there, "
          f"{results.count(None)} failed, in {target}")


if __name__ == "__main__":
    main()
