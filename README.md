# Study Helper AI - V1

An AI-powered study assistant app designed for engineering students and learners. Built with Flutter (frontend) and Python Flask (backend).

## 🎯 Features

- **AI-Powered Q&A**: Ask questions and get detailed explanations on various subjects
- **Study Plan Generator**: Create personalized study plans for any topic
- **Subject Topics**: Browse organized topics across different engineering subjects
- **Multi-Subject Support**: Mathematics, Physics, Chemistry, Computer Science, and Engineering subjects
- **Modern UI**: Beautiful Material Design 3 interface with dark mode support

## 🏗️ Project Structure

```
STUDY-HELPER-V1/
├── frontend/              # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/      # UI screens
│   │   ├── services/     # API services
│   │   └── providers/    # State management
│   └── pubspec.yaml
│
├── backend/              # Flask REST API
│   ├── app.py           # Main Flask application
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   └── requirements.txt
│
└── README.md
```

## 🚀 Getting Started

### Backend Setup (Flask)

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your AI API keys
```

6. Run the server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup (Flutter)

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Flutter dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
# For Android/iOS
flutter run

# For Web
flutter run -d chrome

# For Windows
flutter run -d windows
```

## 🔧 Configuration

### AI API Integration

The app supports multiple AI providers. Add your API key in `backend/.env`:

- **OpenAI GPT**: Add `OPENAI_API_KEY`
- **Google Gemini**: Add `GEMINI_API_KEY`
- **Anthropic Claude**: Add `ANTHROPIC_API_KEY`

Update `backend/services/ai_service.py` to integrate with your chosen AI provider.

## 📱 Supported Platforms

- ✅ Android
- ✅ iOS
- ✅ Web
- ✅ Windows
- ✅ macOS
- ✅ Linux

## 🛠️ Tech Stack

### Frontend
- Flutter 3.0+
- Provider (State Management)
- Material Design 3
- HTTP Client

### Backend
- Python 3.8+
- Flask 3.0
- Flask-CORS
- Python-dotenv

## 📖 API Endpoints

- `POST /api/ask` - Ask a question
- `POST /api/study-plan` - Generate study plan
- `POST /api/explain` - Explain a concept
- `GET /api/topics/<subject>` - Get topics for subject

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License

## 👨‍💻 Author

Shivam

## 🔮 Future Enhancements

- [ ] Document/PDF upload and analysis
- [ ] Practice quiz generation
- [ ] Progress tracking
- [ ] Offline mode
- [ ] Voice input support
- [ ] Code snippet execution
- [ ] Collaborative study sessions
- [ ] Flashcard generation

---

**Note**: This is V1 of the Study Helper app. AI integration requires API keys which need to be configured separately.
