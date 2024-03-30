import Layout from '@/components/Layout'
import '@mantine/core/styles.css';
import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import { createTheme, MantineProvider } from '@mantine/core';


const theme = createTheme({
});

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </MantineProvider>
  )
}
