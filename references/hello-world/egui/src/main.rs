use eframe::egui;

fn main() {
    let native_options = eframe::NativeOptions::default();
    eframe::run_native("My egui App", native_options, Box::new(|cc| Ok(Box::new(MyEguiApp::new(cc)))));
}

#[derive(Default)]
struct MyEguiApp {}

impl MyEguiApp {
    fn new(cc: &eframe::CreationContext<'_>) -> Self {
        // Customize egui here with cc.egui_ctx.set_fonts and cc.egui_ctx.set_global_style.
        // Restore app state using cc.storage (requires the "persistence" feature).
        // Use the cc.gl (a glow::Context) to create graphics shaders and buffers that you can use
        // for e.g. egui::PaintCallback.
        Self::default()
    }
}

impl eframe::App for MyEguiApp {
   fn ui(&mut self, ui: &mut egui::Ui, frame: &mut eframe::Frame) {
       egui::CentralPanel::default().show(ui, |ui| {
           // egui lays out in one pass and cannot centre a group vertically by itself: centre
           // each widget horizontally, and push the group down by half the space it leaves.
           let label_height = ui.text_style_height(&egui::TextStyle::Body);
           let button_height = ui
               .spacing()
               .interact_size
               .y
               .max(label_height + 2.0 * ui.spacing().button_padding.y);
           let group_height = label_height + ui.spacing().item_spacing.y + button_height;
           ui.vertical_centered(|ui| {
               ui.add_space((ui.available_height() - group_height).max(0.0) / 2.0);
               ui.label("Hello, World!");
               if ui.button("Let's Go!").clicked() {
                   println!("Clicked!");
               }
           });
       });
   }
}
