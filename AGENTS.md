# AGENTS.md

Rules for AI agents in this repository. Read it fully at each session's start.

## Project

uwui, a UI framework in Rust, under MIT OR Apache-2.0: [`README.md`](README.md).
AI agents do most of the work. The owner decides direction and architecture.

## Where the work is

- This repository holds no code of uwui's yet: only the tools that measure applications, in
  `scripts/`. uwui's code lives in
  [SlimeEngine](https://github.com/HoneySlatt/SlimeEngine), in `crates/uwui` and
  `crates/uwui-render`, until SlimeEngine's milestone M6d.11 moves it here.
- Work on uwui's code happens there, under SlimeEngine's `AGENTS.md` and its `docs/PLAN.md`.
- Here: uwui's direction, its quality bar, its open decisions and its stages.

## Read before working

- [`docs/PLAN.md`](docs/PLAN.md): what is being done now.
- [`docs/ROADMAP.md`](docs/ROADMAP.md): to plan, or when a task touches a budget or a stage.
- Until the move, uwui's decisions are SlimeEngine's ADRs. Do not decide again what one decided.

## One home per fact

Each fact has one home; elsewhere, link to it.

- `README.md`: what uwui is, its real state, its checks; these change.
- `docs/ROADMAP.md`: direction, the quality bar, open decisions, stages; one changes.
- `docs/PLAN.md`: the current work; it moves.
- `docs/measurements.md`: the figures of the programs and their rivals on the screens of
  reference; one is measured.
- `scripts/`: each script says at its head what it does and how to run it.
- `docs/adr/README.md`: where decisions are recorded; their place changes.
- The milestones of SlimeEngine's Stage 6d, which change both repositories: SlimeEngine's
  `docs/PLAN.md`.

## Checks

```sh
nix develop -c scripts/check.sh
```

Run it before each commit. CI runs it on each push.

## Commits

- One logical change per commit. Subject in the imperative, in English.
- Do not commit what fails the checks.
- Releases and publishing wait for the owner's go.

## Language

Everything in the repository is in English. Talk to the owner in French.
