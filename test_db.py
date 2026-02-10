import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# 1️⃣ Insert a user first
cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
               ("Alice", "alice@example.com", "password123"))
alice_id = cursor.lastrowid  # fetch the ID of the inserted user

# 2️⃣ Insert EmergencyContact for that user
cursor.execute("INSERT INTO emergencycontact (user_id, name, phone_number, email) VALUES (?, ?, ?, ?)",
               (alice_id, "Mom", "1234567890", "mom@example.com"))

# 3️⃣ Insert Location
cursor.execute("INSERT INTO location (latitude, longitude, name, risk_score) VALUES (?, ?, ?, ?)",
               (12.9716, 77.5946, "Home", 0.1))
home_id = cursor.lastrowid

cursor.execute("INSERT INTO location (latitude, longitude, name, risk_score) VALUES (?, ?, ?, ?)",
               (12.9352, 77.6245, "Office", 0.2))
office_id = cursor.lastrowid

# 4️⃣ Insert Route for user
cursor.execute("""
INSERT INTO route (user_id, origin_id, destination_id, route_type, total_distance, safety_score)
VALUES (?, ?, ?, ?, ?, ?)""",
               (alice_id, home_id, office_id, "safest", 10.5, 0.95))
route_id = cursor.lastrowid

# 5️⃣ Insert RouteSegment for that route
cursor.execute("""
INSERT INTO routesegment (route_id, start_location_id, end_location_id, risk_weight, distance)
VALUES (?, ?, ?, ?, ?)""",
               (route_id, home_id, office_id, 0.1, 10.5))

conn.commit()
conn.close()
print("Data inserted successfully!")


