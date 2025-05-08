'use client'

import { useEffect } from 'react'

export default function TelegramWebApp({ onUserIdDetected }) {
  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://telegram.org/js/telegram-web-app.js'
    script.async = true

    script.onload = () => {
      const tg = window.Telegram?.WebApp
      if (tg) {
        tg.ready()
        tg.expand()
        tg.setHeaderColor('#ffffff')
        tg.setBackgroundColor('#ffffff')

        const userId = tg.initDataUnsafe?.user?.id
        if (userId) {
          onUserIdDetected(userId)
        } else {
          console.warn('User ID not found in initDataUnsafe')
          onUserIdDetected(123456789) // Degugg
        }
      } else {
        console.error('Telegram Web App SDK not loaded')
      }
    }

    document.head.appendChild(script)

    return () => {
      document.head.removeChild(script)
    }
  }, [onUserIdDetected])

  return null
}