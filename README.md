# task-management-api-fastapi
A Task Management REST API built with FastAPI, SQLAlchemy, SQLite, and JWT Authentication.

# 🚀 FastAPI Task Management API

A RESTful Task Management API built with **FastAPI** that allows users to register, authenticate using JWT, and securely manage their own tasks.

This project was built to learn backend development concepts including authentication, authorization, CRUD operations, dependency injection, and database interaction using SQLAlchemy.

---

## ✨ Features

- 👤 User Registration
- 🔐 Secure Password Hashing (bcrypt)
- 🔑 JWT Authentication
- 🛡️ Protected Routes
- ➕ Create Tasks
- 📋 View Your Tasks
- ✏️ Update Your Tasks
- ❌ Delete Your Tasks
- 🗄️ SQLite Database using SQLAlchemy ORM

---

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Passlib (bcrypt)
- Python-JOSE (JWT)

---

## 📂 Project Structure

```
.
├── main.py
├── requirements.txt
├── README.md
└── task.db (generated automatically)
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-task-management-api.git
```

Go into the project

```bash
cd fastapi-task-management-api
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn main:app --reload
```

Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/user` | Register a new user |
| POST | `/login` | Login and receive JWT |

---

### Tasks

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/taskcreate` | Create a new task |
| GET | `/tasks` | Get all tasks of logged-in user |
| PUT | `/updatetask/{task_id}` | Update a task |
| DELETE | `/task/{task_id}` | Delete a task |

---

## 🔒 Authentication Flow

1. Register a user
2. Login using email and password
3. Receive a JWT Access Token
4. Authorize using Swagger UI
5. Access protected task endpoints

---

## 📖 What I Learned

While building this project, I learned:

- FastAPI routing
- Dependency Injection
- SQLAlchemy ORM
- Password Hashing
- JWT Authentication
- Protected APIs
- CRUD Operations
- Database Sessions

---

## 🚀 Future Improvements

- PostgreSQL Integration
- SQLAlchemy Relationships
- Response Models
- Environment Variables (.env)
- Docker Support
- Unit Testing
- API Deployment

---

## 📄 License

This project is built for learning purposes.
