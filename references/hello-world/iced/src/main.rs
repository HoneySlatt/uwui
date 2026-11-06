use iced::Center;
use iced::widget::{Container, button, center, column, text};

#[derive(Default)]
struct Hello;

#[derive(Debug, Clone, Copy)]
pub enum Message {
    Clicked,
}

impl Hello {
    pub fn view(&self) -> Container<'_, Message> {
        // A column centred in the window: the text above the button
        center(
            column![
                text("Hello, World!"),
                // The button produces a `Clicked` message when pressed
                button("Let's Go!").on_press(Message::Clicked),
            ]
            .align_x(Center),
        )
    }

    pub fn update(&mut self, message: Message) {
        match message {
            Message::Clicked => {
                println!("Clicked!");
            }
        }
    }
}

fn main() -> iced::Result {
    iced::run(Hello::update, Hello::view)
}
