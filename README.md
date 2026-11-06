<p align="center">
  <img src="logo/uwui.svg" alt="uwui's logo: a blue drop with eyes and a smile, above the name uwui" width="192">
</p>

# uwui

uwui is a UI framework in Rust, drawn by the GPU, for the desktop, Android phones and the web. It is
embedded in a host that calls it, runs without a window or a GPU when tested, looks the same on
every platform, and is read and driven by agents. It is the base of the interfaces of
[SlimeEngine](https://github.com/HoneySlatt/SlimeEngine), its editor and games, and of applications.

## State

- uwui is in development and not usable yet. Nothing is announced; the version 0.0.0 on crates.io
  only keeps its name.
- Its code still lives in SlimeEngine, in `crates/uwui` and `crates/uwui-render`. SlimeEngine's
  Stage 6d moves it here, with its history.
- Outside contributions open at uwui's 1.0. Until then, issues and pull requests from others are
  not taken.

## Where to read next

- [`docs/ROADMAP.md`](docs/ROADMAP.md): what uwui is, its quality bar, its open decisions and its
  stages.
- [`docs/PLAN.md`](docs/PLAN.md): the work in progress.
- [`docs/measurements.md`](docs/measurements.md): what the programs of uwui's pilots and their
  rivals measured, on its screens of reference.
- [`scripts/`](scripts): the tools that measure any application from outside, without a probe in
  its code; [`scripts/measure.py`](scripts/measure.py) first.
- [`docs/adr/README.md`](docs/adr/README.md): where its decisions are recorded.

## Checks

```sh
nix develop -c scripts/check.sh
```

It checks the links between the Markdown files, with lychee, the scripts' syntax, and the
arithmetic of `scripts/measure.py` by its tests.

## Licence

uwui is under the MIT licence or the Apache licence 2.0, at your choice:
[`LICENSE-MIT`](LICENSE-MIT), [`LICENSE-APACHE`](LICENSE-APACHE). Its logo is not under them: its
author keeps its rights, and [`logo/README.md`](logo/README.md) says how it may be shown.
