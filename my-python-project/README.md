# My Python Project

This project includes simple scripts and a REST API for managing student details.

## Purpose

Originally this repository contained a "Hello, World!" example. It has now been
extended with a small API built using Flask that stores student information in
`students.json`.

## How to Run the API

1. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask application:

   ```bash
   python src/api.py
   ```

   The server will start on `http://127.0.0.1:5000` by default.

## API Endpoints

- `GET /students` – return the list of stored students.
- `GET /students/<id>` – return the student at the given index.
- `POST /students` – add a new student. Send a JSON body containing
  `first_name`, `last_name`, `grade`, `age`, `phone_number`, `email`, `address`,
  `father_name` and `mother_name`.

All student data is persisted in the `students.json` file at the project root.
