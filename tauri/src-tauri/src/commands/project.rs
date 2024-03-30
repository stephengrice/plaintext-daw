use std::sync::{Arc, Mutex};
use tauri::State;

use std::fs::File;
use std::io::BufReader;
use rodio::{Decoder, OutputStream, source::Source};

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};


use crate::state::AppState;


#[tauri::command]
pub fn get_devices(handle: tauri::AppHandle, app_state: State<AppState>) -> Vec<String> {
    // Initialize the default host and get the default input device
    let host = cpal::default_host();

    // Get the list of available input devices
    let input_devices = host.input_devices().unwrap();
    
    let mut devices_list: Vec<String> = Vec::new();

    for (index, device) in input_devices.enumerate() {
        devices_list.push(device.name().unwrap().to_string());
    }

    devices_list
}

#[tauri::command]
pub fn record(handle: tauri::AppHandle, app_state: State<AppState>, device_name: String) {
    println!("Starting recording {}", device_name);
    // Initialize the default host and get the default input device
    let host = cpal::default_host();
    let input_devices = host.input_devices().unwrap();
    
    let mut device: Option<cpal::Device> = None;
    for (index, currentDevice) in input_devices.enumerate() {
        if currentDevice.name().unwrap().to_string() == device_name {
            device = Some(currentDevice);
            break;
        }
    }

    if let Some(device) = device {
        println!("Selected device: {:?}", device.name().unwrap().to_string());
        // let device: cpal::Device = host.input_devices().unwrap().nth(16).unwrap();
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
    } else {
        panic!("Invalid device name: {}", device_name);
    }
}
pub fn save_wav_file(filename: &str, samples: &[f32], sample_rate: u32) -> Result<(), hound::Error> {
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
pub fn stop_record(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("Stopped recording");
}

#[tauri::command]
pub fn play_sound(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("Playing sound");
    // Spawn a new thread
    std::thread::spawn(|| {
        // Open the WAV file
        let file = File::open("../../python/test/data/song1/piano/Piano-C5.ogg.wav").expect("Failed to open file");
        let source = Decoder::new(BufReader::new(file)).expect("Failed to decode WAV");
    
        // Start the audio playback
        let (stream, stream_handle) = OutputStream::try_default().unwrap();
        stream_handle.play_raw(source.convert_samples());
        std::thread::sleep(std::time::Duration::from_secs(2));
        println!("Done playing sound.");
    });
}
