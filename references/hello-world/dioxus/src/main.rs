use dioxus::prelude::*;

fn main() {
    dioxus::launch(app);
}

fn app() -> Element {
    rsx! {
        // A column centred in the window: the text above the button
        div {
            style: "position: fixed; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px;",
            "Hello, World!"
            button { onclick: move |_| println!("Clicked!"), "Let's Go!" }
        }
    }
}
