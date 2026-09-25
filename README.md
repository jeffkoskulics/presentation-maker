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

## Try it

```
git clone https://github.com/jeffkoskulics/presentation-maker.git
cd presentation-maker
python3 server.py
```

This opens a 5-slide demo deck at `http://localhost:8000/deck.html`, with
placeholder content (no real photos or media needed) that exercises every
engine feature: bullet slides, cycling backgrounds, a keystroke-triggered
overlay (press `O`), and the timer. Open
`http://<your-lan-ip>:8000/notes.html` on a phone or second tab to see the
synced speaker-notes/timer view — the printed LAN URL is in the terminal
output.

## Repo layout

- `deck.html` — the engine + a hand-authored demo `SLIDES` array. To build
  your own deck, replace the `SLIDES` (and `OVERLAYS`) arrays with your own
  content; everything else is reusable as-is.
- `notes.html` — the speaker-notes/timer view, meant to be opened on a
  second device.
- `server.py` — the dev server described above (stdlib only, no
  dependencies).
- `overlay-demo.html` — a trivial example of the self-contained HTML file an
  `OVERLAYS` entry can point at.

## Status

This is the engine extracted from a real talk's deck, generalized just
enough to be reusable: overlays are now a declarative `OVERLAYS` list
instead of hardcoded key checks, and the demo content ships with the repo
instead of the original deck's material. Structure is still hand-authored
directly in `deck.html`'s `SLIDES` array — there's no compiler yet.

Planned next, not yet built:

- One markdown file per slide, tied together by a master `deck.md` manifest,
  instead of slide content hand-authored in the runtime.
- Speaker notes as visible `> [!note]` markdown callouts (readable in
  Obsidian/GitHub) rather than a JS array or a separate notes file per slide.
- YAML frontmatter directives for per-slide settings (background, logo,
  overlays) that inherit down the deck, Marp-style.
- A small CLI (`build` / `dev`) that compiles the markdown source into the
  same portable, dependency-free `deck.html` output — no runtime toolchain
  required just to *present* a deck, only to *author* one.

## License

MIT — see [LICENSE](LICENSE).
