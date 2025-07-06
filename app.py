
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            is_done INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']  # 폼에서 보낸 내용 받아오기

    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

    return redirect('/')  # 작업 후 메인 페이지로 다시 이동


@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()

    # 현재 상태 조회
    cur.execute('SELECT is_done FROM todos WHERE id = ?', (todo_id,))
    current = cur.fetchone()[0]

    # 반대 값으로 업데이트
    new_status = 0 if current else 1
    cur.execute('UPDATE todos SET is_done = ? WHERE id = ?', (new_status, todo_id))

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)