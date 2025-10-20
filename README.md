
---

# Urban Mobility Data Explorer
Documentation: https://docs.google.com/document/d/17aqYhA6zAZCoZdjYkKeG31aFTatz3k6lhL1fzz6VA2A/edit?tab=t.0#heading=h.xcc4p8qxoyxa

**Project Overview**
The Urban Mobility Data Explorer is a full-stack application designed to analyze, clean, and visualize urban mobility datasets. It helps users explore taxi/trip data, detect anomalies, and gain insights into travel patterns, distances, speeds, and fares. The system includes a Python backend, SQLite database, and an interactive frontend dashboard with charts and a heatmap.

---

## Features

* **Data Cleaning**: Removes invalid or incomplete trip records. Logs unclean data for review.
* **Derived Features**: Computes additional metrics such as trip distance, speed, and fare statistics.
* **Suspicious Trip Detection**: Flags trips with abnormal characteristics (e.g., extreme speeds, invalid durations).
* **Database Integration**: Stores cleaned data in SQLite with structured tables (`trip`, `vendor`, `location`) and views (`trip_summary`, `daily_stats`, `vendor_stats`).
* **Frontend Dashboard**:

  * Interactive charts for trips, fares, and durations
  * Leaflet heatmap showing trip start/end density
  * Filters for vendors and dates
  * Real-time data fetching from the backend API
* **Logging**: Tracks removed/unclean trips to a CSV file.

---

## Project Structure

```
urban-mobility-data-explorer/
├── Backend/
│   ├── app.py                # Flask API
│   ├── calculation.py        # Feature engineering
│   ├── algorithm.py          # Data analysis and anomaly detection
│   ├── logger.py             # Logging of unclean/suspicious trips
│   └── Data/
│       ├── train.csv         # Original dataset
│       ├── cleaned_train.csv # Cleaned dataset
│       └── unclean.csv       # Invalid rows
├── Frontend/
│   ├── index.html            # Dashboard
│   ├── style.css             # Styles
│   └── main.js               # Frontend logic for charts and map
├── databases/
│   ├── setting_up_db.py      # Script to create SQLite DB
│   ├── schema.sql            # Database schema
│   └── urban_db.db           # SQLite database
└── README.md
```

---

## Requirements

* Python 3.9+

* Pip packages:

  * `pandas`
  * `flask`
  * `flask_cors`
  * `numpy`
  * `sqlite3` (standard library)

* Frontend:

  * `Chart.js` (via CDN)
  * `Leaflet.js` and `Leaflet.heat` (via CDN)

---

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend folder:

```bash
cd Backend
```

2. Install required packages:

```bash
pip install pandas flask flask_cors numpy
```

3. Ensure your raw dataset `train.csv` is in `Backend/Data/`.

---

### 2. Database Setup

1. Navigate to the database folder:

```bash
cd databases
```

2. Run the setup script to create SQLite DB and populate tables:

```bash
python3 setting_up_db.py
```

3. Verify database:

```bash
sqlite3 urban_db.db ".tables"
sqlite3 urban_db.db "SELECT COUNT(*) FROM trip;"
```

---

### 3. Running the Backend API

1. Start Flask:

```bash
cd Backend
python3 app.py
```

2. API Endpoints:

| Route           | Method | Description                                     |
| --------------- | ------ | ----------------------------------------------- |
| `/`             | GET    | Checks API status                               |
| `/process-data` | GET    | Cleans data, computes features, returns summary |

Example curl:

```bash
curl http://127.0.0.1:5000/process-data
```

---

### 4. Frontend Setup

1. Navigate to `Frontend/`:

```bash
cd Frontend
```

2. Open `index.html` in a browser.

3. Dashboard features:

   * Click **Process & Load Data** to fetch data from backend.
   * Use vendor filter to explore specific vendor trips.
   * Charts display trip counts, fare distributions, and speeds.
   * Heatmap shows trip density on a map.

---

## Data Cleaning & Logging

* Invalid rows are logged in `Backend/Data/unclean.csv`.
* Suspicious trips (e.g., extreme speeds) are logged using `logger.py`.
* Cleaned dataset is saved as `Backend/Data/cleaned_train.csv`.

---

## Visualization

* **Trip Charts**: Line/bar charts for daily trips.
* **Fare Scatter Plot**: Trip duration vs fare.
* **Heatmap**: Displays geographic density of trips on Leaflet map.
* Fully interactive, updates automatically after data processing.

---

## Folder Structure Notes

* `Backend/` → API, data processing, and cleaning.
* `databases/` → SQLite database and setup scripts.
* `Frontend/` → Interactive visualizations and dashboard.
* `Data/` inside backend → Raw and cleaned datasets.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request.

---


## Collaborators

* **Contibutor **: Thomas Odongo
* **Colaborator**: Kevin Nyawakira
* **Colaborator**: Cynthia Keza
---

