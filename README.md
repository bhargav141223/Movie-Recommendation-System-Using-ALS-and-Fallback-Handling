# Movie Recommendation System - Big Data Analytics Project

A comprehensive movie recommendation system built with **Apache Spark** and **Django**, featuring collaborative filtering with ALS (Alternating Least Squares), real-time poster enrichment, and auto-updating CSV exports.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Big Data Pipeline](#big-data-pipeline)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [Data Export](#data-export)
- [Screenshots](#screenshots)

---

## 🎯 Overview

This project demonstrates a complete Big Data Analysis workflow for building a movie recommendation system:

1. **Data Processing** - Load and analyze MovieLens datasets using Apache Spark
2. **Model Training** - Train collaborative filtering models with Spark MLlib ALS
3. **Artifact Generation** - Export item-item similarity matrices and Top-K neighbors
4. **Web Serving** - Django web application consumes artifacts for real-time recommendations
5. **Data Persistence** - SQLite for user management, ratings, and poster cache
6. **External Enrichment** - OMDb API integration for movie posters
7. **Auto-Export** - Real-time CSV exports on user login and rating events

---

## ✨ Features

### User Features
- **User Authentication** - Secure login/signup with Django auth
- **Movie Library** - Browse movies with genre filtering and search
- **Smart Search** - Case-insensitive title search with instant results
- **Rate Movies** - 5-star rating system for personalized recommendations
- **My Ratings** - View complete rating history with timestamps
- **Export Ratings** - Download all ratings as CSV

### Recommendation Engine
- **Item-Item Collaborative Filtering** - ALS-based similarity computation
- **Top-K Neighbors** - Fast recommendations using precomputed neighbors
- **Fallback Model** - Dense similarity matrix for broader coverage
- **Poster Enrichment** - Automatic poster fetching via OMDb API
- **Watch Links** - Direct Google search links for streaming options

### Big Data Features
- **Spark OLAP** - Exploratory data analysis at scale
- **Distributed Training** - ALS model training on large datasets
- **Parquet Artifacts** - Efficient storage and loading of similarity matrices
- **Auto-Updating CSV** - Real-time data exports to `csv_exports/` folder

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Offline: Apache Spark (BDA_PROJECT.ipynb)                 │
│  ├─ Load CSVs (movies, ratings, links, tags)               │
│  ├─ OLAP Analysis (counts, distributions)                  │
│  ├─ Train ALS Model (userId × movieId × rating)            │
│  ├─ Extract Item Factors & Compute Cosine Similarity       │
│  └─ Export item_topk.parquet                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Online: Django Web App (Port 8000)                        │
│  ├─ User Login/Signup                                      │
│  ├─ Library (search + genre + rate)                        │
│  ├─ Rate Movie → Resolve title → movieId                   │
│  ├─ Recommendations:                                        │
│  │   ├─ Prefer: item_topk.parquet (Top-K)                  │
│  │   └─ Fallback: demo_model.parquet (Dense)              │
│  ├─ Enrich with OMDb API Posters                          │
│  ├─ Persist: SQLite (users, ratings, poster cache)        │
│  └─ Auto-Export: CSV files on login/rating events         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Big Data & ML
- **Apache Spark** - Distributed data processing and model training
- **PySpark MLlib** - ALS collaborative filtering
- **Pandas** - Data manipulation and CSV generation
- **PyArrow/Fastparquet** - Parquet file I/O

### Web Framework
- **Django 5.2.8** - Web application framework
- **SQLite** - User authentication and rating persistence
- **Django Signals** - Event-driven CSV auto-export
- **Whitenoise** - Static file serving

### External Services
- **OMDb API** - Movie poster and metadata enrichment

### Frontend
- **HTML/CSS/JavaScript** - Responsive UI
- **Bootstrap** - CSS framework
- **jQuery** - DOM manipulation and AJAX

---

## 📦 Installation

### Prerequisites
- Python 3.8+ (tested on 3.11)
- pip package manager
- Optional: Java 11+ (for Spark notebook)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd movie-recommendation-system-master
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create `.env` file in project root:
   ```env
   OMDB_API_KEY=your_omdb_api_key_here
   ```
   
   Get your free OMDb API key: https://www.omdbapi.com/apikey.aspx

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   
   Open browser: `http://127.0.0.1:8000/`

---

## 🚀 Usage

### For End Users

1. **Sign Up / Login**
   - Navigate to `/login/` or `/signup/`
   - Create an account or log in with existing credentials

2. **Browse Movies**
   - Visit `/library/` to browse the movie catalog
   - Filter by genre or search by title
   - View movie posters and details

3. **Rate Movies**
   - Click on stars (1-5) to rate any movie
   - Ratings are instantly saved to your profile

4. **Get Recommendations**
   - After rating, view personalized recommendations
   - Or search a movie on homepage for similar movies
   - Click "Watch" buttons for streaming search links

5. **View My Ratings**
   - Visit `/my-ratings/` to see your complete rating history
   - Click `/export-ratings/` to download CSV

### For Developers

**Run CSV Export Manually:**
```bash
python export_to_csv.py
```

**View User Data in Terminal:**
```bash
python show_user_data.py
```

**Train Custom Model (Spark):**
Open `BDA_PROJECT.ipynb` in Jupyter and follow the cells for ALS training.

---

## 📊 Big Data Pipeline

### Step 1: Data Loading (Spark)
```python
movies = spark.read.csv('movies.csv', header=True)
ratings = spark.read.csv('ratings.csv', header=True)
```

### Step 2: OLAP Analysis
- Count distinct users and movies
- Analyze rating distributions
- Compute sparsity metrics

### Step 3: ALS Model Training
```python
als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating",
          rank=64, maxIter=15, regParam=0.08, coldStartStrategy="drop")
model = als.fit(ratings)
```

### Step 4: Top-K Neighbor Generation
- Extract item factors from trained model
- Normalize vectors to unit length
- Compute cosine similarity for each item
- Select top 50 neighbors per movie
- Export to `item_topk.parquet`

### Step 5: Django Integration
- Copy `item_topk.parquet` to `static/`
- Django views auto-detect and use for recommendations
- Falls back to `demo_model.parquet` if not available

---

## 📁 Project Structure

```
movie-recommendation-system-master/
│
├── recommender/                 # Django app
│   ├── models.py               # User, Rating, PosterCache models
│   ├── views.py                # Main logic (recommendations, ratings)
│   ├── urls.py                 # URL routing
│   ├── signals.py              # Auto-export CSV on events
│   ├── templates/              # HTML templates
│   │   └── recommender/
│   │       ├── index.html      # Homepage
│   │       ├── login.html      # Login page
│   │       ├── library.html    # Movie library
│   │       ├── recommendations.html
│   │       ├── my_ratings.html
│   │       └── ...
│   └── ...
│
├── static/                      # Static files
│   ├── demo_model.parquet      # Dense similarity matrix
│   ├── item_topk.parquet       # Top-K neighbors (optional)
│   ├── top_2k_movie_data.parquet
│   ├── login_banner.jpg        # Custom login image
│   └── ...
│
├── csv_exports/                 # Auto-generated CSV files
│   ├── statistics.csv
│   ├── all_users.csv
│   ├── all_ratings.csv
│   ├── user_summary.csv
│   ├── <username>_ratings.csv
│   └── README.txt
│
├── movies.csv                   # Movie metadata
├── BDA_PROJECT.ipynb           # Spark training notebook
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys)
├── db.sqlite3                  # SQLite database
│
├── export_to_csv.py            # Manual CSV export script
├── show_user_data.py           # Terminal data viewer
└── README.md                    # This file
```

---

## 🔌 API Integration

### OMDb API

**Purpose:** Fetch movie posters and metadata

**Configuration:**
1. Sign up at https://www.omdbapi.com/apikey.aspx
2. Add API key to `.env`:
   ```env
   OMDB_API_KEY=your_key_here
   ```

**Features:**
- Title + year matching
- Fallback to title-only search
- Multi-result search with best match
- Database caching (PosterCache model)
- In-memory caching for performance

**Usage in Code:**
```python
from recommender.views import fetch_poster
poster_url = fetch_poster("Toy Story (1995)")
```

---

## 💾 Data Export

### Auto-Export (Signals)

CSV files in `csv_exports/` folder are **automatically updated** on:
- User login
- Movie rating created/updated

**Files Generated:**
1. `statistics.csv` - Database metrics
2. `all_users.csv` - User login information
3. `all_ratings.csv` - Complete rating history
4. `user_summary.csv` - Per-user statistics
5. `<username>_ratings.csv` - Individual user files

### Manual Export

**Terminal View:**
```bash
python show_user_data.py
```

**CSV Export:**
```bash
python export_to_csv.py
```

**Web Export:**
Visit `http://127.0.0.1:8000/export-ratings/` to download ratings CSV.

---

---

## 🔧 Configuration

### Model Selection

Django automatically prefers `item_topk.parquet` if available, otherwise falls back to `demo_model.parquet`.

To use your custom model:
1. Train in `BDA_PROJECT.ipynb`
2. Export `item_topk.parquet`
3. Copy to `static/item_topk.parquet`
4. Restart Django server

### Database

**SQLite** is used by default (`db.sqlite3`).

**Models:**
- `User` - Django built-in auth model
- `Rating` - User movie ratings
- `PosterCache` - Cached OMDb posters

**Reset Database:**
```bash
rm db.sqlite3
python manage.py migrate
```

---

## 📝 Requirements

```txt
wheel
django==5.2.8
pandas
gunicorn
whitenoise
fastparquet
pyarrow
requests
python-dotenv
openpyxl  # For Excel exports (optional)
```

---

## 🌟 Key Features Summary

✅ **Big Data Analysis** - Spark-based OLAP and model training  
✅ **Collaborative Filtering** - ALS item-item recommendations  
✅ **Real-time Serving** - Django web app with low latency  
✅ **Poster Enrichment** - OMDb API with caching  
✅ **Auto-Updating CSVs** - Export on login/rating events  
✅ **User Authentication** - Secure signup/login  
✅ **Rating System** - 5-star ratings with history  
✅ **Search & Filter** - Genre filtering and title search  
✅ **Export Functionality** - Download ratings as CSV  
✅ **Responsive UI** - Bootstrap-based interface

---


## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📧 Contact

 **Kuppam Bhargav Reddy**
 _Department of Artificial Intelligence_
 _Amrita School of Artificial Intelligence, Bengaluru_
 _Amrita Vishwa Vidyapeetham, India_
 bl.en.u4aid23028@bl.students.amrita.edu
 
- **Likhit Hegde**
 _Department of Artificial Intelligence_
 _Amrita School of Artificial Intelligence, Bengaluru_
 _Amrita Vishwa Vidyapeetham, India_
 bl.en.u4aid23029@bl.students.amrita.edu

- **N Viswa Vardhan Reddy**
 _Department of Artificial Intelligence_
 _Amrita School of Artificial Intelligence, Bengaluru_
 _Amrita Vishwa Vidyapeetham, India_
 bl.en.u4aid23035@bl.students.amrita.edu


**Built with ❤️ using Apache Spark and Django**

