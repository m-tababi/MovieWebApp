# 🎬 MovieWebApp

MovieWebApp is a lightweight but complete Flask web application for managing users and their favorite movies.  
The app integrates with the OMDb API to automatically fetch movie details such as title, year, IMDb rating, and poster.

It fully supports **CRUD operations** for:

- 👤 **Users**
- 🎞️ **Movies**

The application implements clean error handling, flash‑based notifications, and custom error pages for a smooth user experience.

---

## 🚀 Features

### ✔ User Management
- Create users  
- Display all users  
- View each user's movie list  

### ✔ Movie Management
- Add movies (auto‑fetch data from OMDb)  
- List movies per user or globally  
- Update movie titles  
- Delete movies  

### ✔ Automatic OMDb Integration
On movie creation, the app automatically loads:
- official title  
- release year  
- IMDb rating  
- poster image URL  

### ✔ Error Handling
- Flash notifications  
- Duplicate checks  
- Input validation  
- OMDb API failures handled cleanly  
- Custom **404** and **500** pages  

---

## 🛠️ Technologies

- Python 3.10+
- Flask
- Flask‑SQLAlchemy
- SQLite
- Jinja2 Templates
- OMDb API
- python‑dotenv

---

## 📂 Project Structure

```
MovieWebApp/
│
├── app.py
├── DataManager.py
├── models.py
│
├── data/
│   └── movies.sqlite3
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── users.html
│   ├── movies.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   └── style.css
│
├── .env
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, I can generate one for you.

---

## 🔑 Setup OMDb API Key

1. Create a `.env` file in the project root  
2. Add the following:

```env
OMDB_API_KEY=your_api_key_here
```

You can get a free key from:  
https://www.omdbapi.com/apikey.aspx

---

## 🗄️ Database Initialization

The database is automatically created at the first run:

```bash
python app.py
```

---

## ▶️ Run the App

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000/
```

---

## 🔗 Routes Overview

### User Routes

| Method | Route | Description |
|--------|--------|-------------|
| GET | `/` | Homepage, list of users |
| POST | `/create_user` | Create a new user |
| GET | `/users` | Display all users |
| GET | `/users/<id>` | Display movies of a specific user |

### Movie Routes

| Method | Route | Description |
|--------|--------|-------------|
| GET | `/movies` | Display all movies |
| POST | `/users/<id>/movies` | Add a movie for a user |
| POST | `/users/<id>/movies/<movie_id>/update` | Update a movie title |
| POST | `/users/<id>/movies/<movie_id>/delete` | Delete a movie |

---

## 🧩 Future Improvements

- Add Bootstrap for UI styling  
- Add pagination  
- Add movie search  
- Add OMDb autocomplete suggestions  
- Add user editing/deletion  
- Add authentication  

---

## 📜 License

This project is free to use for learning and development purposes.

---

## 👤 Author

Your Name  
GitHub: https://github.com/<your-username>
