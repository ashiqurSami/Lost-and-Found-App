# 🧳 Lost & Found Item Tracker API (Backend)

A Django REST Framework-based backend API for tracking and managing lost and found items. Built to support public browsing, matching, real-time communication, and geolocation filtering with production-level scalability.

---

## 🚀 Features

- ✅ JWT Authentication (via SimpleJWT)
- 📝 Post Lost or Found Items (with optional image upload)
- 🔍 Public Item Browsing and Filtering (postgres full text based search)
- 📍 Geo-based Radius Search (PostGIS + GeoDjango)
- 🤝 Smart Matching System on category, date, keyword, location within 3km radius (postgres-trigram)
- 📞 Claim and Contact System (secure, audit-tracked)
- 💬 Real-Time Chat (via Django Channels + Redis)
- ✅ Mark Items as Resolved
- 🛠️ Admin Panel (moderation, abuse handling)
- 📄 Swagger/OpenAPI Documentation (via drf-spectacular)

---

## 🏗️ Tech Stack

- **Backend:** Django 5.x, Django REST Framework
- **Real-time:** Django Channels + Redis
- **Database:** PostgreSQL + PostGIS
- **Auth:** JWT (SimpleJWT)
- **API Docs:** drf-spectacular
- **Image Handling:** Django ImageField

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/lost-found-api.git
cd lost-found-api
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
