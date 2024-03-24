'use client'

import { Button, Title } from "@mantine/core";
import { invoke } from '@tauri-apps/api/tauri';


export default function Home() {
  
  const handleNew = () => {
    console.log('new clicked');    
  }
  const handleOpen = async () => {
    await invoke('open_project', {});
  };

  return (
    <>
      <Title className='text-center pt-2'>Plaintext DAW</Title>
      <div className='py-8 text-center'>
        Let's make some music.
      </div>
      <div className='flex w-full justify-around'>
        <Button variant='outline' color='red' onClick={() => handleNew()}>New</Button>
        <Button variant='outline' onClick={() => handleOpen()}>Open</Button>
      </div>
    </>
  )
}
