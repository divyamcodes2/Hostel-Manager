# 🏨 Hostel Manager

A web application built to simplify complaint handling in hostels — connecting hostellers directly with wardens for quick resolution of issues. 🛠️✨

🔗 **Live Demo:** [https://hostel-manager-1.onrender.com/loginPage/login.html](https://hostel-manager-1.onrender.com/loginPage/login.html)

---

## 📖 Overview

Hostel Manager is a platform designed to bridge communication between hostellers and hostel authorities. It replaces manual registers and word-of-mouth complaint handling with a simple, trackable digital system. 📋➡️💻

---

## ✨ Features

- 📝 **Complaint Portal** – Hostellers can raise complaints directly through the website.
- 🔀 **Direct Routing to Warden** – Complaints are automatically forwarded to the concerned warden for quick action.
- 📊 **Status Tracking** – Hostellers and wardens can view the status of raised complaints (🟡 Pending / 🔵 In Progress / 🟢 Resolved).
- 🔐 **User Authentication** – Separate login access for hostellers and wardens.
- 🏠 **Room Management** – Admins can create hostel blocks/rooms and assign or remove students.
- 👥 **User Management** – Admins can create student & warden accounts and activate/deactivate users.
- 🍪 **Secure Sessions** – Cookie-based sessions configured for secure, cross-origin HTTPS deployments.

---

## 🧰 Tech Stack

| Layer 🧱 | Technology 🚀 |
|---|---|
| 🎨 Frontend | HTML, CSS, JavaScript |
| ⚙️ Backend | Python (Flask, Flask-SQLAlchemy, Flask-CORS) |
| 🗄️ Database | SQL (PostgreSQL via `psycopg2`, SQLite for local fallback) |
| 🌐 Server | Gunicorn |
| ☁️ Hosting | Render |

---

## 🗂️ Project Structure

```
Hostel-Manager-main/
├── backend/
│   ├── app.py              # 🏗️ Flask app factory & config
│   ├── models/              # 🧩 User, Room, Complaint models
│   └── routes/               # 🛣️ Auth, Complaints, Staff, Admin APIs
├── database/
│   ├── schema.sql            # 🗃️ Database schema
│   └── seed.py                # 🌱 Seed data script
├── frontend/
│   ├── admin/                 # 🛡️ Admin login & dashboard
│   ├── staff/                  # 👷 Warden login & dashboard
│   ├── student/                 # 🎓 Student login & dashboard
│   ├── loginPage/                # 🚪 Main login landing page
│   ├── css/                       # 🎨 Stylesheets
│   └── js/                         # ⚡ API client
├── uploads/                 # 📎 Uploaded files
├── requirements.txt          # 📦 Python dependencies
└── run.py                     # ▶️ App entry point
```

---

## 👤 User Roles

- 🎓 **Student** – Logs in, submits complaints, and tracks their status.
- 👷 **Warden** – Views incoming complaints and updates their status.
- 🛡️ **Admin** – Manages users, rooms, and room assignments.

---

## 🚀 Usage

1. 🔑 Hostellers log in and submit complaints through the dashboard.
2. 📬 Complaints are routed to the respective warden in real time.
3. ✅ Wardens review, update status, and resolve issues through their panel.
4. 🛡️ Admins manage users and rooms, and assign students to rooms.

---

## 🔌 API Overview

| Endpoint 🌍 | Method | Description |
|---|---|---|
| `/api/auth/login` | POST | 🔓 Log in a user |
| `/api/auth/me` | GET | 🙋 Get current session user |
| `/api/auth/logout` | POST | 🚪 Log out |
| `/api/complaints` | POST / GET | 📝 Create / list complaints |
| `/api/complaints/<id>` | GET | 🔍 Get a specific complaint |
| `/api/warden/complaints` | GET | 📋 List all complaints (warden) |
| `/api/warden/complaints/<id>` | PATCH | 🔄 Update complaint status |
| `/api/admin/users` | POST / GET | 👥 Create / list users |
| `/api/admin/rooms` | POST / GET | 🏠 Create / list rooms |
| `/api/admin/users/<id>/room` | PATCH | 🔀 Assign/remove student room |
| `/api/admin/users/<id>/status` | PATCH | ⚡ Activate/deactivate user |

---

## 💖 Made By CodePhoenix

Flask 🐍 + a lot of ☕ to make hostel life a little easier for everyone!
