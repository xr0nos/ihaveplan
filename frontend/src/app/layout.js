import './globals.css'
import Head from 'next/head'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Daily Planner',
  description: 'Telegram mini-app for task scheduling',
}

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      {/* <Head>
        <script src="https://telegram.org/js/telegram-web-app.js" async></script>
      </Head> */}
      <body className={inter.className}>{children}</body>
    </html>
  )
}