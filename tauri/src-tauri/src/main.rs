#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use std::sync::{Arc, Mutex};
use tauri::api::dialog;
use tauri::{Manager, State};

use std::fs::File;
use std::io::BufReader;
use rodio::{Decoder, OutputStream, source::Source};

mod state;

struct AppState(Arc<Mutex<state::App>>);

fn render_song(path: String) {
    Command::new("plaintext-daw")
        .arg("render")
        .arg(path)
        .spawn()
        .expect("failed to render song");
}

#[tauri::command]
fn new_project(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("New project clicked.");
}

    #[tauri::command]
fn open_project(handle: tauri::AppHandle, app_state: State<AppState>) {
    let app_state = app_state.0.clone();
    dialog::FileDialogBuilder::new()
        .add_filter("Yaml", &["yml", "yaml"])
        .pick_file(move |file_path| {
            if let Some(path) = file_path {
                app_state.lock().unwrap().filepath = path.to_str().unwrap().to_string();
                tauri::WindowBuilder::new(
                    &handle,
                    "editor",
                    tauri::WindowUrl::App("index2.html".into()),
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
fn record(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("Started recording");
}

#[tauri::command]
fn stop_record(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("Stopped recording");
}

#[tauri::command]
fn play_sound(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("Playing sound");
    // Open the WAV file
    let file = File::open("../../python/test/data/song1/piano/Piano-C5.ogg.wav").expect("Failed to open file");
    let source = Decoder::new(BufReader::new(file)).expect("Failed to decode WAV");

    // Start the audio playback
    let (stream, stream_handle) = OutputStream::try_default().unwrap();
    stream_handle.play_raw(source.convert_samples());
    std::thread::sleep(std::time::Duration::from_secs(2));
    println!("Done sound playing handler");
}

fn main() {
    tauri::Builder::default()
        .manage(AppState(Default::default()))
        .invoke_handler(tauri::generate_handler![
            new_project,
            open_project, 
            record, 
            stop_record, 
            play_sound,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
