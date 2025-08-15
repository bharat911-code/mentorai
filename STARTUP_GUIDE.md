# 🚀 Yapper RAG Startup Guide

## Quick Start (Next Time You Open Cursor)

### 1. Start the Backend (Yapper RAG Server)
```bash
python yapper_server.py
```
- This starts the RAG server on port 8001
- Wait for "✅ Model and index initialized successfully!" message
- Keep this terminal running

### 2. Start the Frontend (in a new terminal)
```bash
npm run dev
```
- This starts the React frontend on port 3000
- You'll see "Local: http://localhost:3000/"

### 3. Open in Browser
Go to: `http://localhost:3000`

## 🎯 What You'll Get

- **Beautiful "Ask Naval" interface**
- **Type any question** about Naval's philosophy
- **Long, detailed responses** using Naval's actual content
- **Dark/light mode toggle** (click background)

## 🔧 Ports Used

- **Frontend**: Port 3000 (http://localhost:3000)
- **Backend**: Port 8001 (http://localhost:8001)

## 💡 Example Questions

- "Who are you?"
- "What is wealth?"
- "How to be happy?"
- "What is Naval's philosophy on success?"
- "How to build wealth?"
- "What is the meaning of life?"

## 🛠️ Troubleshooting

If ports are busy:
1. Kill processes: `taskkill /f /im python.exe` and `taskkill /f /im node.exe`
2. Restart both servers

## 📁 Key Files

- `yapper_server.py` - Backend RAG server
- `src/App.tsx` - Frontend interface
- `yapper_ravikant/` - Naval's content (259 text files)

---

**Enjoy your Naval RAG assistant! 🎉** 