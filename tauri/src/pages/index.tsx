'use client'

import { Button, Title } from "@mantine/core";
import { invoke } from '@tauri-apps/api/tauri';
import { useState } from "react";


export default function Home() {
  
  const [recording, setRecording] = useState<boolean>(false);

  const handleNew = async () => {
    await invoke('new_project', {});
  }
  const handleOpen = async () => {
    await invoke('open_project', {});
  };
  
  const handleRecord = async () => {
    setRecording(true);
    await invoke('record', {});
  };
  const handleStopRecord = async () => {
    setRecording(false);
    await invoke('stop_record', {});
  };
  
  const handlePlay = async () => {
    await invoke('play_sound', {});
  }

  return (
    <>
      <Title className='text-center pt-2'>Plaintext DAW</Title>
      <div className='py-8 text-center'>
        Let's make some music.
      </div>
      <div className='flex w-full justify-around'>
        <Button variant='outline' color='red' onClick={handleNew}>New Project</Button>
        <Button variant='outline' onClick={handleOpen}>Open Project</Button>
        {recording ? (
          <Button variant='outline' color='blue' onClick={handleStopRecord}>Stop</Button>
        ) : (
          <Button variant='outline' color='red' onClick={handleRecord}>Record</Button>
        )}
        <Button variant='outline' color='green' onClick={handlePlay}>Play sound</Button>
      </div>
    </>
  )
}
