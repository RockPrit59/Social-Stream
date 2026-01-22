# 🚀 Social Stream - Real-Time Django Social Platform

A full-stack social networking application built with **Django** and **Django Channels**. This project features user profiles, a social feed, follow/unfollow functionality, and a **real-time private chat system** powered by WebSockets and Redis.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/django-5.0-green.svg)
![Redis](https://img.shields.io/badge/redis-channels-red.svg)

---

## 📸 Screenshots

### Real-Time Chat (WebSocket)
*Private messaging with synchronized room logic.*
![Real Time Chat](path/to/your/image_ae116c.png)

### User Feed & Interface
*Responsive social feed and profile management.*
![Social Feed](path/to/your/image_ada12c.png)

---

## ✨ Features

- **🔐 User Authentication:** Secure Login, Registration, and Logout.
- **👤 Profile Management:** Profile pictures, bios, and "Follow/Unfollow" system.
- **📰 Social Feed:** View posts from users you follow.
- **💬 Real-Time Chat:**
  - Instant messaging using **WebSockets** (Django Channels).
  - **Smart Room Logic:** Automatically sorts usernames (e.g., `chat_UserA_UserB`) to ensure two users always connect to the same private room.
  - Auto-scrolling and real-time UI updates.
- **🔍 Search:** Find other users by username.
- **☁️ Production Ready:** Configured for deployment on **Railway** with PostgreSQL and Redis.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django 5.x
- **Real-Time Layer:** Django Channels, Daphne, Redis
- **Database:** SQLite (Local), PostgreSQL (Production)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (WebSockets)
- **Deployment:** Railway (Cloud), Whitenoise (Static Files)

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/RockPrit59/Social-Stream](https://github.com/RockPrit59/Social-Stream)
cd Social-Stream
2. Create a Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Apply Database Migrations
python manage.py migrate
5. Run the Development Server
python manage.py runserver
Note on Chat: For local development, the project is configured to use an InMemoryChannelLayer by default. If you want to test with Redis locally, ensure you have Redis installed and update settings.py.
🚀 Deployment (Railway)
This project is optimized for deployment on Railway.app.

1.Push to GitHub.

2.Connect Railway: Create a new project on Railway and select your GitHub repo.

3.Add Redis: Add a Redis service in Railway and link it.

4.Environment Variables: Railway usually handles REDIS_URL and DATABASE_URL automatically.

5.Start Command:
daphne -b 0.0.0.0 -p $PORT core.asgi:application
📂 Project Structure
├── core/                # Main project configuration (Settings, ASGI, WSGI)
├── feed/                # Main app: Feed, Posts, and Search logic
│   ├── consumers.py     # WebSocket logic for handling chat messages
│   ├── routing.py       # URL routing for WebSockets
│   └── views.py         # Views for the feed and posts
├── users/               # Authentication and Profile management
├── static/              # CSS, JS, and Static assets
├── templates/           # HTML Templates
└── manage.py            # Django command-line utility
🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

📄 License
This project is licensed under the MIT License.