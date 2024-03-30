#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use crate::commands::home;
use crate::commands::project;
use crate::state::AppState;

mod state;
mod commands {
    pub mod home;
    pub mod project;
}



fn main() {
    tauri::Builder::default()
        .manage(AppState(Default::default()))
        .invoke_handler(tauri::generate_handler![
            home::new_project,
            home::open_project,
            project::get_devices, 
            project::record,
            project::stop_record, 
            project::play_sound,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
