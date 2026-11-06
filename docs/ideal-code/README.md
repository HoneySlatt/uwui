# The ideal code of each screen, in four state models

How an application's author would want to write each screen of SlimeEngine's milestone M6d.1b, in
each of the four state models that it compares, before any prototype
([ADR-0202](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md)).
Written for M6d.1b1 on 2026-11-06. Each prototype of M6d.1b2 and M6d.1b3 starts from its file here;
the lines that the prototype forces to change are counted then. Nothing here compiles: the API is
the one that an author would want, which does not exist yet. The files are valid Rust, formatted
by rustfmt: `rustfmt --edition 2024 --check docs/ideal-code/*/*.rs`, with any Rust toolchain, which
this repository's shell does not carry yet.

Update this folder only to correct a file, before the prototypes start; afterwards, the prototypes
say what changed and why.

## The four models

A *state model* is how a change of the application's state reaches its interface.

- **The control,** today's rebuild by keys (`control/`): the program keeps its state, and a
  builder runs when the revision it is given moved, a number that the program moves by hand. The
  elements that it adds are matched with those before by their keys. Actions are read from a queue
  by the ids of the elements that the builders returned. Read from SlimeEngine's editor
  (`crates/slime-editor/src/hierarchy.rs`) and uwui's README.
- **Signals** (`signals/`), as in Floem: a view's function runs once; a closure that reads a
  signal, a label's text or a state, runs again when the signal changes, and nothing else does. A
  signal set to the value it holds tells no one.
- **Views that say they changed** (`views/`), as in GPUI: a view is a value of the program's that
  renders its elements, again when it calls `notify`. A view within it renders apart: on uwui's
  tree, which keeps its layout, it needs no size of its own, unlike GPUI's `Entity::cached`, which
  needs one.
- **Messages** (`messages/`), as in Elm and Iced: input becomes messages; `update` changes the
  state; `view` describes the whole interface again after each one, and `lazy` keeps a part
  whose value did not change. Between messages, the description is kept, as Iced keeps its own, so
  that a grid that scrolls runs its closure for the cells that come alone. uwui's `lazy` compares
  its value by `PartialEq`, keeps its part in the tree, may borrow the state, and runs its closure
  again when a list within it needs rows; Iced's needs a value that it hashes and content that
  borrows nothing, so that its author clones the rows' data or shares it.

Each model renders on uwui's tree, which keeps its elements from one frame to the next, styles,
lays out and draws again only what changed, and builds only the rows of a list that show. In the
three new models, the elements that `view` or `render` describes are matched with the tree's by
their keys, as the control's are.

## The screens

