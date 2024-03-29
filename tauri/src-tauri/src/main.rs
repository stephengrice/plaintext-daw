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

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use hound::WavWriter;
use std::thread;

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
fn open_project(handle: tauri::AppHandle, app_state: State<AppState>) {
    let app_state = app_state.0.clone();
    dialog::FileDialogBuilder::new()
        .add_filter("PTD Project (*.ptd)", &["ptd"])
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
    // Initialize the default host and get the default input device
    let host = cpal::default_host();
    
    // Get the list of available input devices
    let input_devices = host.input_devices().unwrap();
    
    println!("Available input devices:");
    for (index, device) in input_devices.enumerate() {
        println!("{}: {}", index, device.name().unwrap());
    }
    let device: cpal::Device = host.input_devices().unwrap().nth(16).unwrap();
    // let device = input_devices.nth(16).unwrap();
    // let device = host
    //     .default_input_device()
    //     .expect("Failed to get default input device");
    
    // Get the list of available output devices
    // let output_devices = host.output_devices().unwrap();

    // println!("Available output devices:");
    // for (index, device) in output_devices.enumerate() {
    //     println!("{}: {}", index, device.name().unwrap());
    // }

    // Get the format of the input device
    let stream_config = device.default_input_config().unwrap();
    let sample_rate = stream_config.sample_rate().0 * 2; // TODO figure out why it plays back at half speed??

    // Create a shared buffer to store the recorded audio samples
    let buffer = Arc::new(Mutex::new(Vec::<f32>::new()));

    // Clone the buffer for use in the audio stream callback
    let buffer_clone = buffer.clone();

    // Define the callback that will be called with recorded audio samples
    let callback = move |data: &[f32], _: &cpal::InputCallbackInfo| {
        let mut buffer = buffer_clone.lock().unwrap();
        buffer.extend_from_slice(data);
    };

    // Create an audio stream with the specified device, format, and callback
    let stream = device
        .build_input_stream(&stream_config.into(), callback, |err| eprintln!("Error: {}", err), None)
        .expect("Failed to build input stream");

    // Start the audio stream
    stream
        .play()
        .expect("Failed to start input stream");

    println!("Recording audio...");

    // Keep the main thread alive while the audio stream is active
    std::thread::sleep(std::time::Duration::from_secs(5));

    // Once recording is complete, save the recorded audio buffer to a WAV file
    println!("Recording finished, saving to WAV file...");

    let buffer = buffer.lock().unwrap();
    save_wav_file("recorded_audio.wav", &buffer, sample_rate).expect("Failed to save WAV file");
}
fn save_wav_file(filename: &str, samples: &[f32], sample_rate: u32) -> Result<(), hound::Error> {
    let spec = hound::WavSpec {
        channels: 1,
        sample_rate: sample_rate,
        bits_per_sample: 32,
        sample_format: hound::SampleFormat::Float,
    };

    let mut writer = hound::WavWriter::create(filename, spec)?;

    for &sample in samples {
        writer.write_sample(sample)?;
    }

    writer.finalize()?;
    Ok(())
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
