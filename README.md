# presentation-maker

A reusable presentation system generalized from a deck built for a panel
interview: a self-contained HTML slide deck plus a cross-device
presenter-notes and timer view, so you can screen-share your entire display
for a whole talk without ever risking notes appearing on the shared screen.

This started as a one-off job-interview deck (proprietary content, kept out
of this repo). What's being extracted and open-sourced here is just the
underlying engine — the slide runtime, the notes/timer sync server, and (in
progress) a markdown-first authoring layer on top.

## What it does

- **Deck runtime** — a single portable `deck.html` renders an ordered list
  of slides with keyboard navigation (arrows / space), per-slide time
  budgets, cycling background images (pure CSS crossfade), and
  keystroke-triggered content overlays (e.g. a map or video gallery panel
  callable from any slide).
- **Speaker view, on a second device** — a tiny local server
  (`server.py`, Python standard library only, no dependencies) serves the
  deck and exposes a small `/api/state` endpoint. A separate speaker-notes
  page polls it and stays in sync with whatever slide is on screen — notes
  live on your phone or tablet, never on the shared screen.
- **Presentation timer** — start/pause/reset from the notes page, with a
  live elapsed time and a cumulative "planned vs. actual" comparison against
  each slide's time budget.

## Status

The version validated in a real talk is a hand-rolled vanilla JS/HTML deck
and a Python dev server — proven, but deck-specific (content and structure
are hardcoded into `deck.html`). Current work is generalizing that into a
standalone tool:

- One markdown file per slide, tied together by a master `deck.md` manifest,
  instead of slide content hardcoded into the runtime.
- Speaker notes as visible `> [!note]` markdown callouts (readable in
  Obsidian/GitHub) rather than a separate notes file per slide.
- YAML frontmatter directives for per-slide settings (background, logo,
  overlays) that inherit down the deck, Marp-style.
- A small CLI (`build` / `dev`) that compiles the markdown source into the
  same portable, dependency-free `deck.html` output — no runtime toolchain
  required just to *present* a deck, only to *author* one.

Design is in progress; no CLI or compiler has shipped yet. The example/demo
deck used for documentation will be generic placeholder content, not any
real talk's material.

## License

MIT.
