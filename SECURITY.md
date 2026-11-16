# Security

## Reporting a vulnerability

Report a vulnerability privately, through GitHub's private vulnerability reporting: the
repository's **Security** tab, then **Report a vulnerability**. Do not open a public issue for it.
While uwui's code still lives in SlimeEngine, a vulnerability of uwui may be reported in either
repository.

Say what is affected, how to reproduce it, and what it lets someone do. The owner answers as soon
as they can; there is no bounty.

## What is supported

Before 1.0, fixes land on `main`; no release of uwui is made yet.

## What matters most

- Documents that uwui reads, themes, style sheets, shortcuts and dock layouts: a damaged or hostile
  one must give an error, never a crash, a hang or memory exhausted.
- The core for agents and its MCP library, through which a tool reads and drives a program: a tool
  that reaches a program without its secret, or makes it do what it did not offer.
- What a screen reader's adapter is asked: a request that does what no person could.
