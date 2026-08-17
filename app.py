from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("items.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    conn = get_db_connection()
    conn.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    name = request.form["name"]
    conn = get_db_connection()
    conn.execute("UPDATE items SET name = ? WHERE id = ?", (name, id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)