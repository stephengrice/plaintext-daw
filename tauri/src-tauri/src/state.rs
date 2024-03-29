use serde::Deserialize;
use serde::Serialize;
use std::sync::{Arc, Mutex};

pub struct AppState(pub Arc<Mutex<App>>);

#[derive(Clone, Default, Serialize)]
pub struct App {
    pub filepath: String,
    pub song: Song,
    pub contents: String,
}

#[derive(Clone, Default, Deserialize, Serialize)]
pub struct Song {
    pub bpm: i32,
    pub sample_rate: i32,
}
