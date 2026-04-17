# Frontend README

## Mini Notebook LLM - React Frontend

A modern, feature-rich React frontend for the Mini Notebook LLM application.

### 🎯 Features Implemented

✅ **1. Login** - Secure authentication system with demo credentials
✅ **2. Memory** - Stores all conversation messages (shows count in header)
✅ **3. Voice** - Speech-to-text input + Text-to-speech output
✅ **4. Dangerous UI** - Eye-catching pink/danger theme with animations
✅ **5. Quiz Me** - Generate quizzes by typing "quiz [topic]"
✅ **6. Smooth Typing Animation** - Character-by-character typing effect for AI responses
✅ **7. Scrollable Chat Window** - Auto-scrolling chat with full conversation history
✅ **8. Key Points** - Auto-extracts bullet points from responses
✅ **9. Explanation in Simple Language** - Backend configured for clarity

### 📦 Installation

```bash
cd frontend
npm install
```

### 🚀 Running the Application

**Terminal 1 - Start Backend:**
```bash
cd ..
python main.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### 📝 Usage

1. **Login**: Use any username/password (demo mode)
2. **Chat**: Type questions naturally
3. **Voice**: Click 🎙️ button to speak
4. **Quiz**: Type "quiz machine learning" to get questions
5. **Explain**: Type "explain AI" for simplified explanations
6. **Voice Output**: Toggle 🔊 button to hear responses read aloud

### 🎨 Dangerous UI Features

- Pink danger theme (#ff0066)
- Glowing text animations
- Smooth transitions & hover effects
- Animated background elements
- Custom scrollbar styling

### 🔧 Build for Production

```bash
npm run build
# Creates optimized build in dist/
```

### 📱 Responsive Design

- Desktop optimized
- Mobile friendly components
- Sidebar collapses on smaller screens

### 🎤 Voice Support

- Speech Recognition (input)
- Speech Synthesis (output)
- Works in Chrome, Edge, Safari

### ⚙️ Tech Stack

- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Axios
- React Router

### 🐛 Troubleshooting

**Backend connection error:**
- Ensure backend is running on http://localhost:8000
- Check CORS settings in main.py

**Voice not working:**
- Use HTTPS or localhost
- Check browser permissions

**Animations not smooth:**
- Clear browser cache
- Check GPU acceleration enabled

Enjoy your hackathon! 🚀
