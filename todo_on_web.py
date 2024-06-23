#Aaron's personal todo list
#Aaron's Get-To-It List
from flask import Flask, jsonify, request, render_template
import json
from datetime import datetime

app = Flask(__name__)

TASKS_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
            return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    today = datetime.today().date()
    updated_tasks = []

    for task in tasks:
        task_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
        if task_date < today:
            task['due_date'] = today.strftime('%Y-%m-%d')
        updated_tasks.append(task)

    # Sort tasks by due date and then by name
    updated_tasks.sort(key=lambda x: (x['due_date'], x['name']))

    save_tasks(updated_tasks)
    return jsonify(updated_tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = load_tasks()
    new_task = {
        'name': request.form['name'],
        'due_date': request.form['due_date']
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return '', 201

@app.route('/tasks/<int:task_index>', methods=['DELETE'])
def delete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_tasks(tasks)
        return '', 204
    return '', 404

@app.route('/tasks/<int:task_index>', methods=['PUT'])
def edit_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index] = {
            'name': request.form['name'],
            'due_date': request.form['due_date']
        }
        save_tasks(tasks)
        return '', 204
    return '', 404

if __name__ == '__main__':
    app.run(host='192.168.50.214', port=9000, debug=True)
