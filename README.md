# Python ChatBot

A simple, fully functional chatbot built with Python and Flask that can be accessed from any device on your local network or deployed to the cloud.

## Features

- ✨ Clean, responsive web interface
- 💬 Real-time chat with AI-like responses
- 🌐 Accessible from any device on your local network
- ☁️ Easy deployment to cloud platforms (Render, Railway, etc.)
- 🗑️ Clear chat history functionality
- ⚡ Built with Flask and vanilla JavaScript (no heavy frameworks)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Local Installation & Usage
## 🚀 Live Chatbot

Try the live chatbot here:

https://chatbot-api-wa1s.onrender.com
1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd python-chatbot
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the chatbot:**
   - **On your local machine:** Open a browser and go to `http://127.0.0.1:5000`
   - **On other devices on your network:** 
     - Find your computer's IP address (it will be displayed when you run the app)
     - On other devices, visit `http://[YOUR_IP_ADDRESS]:5000`

   Example output when running:
   ```
   🚀 ChatBot is running!
   📱 Local access: http://127.0.0.1:5000
   💻 Network access: http://192.168.1.100:5000
   📝 Share the network address with other devices on your Wi-Fi
   ```

## ☁️ Cloud Deployment Instructions

### Option 1: Deploy to Render (Free Tier)

1. Push your code to a GitHub repository
2. Go to [Render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click "Create Web Service"

### Option 2: Deploy to Railway (Free Tier)

1. Push your code to a GitHub repository
2. Go to [Railway.app](https://railway.app) and create a new project
3. Deploy from GitHub and select your repository
4. Railway will automatically detect the Python environment and install dependencies
5. Make sure the start command is: `python app.py`

### Option 3: Deploy to Other Platforms (Heroku, Fly.io, etc.)

The application is designed to work with any platform that supports Python Flask applications. Just ensure:
- The start command runs `python app.py` or uses a WSGI server like Gunicorn
- The app listens on all interfaces (`0.0.0.0`) and the port provided by the platform's `PORT` environment variable

## 🔧 Customization

### Changing Bot Responses
Edit the `BOT_RESPONSES` dictionary in `app.py` to add or modify responses:

```python
BOT_RESPONSES = {
    "hello": "Hello! How can I help you today?",
    # Add more responses here
    "default": "I'm not sure I understand. Could you rephrase that or ask something else?"
}
```

### Styling
Modify the CSS in `templates/index.html` to change the appearance.

## 📝 Notes

- This chatbot uses in-memory storage, so chat history will be reset when the server restarts.
- For production use with persistent storage, consider integrating a database like SQLite, PostgreSQL, or Redis.
- The bot's responses are rule-based. For more advanced conversations, consider integrating with NLP libraries or AI APIs.

## 🛡️ Security Considerations

For local network use, this application is safe. If deploying to the public internet:
- Consider adding authentication
- Use environment variables for the secret key
- Implement rate limiting to prevent abuse

## 🎉 Enjoy!

You now have a working chatbot that you can access from your phone, tablet, or any other device on your network. Have fun chatting with your Python-powered assistant!

---

**Created with ❤️ using Python and Flask**
