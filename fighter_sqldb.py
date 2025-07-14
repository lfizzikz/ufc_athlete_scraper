import csv
import sqlite3

conn = sqlite3.connect("ufc_analysis.db")
cur = conn.cursor()

cur.execute(
    """
CREATE TABLE If NOT EXISTS fighters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT,
    record          TEXT,
    weight_class    TEXT,
    nick_name       TEXT
    )
    """
)
conn.commit()

with open("fighters.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            "INSERT INTO fighters (name, record, weight_class, nick_name) VALUES (?, ?, ?, ?)",
            (row["name"], row["record"], row["weight_class"], row["nick_name"]),
        )
conn.commit()

cur.execute("SELECT COUNT(*) FROM fighters")
total = cur.fetchone()[0]
print("Total fighters in DB:", total)

cur.close()
conn.close()


def get_fighter_id(cur, name):
    cur.execute("SELECT id FROM fighters WHERE name LIKE ?", (f"%{name}%",))
    result = cur.fetchone()
    return result[0] if result else None


def insert_fight(cur, fight_data):
    cur.execute(
        """
        INSERT INTO fights (
        fighter_id, result, opponent, method, event,
        date, round, time, location, notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?)
    """,
        (
            fight_data["fighter_id"],
            fight_data["result"],
            fight_data["opponent"],
            fight_data["method"],
            fight_data["event"],
            fight_data["date"],
            fight_data["round"],
            fight_data["time"],
            fight_data["location"],
            fight_data["notes"],
        ),
    )
