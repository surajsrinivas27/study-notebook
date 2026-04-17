import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

function TypingAnimation({ text }) {
  const [displayedText, setDisplayedText] = useState('')
  const [isTyping, setIsTyping] = useState(true)

  useEffect(() => {
    if (!text) return

    let currentIndex = 0
    const typingSpeed = 10 // milliseconds per character

    const typeInterval = setInterval(() => {
      if (currentIndex < text.length) {
        setDisplayedText(text.substring(0, currentIndex + 1))
        currentIndex++
      } else {
        setIsTyping(false)
        clearInterval(typeInterval)
      }
    }, typingSpeed)

    return () => clearInterval(typeInterval)
  }, [text])

  return (
    <div className="text-sm">
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
      >
        {displayedText}
      </motion.span>
      {isTyping && <span className="typing-cursor"></span>}
    </div>
  )
}

export default TypingAnimation
