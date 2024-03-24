import { Button, Title } from "@mantine/core";


export default function Home() {
  return (
    <>
      <Title className='text-center pt-2'>Plaintext DAW</Title>
      <div className='py-8 text-center'>
        Let's make some music.
      </div>
      <div className='flex w-full justify-around'>
        <Button variant='outline' color='red'>New</Button>
        <Button variant='outline'>Open</Button>
      </div>
    </>
  )
}
