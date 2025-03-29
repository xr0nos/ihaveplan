'use client'

import { useEffect } from 'react'

export default function TelegramWebApp() {
  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://telegram.org/js/telegram-web-app.js'
    script.async = true
    script.onload = () => {
      if (window.Telegram?.WebApp) {
        const webApp = window.Telegram.WebApp
        webApp.ready()
        webApp.expand()
        webApp.setHeaderColor('#f5f7fa')
        webApp.setBackgroundColor('#f5f7fa')
      }
    }
    document.head.appendChild(script)
    
    return () => {
      document.head.removeChild(script)
    }
  }, [])

  return null
}