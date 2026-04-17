// Voice utilities for speech-to-text and text-to-speech

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
const SpeechSynthesis = window.speechSynthesis

export const voiceUtils = {
  isSupported: () => {
    return !!SpeechRecognition && !!SpeechSynthesis
  },

  startListening: (onResult, onError) => {
    if (!SpeechRecognition) {
      onError('Speech Recognition not supported')
      return
    }

    const recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'en-US'

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript
      }
      onResult(transcript)
    }

    recognition.onerror = (event) => {
      onError(event.error)
    }

    recognition.start()
    return recognition
  },

  speak: (text, onEnd) => {
    if (!SpeechSynthesis) {
      console.error('Speech Synthesis not supported')
      return
    }

    // Cancel any ongoing speech
    SpeechSynthesis.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 1.0
    utterance.pitch = 1.0
    utterance.volume = 1.0

    utterance.onend = onEnd

    SpeechSynthesis.speak(utterance)
  },

  stopSpeaking: () => {
    if (SpeechSynthesis) {
      SpeechSynthesis.cancel()
    }
  },
}

export default voiceUtils
