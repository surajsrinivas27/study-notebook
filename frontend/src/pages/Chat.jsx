import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import ChatWindow from '../components/ChatWindow'
import TypingAnimation from '../components/TypingAnimation'
import { chatAPI } from '../utils/api'
import { voiceUtils } from '../utils/voice'

function Chat({ setIsAuthenticated }) {
  const navigate = useNavigate()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [voice, setVoice] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [mode, setMode] = useState('chat') // chat, quiz, explain
  const [keyPoints, setKeyPoints] = useState([])
  const [showKeyPoints, setShowKeyPoints] = useState(false)
  const recognitionRef = useRef(null)

  // Add welcome message
  useEffect(() => {
    const username = localStorage.getItem('username') || 'Learner'
    setMessages([
      {
        id: 1,
        role: 'assistant',
        content: `Welcome, ${username}! 🎓 I'm your AI learning companion. Ask me anything - I can explain concepts, generate quizzes, complete code, and much more! Try saying "voice mode" to use voice commands.`,
        timestamp: new Date(),
        keyPoints: [],
      },
    ])
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setIsAuthenticated(false)
    navigate('/login')
  }

  const extractKeyPoints = (text) => {
    // Simple extraction of bullet points or numbered items
    const lines = text.split('\n')
    const points = lines
      .filter((line) => line.match(/^[-•*\d.]/))
      .map((line) => line.replace(/^[-•*\d.]\s*/, '').trim())
      .filter((line) => line.length > 0)
    return points.slice(0, 5)
  }

  const handleVoiceInput = () => {
    if (!voiceUtils.isSupported()) {
      alert('Voice not supported in your browser')
      return
    }

    setIsListening(true)
    recognitionRef.current = voiceUtils.startListening(
      (transcript) => {
        setInput(transcript)
        setIsListening(false)
        setTimeout(() => handleSendMessage(null, transcript), 500)
      },
      (error) => {
        console.error('Voice error:', error)
        setIsListening(false)
      }
    )
  }

  const handleSendMessage = async (e, voiceText = null) => {
    if (e) e.preventDefault()

    const text = voiceText || input.trim()
    if (!text) return

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      content: text,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      let response
      let processedContent

      if (text.toLowerCase().includes('quiz')) {
        response = await chatAPI.generateQuiz(text.replace(/quiz/i, '').trim() || 'general knowledge')
        processedContent = response.response
      } else if (text.toLowerCase().includes('explain')) {
        response = await chatAPI.explain(text.replace(/explain/i, '').trim())
        processedContent = response.response
      } else if (text.toLowerCase().includes('voice mode')) {
        processedContent =
          '🎤 Voice mode activated! Click the voice button or speak after pressing it. Your voice will be converted to text automatically.'
      } else {
        response = await chatAPI.chat(text)
        processedContent = response.response
      }

      const points = extractKeyPoints(processedContent)
      if (points.length > 0) {
        setKeyPoints(points)
        setShowKeyPoints(true)
      }

      const assistantMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: processedContent,
        timestamp: new Date(),
        keyPoints: points,
      }

      setMessages((prev) => [...prev, assistantMessage])

      if (voice) {
        voiceUtils.speak(processedContent)
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: `⚠️ Error: ${error.message || 'Failed to get response'}. Make sure the backend is running on http://localhost:8000`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const toggleVoice = () => {
    if (voice) {
      voiceUtils.stopSpeaking()
    }
    setVoice(!voice)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-darkbg to-darkcard flex flex-col">
      {/* Header */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-darkcard border-b-2 border-danger p-4 shadow-lg"
      >
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-danger animate-glow">🧠 Mini Notebook</h1>
            <span className="text-gray-400 text-sm">
              {localStorage.getItem('username')} | Memory: {messages.length} messages
            </span>
          </div>
          <div className="flex gap-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleVoice}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                voice
                  ? 'bg-danger text-white'
                  : 'bg-gray-700 text-gray-200 hover:bg-gray-600'
              }`}
            >
              {voice ? '🔊 Voice ON' : '🔇 Voice OFF'}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLogout}
              className="px-4 py-2 bg-gray-700 hover:bg-red-900 text-white rounded-lg font-semibold transition-colors"
            >
              🚪 Logout
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 flex gap-4 p-4 overflow-hidden max-w-6xl mx-auto w-full">
        {/* Chat Window */}
        <div className="flex-1 flex flex-col gap-4">
          {/* Chat Messages - Scrollable */}
          <ChatWindow messages={messages} />

          {/* Key Points Panel */}
          <AnimatePresence>
            {showKeyPoints && keyPoints.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="bg-darkcard border-l-4 border-danger rounded-lg p-4 max-h-32 overflow-y-auto"
              >
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-bold text-danger">📌 Key Points</h3>
                  <button
                    onClick={() => setShowKeyPoints(false)}
                    className="text-gray-400 hover:text-danger text-xl"
                  >
                    ✕
                  </button>
                </div>
                <ul className="space-y-1">
                  {keyPoints.map((point, idx) => (
                    <li key={idx} className="text-sm text-gray-300 flex gap-2">
                      <span className="text-danger">•</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Input Area */}
          <motion.form
            onSubmit={handleSendMessage}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="flex gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={isListening ? '🎤 Listening...' : 'Ask me anything (try: explain X, quiz Y)...'}
              disabled={loading || isListening}
              className="flex-1 px-4 py-3 bg-darkcard border-2 border-gray-600 rounded-lg focus:border-danger focus:outline-none text-white placeholder-gray-400 transition-colors disabled:opacity-50"
            />

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="button"
              onClick={handleVoiceInput}
              disabled={loading}
              className="px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors disabled:opacity-50 danger-button"
            >
              {isListening ? '🎤' : '🎙️'}
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-danger hover:bg-pink-700 text-white rounded-lg font-bold transition-colors disabled:opacity-50 relative overflow-hidden danger-button"
            >
              {loading ? '⚙️ ...' : '🚀 Send'}
            </motion.button>
          </motion.form>

          {/* Loading Animation */}
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-center items-center py-4"
            >
              <span className="text-danger font-bold animate-pulse">
                🤖 AI is thinking
                <span className="inline-block ml-1">
                  <span className="animate-bounce">.</span>
                  <span className="animate-bounce" style={{ animationDelay: '0.1s' }}>
                    .
                  </span>
                  <span className="animate-bounce" style={{ animationDelay: '0.2s' }}>
                    .
                  </span>
                </span>
              </span>
            </motion.div>
          )}
        </div>

        {/* Sidebar - Features Info */}
        <motion.div
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="hidden lg:block w-64 bg-darkcard rounded-lg border-2 border-gray-700 p-4 h-fit"
        >
          <h3 className="text-danger font-bold mb-4">✨ Features</h3>
          <div className="space-y-3 text-sm">
            <div>
              <p className="font-semibold text-danger">🔐 Login</p>
              <p className="text-gray-400">Secure authentication</p>
            </div>
            <div>
              <p className="font-semibold text-danger">💾 Memory</p>
              <p className="text-gray-400">{messages.length} messages stored</p>
            </div>
            <div>
              <p className="font-semibold text-danger">🎙️ Voice</p>
              <p className="text-gray-400">Speech-to-text & TTS</p>
            </div>
            <div>
              <p className="font-semibold text-danger">⚡ Dangerous UI</p>
              <p className="text-gray-400">Eye-catching design</p>
            </div>
            <div>
              <p className="font-semibold text-danger">❓ Quiz Me</p>
              <p className="text-gray-400">Say "quiz topic"</p>
            </div>
            <div>
              <p className="font-semibold text-danger">✍️ Typing Animation</p>
              <p className="text-gray-400">Smooth responses</p>
            </div>
            <div>
              <p className="font-semibold text-danger">📜 Scrollable Chat</p>
              <p className="text-gray-400">Full conversation</p>
            </div>
            <div>
              <p className="font-semibold text-danger">📌 Key Points</p>
              <p className="text-gray-400">Auto-extracted summary</p>
            </div>
            <div>
              <p className="font-semibold text-danger">📚 Simple Language</p>
              <p className="text-gray-400">Easy to understand</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Chat
