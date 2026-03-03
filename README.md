# ISS Location API Pipeline 

An automated data pipeline that tracks the International Space Station (ISS) in real time. Every 5 minutes, the pipeline fetches the current ISS position from a live API and stores it in a PostgreSQL database for analysis.

## Overview

This project demonstrates a real-world automated ETL pipeline using a live public API. It runs on a schedule, continuously collecting and storing geolocation data that can be queried and analyzed over time.

## Tech Stack

- **Python 3** — pipeline logic
- **requests** — fetching data from the API
- **pandas** — transforming API response into structured data
- **SQLAlchemy + psycopg2** — database connection and loading
- **APScheduler** — scheduling the pipeline to run every 5 minutes
- **PostgreSQL** — storing the location data
- **pgAdmin 4** — database management and querying

## Data Source

[Open Notify ISS API](http://api.open-notify.org/iss-now.json) — a free, public API that returns the real-time position of the ISS. No API key required.

**Sample API Response:**
```json
{
  "iss_position": {
    "latitude": "32.456",
    "longitude": "-95.123"
  },
  "timestamp": 1709413200,
  "message": "success"
}
```

## Project Structure

```
iss-api-pipeline/
├── iss_pipeline.py   # Main ETL pipeline script
├── .gitignore        # Excludes .env and cache files
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL installed and running
- pgAdmin 4 (optional, for visual querying)

### Setup

1. Clone the repo:
```bash
git clone https://github.com/yourusername/iss-api-pipeline.git
cd iss-api-pipeline
```

2. Create and activate a virtual environment:
```bash
python3 -m venv etl_env
source etl_env/bin/activate
```

3. Install dependencies:
```bash
pip install pandas psycopg2-binary sqlalchemy requests apscheduler python-dotenv
```

4. Create a `.env` file in the project root with your database credentials:
```
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=space_data
```

5. Create a `space_data` database in PostgreSQL (via pgAdmin or terminal).

### Run the Pipeline

```bash
python3 iss_pipeline.py
```

Expected output:
```
[2026-03-02 19:00:00] Fetching ISS position...
  → Lat: 32.456, Lon: -95.123
Scheduler started — running every 5 minutes. Press Ctrl+C to stop.
[2026-03-02 19:05:00] Fetching ISS position...
  → Lat: 41.872, Lon: -110.445
```

The pipeline runs indefinitely, fetching a new position every 5 minutes. Press **Ctrl+C** to stop.

## Database Schema

Data is stored in a table called `iss_location`:

| Column | Type | Description |
|---|---|---|
| `timestamp` | timestamp | Time of ISS position reading (UTC) |
| `latitude` | float | ISS latitude (-90 to 90) |
| `longitude` | float | ISS longitude (-180 to 180) |
| `fetched_at` | timestamp | Time the record was inserted |

## Sample Queries

```sql
-- View latest positions
SELECT * FROM iss_location ORDER BY fetched_at DESC LIMIT 10;

-- Count total readings collected
SELECT COUNT(*) AS total_readings FROM iss_location;

-- See how far the ISS traveled between readings
SELECT
  timestamp,
  latitude,
  longitude,
  latitude - LAG(latitude) OVER (ORDER BY timestamp) AS lat_change,
  longitude - LAG(longitude) OVER (ORDER BY timestamp) AS lon_change
FROM iss_location
ORDER BY timestamp DESC;
```

## What I Learned

- Calling a live REST API with Python and parsing JSON responses
- Scheduling automated tasks with APScheduler
- Appending real-time data to a PostgreSQL table incrementally
- Managing database credentials securely with environment variables

## License

MIT
