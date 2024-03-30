import { Button, Select, Title } from "@mantine/core";
import { invoke } from '@tauri-apps/api/tauri';
import { useEffect, useState } from "react";


export default function ProjectView() {
    const [devices, setDevices] = useState<string[]>([]);
    const [device, setDevice] = useState<string>('');
    const [recording, setRecording] = useState<boolean>(false);

    useEffect(() => {
        invoke('get_devices', {}).then((resp) => {
            const respTyped = resp as string[];
            setDevices(respTyped);
            setDevice(respTyped[0]);
        });
    }, []);

    const handleRecord = async () => {
        setRecording(true);
        await invoke('record', { deviceName: device });
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
                    value={device}
                    onChange={(value, option) => setDevice(option.value)}
                />
            </div>
        </>
    )
}
