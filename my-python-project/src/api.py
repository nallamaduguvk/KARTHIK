from flask import Flask, jsonify, request, abort
import json
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path(__file__).resolve().parent.parent / 'students.json'

def load_students():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=4)


@app.route('/students', methods=['GET'])
def get_students():
    students = load_students()
    return jsonify(students)


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    students = load_students()
    if 0 <= student_id < len(students):
        return jsonify(students[student_id])
    abort(404)


@app.route('/students', methods=['POST'])
def add_student():
    if not request.json:
        abort(400)
    student = request.json
    required_fields = [
        'first_name', 'last_name', 'grade', 'age', 'phone_number',
        'email', 'address', 'father_name', 'mother_name'
    ]
    if not all(field in student for field in required_fields):
        abort(400)
    students = load_students()
    students.append(student)
    save_students(students)
    return jsonify(student), 201


if __name__ == '__main__':
    app.run(debug=True)
