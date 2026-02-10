import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

tables = [
    """CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE,
        password TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );""",

    """CREATE TABLE IF NOT EXISTS EmergencyContact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        phone_number TEXT,
        email TEXT,
        FOREIGN KEY(user_id) REFERENCES User(id)
    );""",

    """CREATE TABLE IF NOT EXISTS Location (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        name TEXT,
        risk_score REAL
    );""",

    """CREATE TABLE IF NOT EXISTS Route (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        origin_id INTEGER,
        destination_id INTEGER,
        route_type TEXT,
        total_distance REAL,
        safety_score REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES User(id),
        FOREIGN KEY(origin_id) REFERENCES Location(id),
        FOREIGN KEY(destination_id) REFERENCES Location(id)
    );""",

    """CREATE TABLE IF NOT EXISTS RouteSegment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        start_location_id INTEGER,
        end_location_id INTEGER,
        risk_weight REAL,
        distance REAL,
        FOREIGN KEY(route_id) REFERENCES Route(id),
        FOREIGN KEY(start_location_id) REFERENCES Location(id),
        FOREIGN KEY(end_location_id) REFERENCES Location(id)
    );""",

    """CREATE TABLE IF NOT EXISTS SensorEvent (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        accel_x REAL,
        accel_y REAL,
        accel_z REAL,
        gyro_x REAL,
        gyro_y REAL,
        gyro_z REAL,
        anomaly_score REAL,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES User(id)
    );""",

    """CREATE TABLE IF NOT EXISTS AudioEvent (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        distress_probability REAL,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES User(id)
    );""",

    """CREATE TABLE IF NOT EXISTS EmergencyAlert (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        location_id INTEGER,
        final_risk_score REAL,
        alert_triggered BOOLEAN,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES User(id),
        FOREIGN KEY(location_id) REFERENCES Location(id)
    );""",

    """CREATE TABLE IF NOT EXISTS MLModel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        version TEXT,
        accuracy REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        file_path TEXT
    );"""
]

for table in tables:
    cursor.execute(table)

conn.commit()
conn.close()
print("Tables created successfully!") 
