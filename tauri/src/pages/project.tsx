import { Button } from "@mantine/core";
import { invoke } from '@tauri-apps/api/tauri';
import { useState } from "react";


export default function ProjectView() {
    const [recording, setRecording] = useState<boolean>(false);

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
            {recording ? (
                <Button variant='outline' color='blue' onClick={handleStopRecord}>Stop</Button>
            ) : (
                <Button variant='outline' color='red' onClick={handleRecord}>Record</Button>
            )}
            <Button variant='outline' color='green' onClick={handlePlay}>Play sound</Button>
        </>
    )
}
