# Resume Chatbot

A modern resume + AI chatbot application built with **FastAPI** backend and **Vite + Vanilla JS** frontend.

## Features

- 🎨 **Premium Dark Theme** - Glassmorphism effects, smooth animations
- 💬 **AI Chat Widget** - Interactive Q&A about the resume
- ⚡ **FastAPI Backend** - Async-native, auto-generated API docs
- 🔗 **n8n Integration** - Webhook-based AI responses
- 📱 **Responsive Design** - Works on desktop and mobile

## Project Structure

```
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI app
│   ├── config.py        # Environment configuration
│   ├── models.py        # Pydantic models
│   ├── services/
│   │   └── chat.py      # n8n webhook integration
│   └── requirements.txt
│
├── frontend/            # Vite frontend
│   ├── index.html       # Main HTML
│   ├── style.css        # Premium CSS
│   ├── main.js          # Chat widget logic
│   └── package.json
│
└── main.py              # (Legacy) Original Streamlit app
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Edit with your n8n webhook URL
uvicorn main:app --reload
```

API docs available at: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-id
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/chat` | Send chat message |

## Deployment

### Backend
Deploy to any Python hosting (Render, Railway, Fly.io):
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
Build for production:
```bash
cd frontend
npm run build
```
Deploy the `dist/` folder to any static hosting (Vercel, Netlify, Cloudflare Pages).

## License

MIT