from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home page - show notes
@app.route("/")
def index():
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

# Add new note
@app.route("/add", methods=("POST",))
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# Edit note
@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit_note(id):
    conn = get_db_connection()
    note = conn.execute("SELECT * FROM notes WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn.execute(
            "UPDATE notes SET title=?, content=? WHERE id=?",
            (title, content, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", note=note)

# Delete note
@app.route("/delete/<int:id>")
def delete_note(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
