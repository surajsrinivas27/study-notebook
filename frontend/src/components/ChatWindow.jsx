import React, { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import TypingAnimation from './TypingAnimation'

function ChatWindow({ messages }) {
  const endRef = useRef(null)
  const scrollContainerRef = useRef(null)

  useEffect(() => {
    // Auto-scroll to bottom
    setTimeout(() => {
      endRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }, [messages])

  return (
    <div
      ref={scrollContainerRef}
      className="flex-1 bg-darkcard border-2 border-gray-700 rounded-lg p-6 overflow-y-auto space-y-4"
    >
      <AnimatePresence>
        {messages.map((message, idx) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 * idx }}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg ${
                message.role === 'user'
                  ? 'bg-danger text-white rounded-br-none'
                  : 'bg-gray-800 text-gray-100 rounded-bl-none border-l-2 border-danger'
              }`}
            >
              {message.role === 'assistant' ? (
                <TypingAnimation text={message.content} />
              ) : (
                <p className="text-sm">{message.content}</p>
              )}
              <p className="text-xs mt-2 opacity-70">
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
      <div ref={endRef} />
    </div>
  )
}

export default ChatWindow

import { AnimatePresence } from 'framer-motion'
