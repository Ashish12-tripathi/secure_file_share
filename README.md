# 🔐 Secure File Share

A secure, FastAPI-based file sharing backend system that allows users to upload, download, and manage files with role-based authentication and JWT authorization.

---

## 📦 Features

- ✅ **JWT Authentication** for secure login
- 🔐 **Role-based access control** (e.g., user, ops)
- 📁 **Secure file upload & download**
- 🗃️ **File metadata management**
- 🧑‍💼 Admin/Operator-level endpoints
- ⚙️ Built with **FastAPI + SQLAlchemy**
- 📄 Interactive API Docs using **Swagger (OpenAPI)**

---

## 🚀 Tech Stack

| Tech            | Description                |
|----------------|----------------------------|
| **FastAPI**     | Web framework (backend)    |
| **SQLAlchemy**  | ORM for database access    |
| **SQLite / PostgreSQL** | Database engine        |
| **Pydantic**    | Data validation            |
| **JWT**         | Authentication/authorization |
| **Uvicorn**     | ASGI server for FastAPI    |

---

## 🔐 Authentication Flow

- Users authenticate via `/ops/login` with email and password
- JWT token is issued on success
- Protected endpoints require the JWT token in `Authorization: Bearer <token>`

---

## 📂 Project Structure

  secure_file_share/
├── apps/
│ ├── main.py
│ ├── routes/
│ │ ├── ops.py
│ │ ├── client.py
│ ├── models/
│ ├── database.py
│ ├── schemas/
│ └── utils/
├── requirements.txt
├── README.md
└── test_cases/
