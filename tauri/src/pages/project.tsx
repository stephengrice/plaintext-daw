import { Button, Select, Title } from "@mantine/core";
import { invoke } from '@tauri-apps/api/tauri';
import { useEffect, useState } from "react";


export default function ProjectView() {
    const [devices, setDevices] = useState<string[]>([]);
    const [recording, setRecording] = useState<boolean>(false);

    useEffect(() => {
        invoke('get_devices', {}).then((resp) => {
            setDevices(resp as string[]);
        });
    }, []);

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
            <div>
                <Title order={2}>Devices</Title>
                <Select
                    label="Input Devices"
                    data={devices}
                />
            </div>
        </>
    )
}
