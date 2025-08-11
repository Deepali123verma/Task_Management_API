# Task Management REST API

A secure and scalable Task Management REST API built with **Flask** and **PostgreSQL**, featuring **JWT authentication**, **role-based access control**, **RSA-based encryption**, and **Swagger API documentation**.  
Dockerized for easy deployment.

---

## 🚀 Features
- **User Authentication**: JWT-based secure login system
- **Role-Based Access**: Admin & User privileges
- **Task Management**: Create, assign, update, and track tasks
- **Data Security**: RSA asymmetric encryption for sensitive data
- **API Documentation**: Swagger UI for interactive testing
- **Docker Support**: Easy containerized deployment

---

## 🛠 Tech Stack
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT (Public/Private Key)
- **Docs**: Swagger (Flasgger)
- **Deployment**: Docker

---

## 📦 Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/task-management-api.git
cd task-management-api
2️⃣ Create Virtual Environment & Install Dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

pip install -r requirements.txt
3️⃣ Configure Environment Variables
Create a .env file:

env
Copy
Edit
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
JWT_PRIVATE_KEY=your_private_key
JWT_PUBLIC_KEY=your_public_key
JWT_ALGORITHM=RS256
4️⃣ Run with Docker (Optional)
bash
Copy
Edit
docker build -t task-api .
docker run -p 5000:5000 task-api
📜 API Documentation
After running the project, open:

bash
Copy
Edit
http://localhost:5000/apidocs