The four screens of ADR-0202, with their scripted interactions as
[ADR-0202 lists them](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md#decision),
at the sizes of the [screens of reference](../ROADMAP.md#screens-of-reference):

| Screen | Its files |
|---|---|
| "Hello, World!", gpui-kit's "Basic Example" | `hello.rs`, `sheets/hello.style` |
| Slatty's library, 10,000 covers | `library.rs`, `sheets/library.style` |
| Opium's songs, 8,500 songs | `songs.rs`, `sheets/songs.style` |
| A document of 100,000 lines | `document.rs`, `sheets/document.style` |

Where the owner's programs and ADR-0202 differ, the screen follows ADR-0202, and these choices
were made:

- Slatty's grid on the desktop has no selection by the arrows; its mode for gamepads has one. The
  grid here has one.
- Opium's headers do not sort in its M3E theme, which shows the newest songs first. The headers
  here sort as Opium's other themes do: ascending, descending, then none.
- A game's page shows its key art, its title and the button back to the library; Slatty's Play
  button, cards and footer are left out. The key art fades in over 180 ms, easing out, as Slatty's;
  its page's own fade is left out.
- The wave of progress is the one in Opium's bar below the table, its phase moving 4.2 radians a
  second at each frame while a song plays. Enter plays the song selected. A song's end is left
  out: the scripted interaction plays less than a song.
- The theme changes between dark and light, colors alone.
- Covers are matched by their games, so that a cover keeps its state when the filter moves it.
  The table's rows and the document's lines are matched by their places, and the selection is a
  place: a sort selects the song that comes to it, as in gpui-kit, not the one selected before,
  as in SwiftUI.

## What the four share

So that the files differ by their model alone, they share what is not the state model's:

- One call starts the application (`uwui::run`, or `uwui::application` for messages); how is
  M6d.1d's question.
- Elements made without a style, nested as tuples: `column`, `row`, `stack`, `label`, `button`,
  `image`, `search_field`, `pressable` (a box that takes presses), `wave`; each styled by its
  classes, `class` and `class_if`, and the shared style sheet, `sheets/`, whose classes `muted`
  and `primary` the shipped theme styles. The control nests through its builders' closures, as
  today. Styles written in code are M6d.1d's question.
- A grid and a list that build only what shows, show the place selected that the program gives
  them, scroll it into sight, and step from it by the arrows, giving the place they lead to
  (`ActionKind::Step` in the control, `on_step` elsewhere), as the references' lists do.
- A root's theme by its name.
- Each frame's time, set before the frame's input is handled: an input at rest starts a frame.
  The control reads it in `advance`, signals in `frame_time`, views in `Cx::frame_time`, messages
  in `update`.
- A key art's fade written in the style sheet: `enter`, what an element shows as it appears, from
  which its transition starts. No such part of a style exists yet. The fade is the same in the
  four; only the wave tests motion that the model drives.
- The document's edit, from outside the screen, called by the bench on what it holds: the
  control's state, the signals' handle, the views' `View`, and the messages' application, which it
  sends `Message::Edit`.
- In the songs' files, their types and the helpers that sort, write a length and work out the
  wave: 62 lines, the same in the four. In the library's, 12.

Layouts written in files (M6d.1d), Rust's code reloaded and the executor (M6d.1c) are left out: the
interface is built in Rust, and no task runs.

## What runs again, as the code reads

What each interaction runs again in each model, read from the files, not measured: M6d.1b2 and
M6d.1b3 count it. "Rows" and "cells" are those that show; "whole" is the whole screen's
description, its rows and cells that show included.

| Interaction | Control | Signals | Views | Messages |
|---|---|---|---|---|
| A frame where nothing changed | `advance`, and `build`, which compares its revisions and runs no builder | nothing | nothing | nothing |
| "Hello, World!": pressed | `act` | the press's closure | the press's closure | `update`, then `view` |
| The grid scrolled | the cells' builder | the cells that come made; those that leave, disposed | the cells' processor | the grid's closure, for the cells that come |
| A character of the filter | the screen's builder and the cells' | the memo of the games shown, the grid's items and its selection; the cells that come made, those that leave disposed | `render`, whole | `update`, then `view`, whole |
| The selection moved | the screen's builder, which gives the grid its selection | the grid's selection | `render`, whole | `update`, then `view`, whole |
| A game's page opened or closed | the screen's builder | the page made or disposed | `render`, whole | `update`, then `view`, whole |
| The theme changed | `set_theme`; every element styled again | the root's theme; every element styled again | `render`, whole; every element styled again | `update`, then `view`, whole; every element styled again |
| The table scrolled | the rows' builder | the rows that come made; those that leave, disposed | the rows' processor | the list's closure, for the rows that come |
| A column sorted | the screen's builder and the rows' | the headers' texts, the memo of the order, then each row's closures | `render`, whole, but the bar | `update`, then `view`, whole |
| The selection moved in the table | the screen's builder | the list's selection | `render`, whole, but the bar | `update`, then `view`, whole |
| A song played | the screen's builder and the rows' | each row's `playing`, the bar's title and wave | `render`, whole, and the bar | `update`, then `view`, whole |
| Each frame while a song plays | the wave's builder alone | the wave's closure alone | the bar's `render` alone | `update`, then `view`: the headers and the bar; the table kept by `lazy` |
| A line of the document changed | the lines' builder | the line's label alone, or nothing if it does not show | `render`, whole | `update`, then `view`, whole |

## Lines and concepts

Counted by [`scripts/count_code.py`](../../scripts/count_code.py), after rustfmt with its defaults
and edition 2024: lines without blank lines and comments; concepts as each file's header lists
them, one bullet each. A concept is one thing to learn: a type with its methods, a trait with its
methods, a function or a family of functions that work alike, such as the handlers, or a rule that
the compiler does not check. The model's concepts are those of the state model; the shared ones,
the same in the four for one screen, are the elements and what the four share.

Lines; then the model's concepts, and the shared ones:

| Screen | Control | Signals | Views | Messages |
|---|---|---|---|---|
| "Hello, World!" | 25; 9 + 3 | 13; 3 + 3 | 16; 5 + 3 | 21; 5 + 3 |
| Slatty's library | 140; 11 + 8 | 63; 11 + 8 | 101; 8 + 8 | 98; 7 + 8 |
| Opium's songs | 203; 11 + 8 | 140; 11 + 8 | 172; 8 + 8 | 168; 11 + 8 |
| The document | 41; 6 + 4 | 28; 6 + 4 | 28; 8 + 4 | 31; 6 + 4 |

The style sheets, the same in the four: 3 lines for "Hello, World!", 21 for the library, 37 for the
songs, 6 for the document.

What the figures say:

- Signals are the shortest on every screen, tied with views on the document: no revision, no id
  kept, no `notify`, and the screen's state lives in the closures that read it.
- The control is the longest on every screen: each change moves a revision by hand, and each
  element that an action names keeps its id from the build that made it.
- Fewer lines do not mean fewer concepts. Signals teach as many as the control, 11 on the two
  larger screens: tracking, its two panics, and three kinds of handles. Views teach the fewest
  there, 8; messages 7 on the library, but 11 on the songs, where `lazy` and the frames'
  subscription come in.

## The references beside

What the references' own examples hold of the same kind of screen, read on 2026-11-06. No
reference has an example that holds a whole screen: each line names the nearest, and what it
lacks. Lines are without blank lines and comments, for the whole file, styles written in code
included; uwui's leave theirs to the style sheet.

| Screen | GPUI and gpui-kit | Iced | Floem | SwiftUI |
|---|---|---|---|---|
| "Hello, World!" | gpui-kit 0.7.3's, 30 lines, frozen in [`references/hello-world/gpui-kit`](../../references/hello-world/gpui-kit/); GPUI alone at Zed's `145bcfc`, 39 lines, frozen in [`references/hello-world/gpui`](../../references/hello-world/gpui/) | its README's, 29 lines, frozen in [`references/hello-world/iced`](../../references/hello-world/iced/) | no "Hello, World!"; `counter-simple`, 13 lines, a counter | no whole file; `Button`'s page, and Landmarks' `App`, 17 lines |
| A grid of covers | no grid; gpui-kit's `list_story.rs`, 787 lines, a list searched and moved through by the keys; GPUI's `uniform_list.rs`, 63, one column | `gallery`, 517 lines and 168 of its data: built whole at each `view`, without a filter, the keys or a theme | no grid; `virtual_list`, 24 lines, a million numbers | Landmarks' grid, 36, 27 and 58 lines over three files: its search is kept, never applied |
| A table of songs | gpui-kit's `data_table_story.rs`, 1,493 lines: sorted, selected, values moved by a timer; GPUI's `data_table.rs`, 458, without sorting or selection | `table`, 238 lines: built whole at each `view`, without sorting or selection | no table | `Table`'s page: sorting in 14 lines, selection by ids |
| A document of 100,000 lines | gpui-kit's `virtual_list_story.rs`, 255 lines; GPUI's `list_example.rs`, 159 | none; `lazy`, 201 lines, a revision kept by hand | `widget-gallery/src/lists.rs`, 96 lines, 100,001 items | none; `LazyVStack`'s page, 100 items |

Sources and versions, the frozen "Hello, World!" apart: gpui-kit 0.9.0's stories at
[`7591a35`](https://github.com/longbridge/gpui-kit/tree/7591a35eced761e3613c01e71ff04c10129dae1a/crates/story/src/stories);
GPUI's examples at Zed's
[`1253dde`](https://github.com/zed-industries/zed/tree/1253dde6ecdbbcac2639ac78411369fb640894be/crates/gpui/examples);
Iced
[0.14.0](https://github.com/iced-rs/iced/tree/0.14.0/examples); Floem `main` at
[`1351ffb`](https://github.com/lapce/floem/tree/1351ffb/examples); SwiftUI's
[documentation](https://developer.apple.com/documentation/swiftui/) and its sample
[Landmarks with Liquid Glass](https://developer.apple.com/documentation/swiftui/landmarks-building-an-app-with-liquid-glass),
for iOS and macOS 27.

What the screens' examples need an author to learn, the elements apart:

- **GPUI with gpui-kit,** a list searched and moved through: `App`; `Window`; `Context`; `Entity`
  and `cx.new`; `Render`; `IntoElement`; `notify`, and the rule that a view without it shows what
  it showed; `cx.subscribe` and the list's events; `ListState`; `ListDelegate`, its counts, its
  search and its selection; `IndexPath`; `InputState` and its events; `Theme::change`. The table
  adds `TableState`, `TableDelegate`, some 25 methods, `Column`, `ColumnSort`, `TableEvent`,
  `cx.spawn` and the background executor's timer. In GPUI alone, the keys need `actions!`,
  `KeyBinding`, `key_context`, `FocusHandle` and `on_action`; a field of text is written by hand.
- **Iced,** the gallery and the table: `Message`; `update`; `view`; `Element`; `Task`;
  `Subscription`, `window::frames` and `keyboard::listen`; `application::timed`; `Theme`;
  `Animation` and `interpolate`; `sensor`; a scrollable's `Id` and `snap_to`. Its rules: the whole
  tree is built again at each `view`; what moves needs a key; a frame's subscription stops when
  nothing moves; a key that a field took never reaches `keyboard::listen`.
- **Floem,** a list of 100,001 items: `RwSignal`; `Effect`; `Memo`; `Label::derived`;
  `dyn_view` and `dyn_container`; `VirtualStack` and `VirtualList`, their keys and their items'
  sizes; `Scope`; styles as closures; `Transition` and `Animation`. Its rules: the view's function
  runs once; a read in a closure tracks; `get_untracked` does not; and two panics, a value borrowed
  twice and a signal of a scope disposed.
- **SwiftUI,** Landmarks' grid and `Table`'s page: `View` and `body`; `@State`; `@Binding` and
  `@Bindable`; `@Observable`; `@Environment`; `LazyVGrid` and `GridItem`; `ForEach` and
  `Identifiable`; `NavigationStack`, `NavigationLink` and `navigationDestination`; `searchable`;
  `focusable` and `onKeyPress`; `withAnimation` and `transition`; `Table`, `TableColumn` and
  `KeyPathComparator`; `onChange`. Its rule: `body` runs again when a property that it read
  changes.

What the comparison says:

- uwui's files are shorter than the references' nearest examples, but they leave their styles to
  the style sheet and hold less: no network, no placeholders, no settings.
- gpui-kit holds most in its components, the list's search, selection and keys, which its
  delegates' traits teach. uwui's grid and list hold the selection and the arrows in the four
  models alike, as Floem's `VirtualList` and SwiftUI's `Table` do.
- Signals in uwui need fewer concepts than Floem's examples: `Effect`, `Scope` and
  `get_untracked` do not show in these screens.
- No reference writes a grid of 10,000 or a table of 8,500 that builds only what shows, with a
  filter, a sort and a frame's motion together; uwui's files are judged against parts of several.

## Mistakes that the compiler lets through

What each model's code here could get wrong and still compile; M6d.1b3 shows each by a small case
that renders wrong or panics:

- **A key wrong or forgotten, in the four:** a cover matched by its place, not its game: its
  state, its hover or a fade under way, passes to another game when the filter moves it. In the
  control, `children.add(place, …)`; in signals, the grid's key closure; in views and messages,
  `.key` left out.
- **Control:** a revision not moved, `select` without `self.revision += 1`; an id kept after its
  builder ran again, `ids.close` not cleared as the page closes.
- **Signals:** a signal read outside a closure that the view tracks, `label(filter.get())`; a
  signal of a view disposed read, a cover's closure that reads its page's signal; a value
  borrowed twice, `selected.update` inside a closure that `selected.with` runs.
- **Views:** a `notify` forgotten, `select` without it; the bar changed in `View::update`
  without its own `notify`.
- **Messages:** a `lazy` part whose value leaves out what it reads, the song playing: the row
  playing does not show; a subscription to frames not given up: frames at rest.

## What the prototypes must add to uwui's tree

Shared by the four, built once on M6d.1b2's branch: elements made without a style and nested as
tuples; `class_if`; a grid that builds only its cells that show; a grid and a list that show the
place selected, scroll it into sight and give `Step`; `Ui::set_theme` by a theme's name;
`Ui::request_frame`; each frame's time set before its input; `enter` in a style;
`Element::wave`; `uwui::sample`. Then each model's own: the control's `Program`; the signals'
runtime and the views that read it; the views' `Cx`, `notify` and views within views; the
messages' `update`, `view`, `lazy`, `Subscription` and `frames`.
