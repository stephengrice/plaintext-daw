use std::process::Command;
use std::sync::{Arc, Mutex};
use tauri::api::dialog;
use tauri::{Manager, State};

use std::fs::File;
use std::io::BufReader;
use rodio::{Decoder, OutputStream, source::Source};

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use hound::WavWriter;
use std::thread;

use crate::state::AppState;


#[tauri::command]
pub fn new_project(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("New project clicked.");
    // Spawn a new thread
    std::thread::spawn(|| {
        // Code to be executed in the new thread
        let mut counter = 0;
        while counter < 2 {
            println!("Hello from the new thread! {}", counter);
            std::thread::sleep(std::time::Duration::from_secs(1));
            counter += 1;
        }
        println!("Done looping in new thread.");
    });

    let app_state = app_state.0.clone();
    dialog::FileDialogBuilder::new()
        .add_filter("PTD Project (*.ptd)", &["ptd"])
        .set_file_name("project.ptd")
        .save_file(move |file_path| {
            if let Some(path) = file_path {
                // Touch the project file
                let mut file = File::create(path.to_str().unwrap().to_string());
                // Open project window
                app_state.lock().unwrap().filepath = path.to_str().unwrap().to_string();
                tauri::WindowBuilder::new(
                    &handle,
                    "editor",
                    tauri::WindowUrl::App("/project".into()),
                )
                .title("Plaintext DAW Editor")
                .build()
                .unwrap();
                handle
                    .get_window("open-project")
                    .unwrap()
                    .close()
                    .expect("Unable to close window");
            }
    });
}

#[tauri::command]
pub fn open_project(handle: tauri::AppHandle, app_state: State<AppState>) {
    let app_state = app_state.0.clone();
    dialog::FileDialogBuilder::new()
        .add_filter("PTD Project (*.ptd)", &["ptd"])
        .pick_file(move |file_path| {
            if let Some(path) = file_path {
                app_state.lock().unwrap().filepath = path.to_str().unwrap().to_string();
                tauri::WindowBuilder::new(
                    &handle,
                    "editor",
                    tauri::WindowUrl::App("/project".into()),
                )
                .title("Plaintext DAW Editor")
                .build()
                .unwrap();
                handle
                    .get_window("open-project")
                    .unwrap()
                    .close()
                    .expect("Unable to close window");
            }
        });
}
