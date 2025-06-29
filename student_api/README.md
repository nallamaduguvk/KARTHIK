# Student API

This project provides a simple REST API for managing student details using [FastAPI](https://fastapi.tiangolo.com/). Data can be stored in MongoDB or kept in-memory for testing.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Motor (MongoDB driver)
- Jinja2

All required packages are listed in `requirements.txt`.

## Running the API

Install dependencies and start the application using `uvicorn`:

```bash
pip install -r requirements.txt
uvicorn student_api.app.main:app --reload
```

If the environment variable `MONGODB_URI` is set, the API will store data in MongoDB. Otherwise it falls back to an in-memory store.

The server will start at `http://127.0.0.1:8000`. Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Using Postman

Once the server is running you can exercise the API with [Postman](https://www.postman.com/):

1. Open Postman and create a new request.
2. Set the request URL to `http://127.0.0.1:8000/students` and choose the appropriate HTTP method.
3. For POST and PUT requests, select **Body → raw → JSON** and provide the student data.
4. Send the request and inspect the response.

Example JSON body:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "grade": "10",
  "age": 16,
  "phone_number": "1234567890",
  "email": "john@example.com",
  "address": "123 Main St",
  "father_name": "Jack Doe",
  "mother_name": "Jane Doe"
}
```

## Available Endpoints

- `POST /students` – Create a new student
- `GET /students` – List all students
- `GET /students/{student_id}` – Retrieve a student by ID
- `PUT /students/{student_id}` – Update an existing student
- `DELETE /students/{student_id}` – Delete a student

## Running Tests

Tests use `pytest`. Execute them with:

```bash
pytest
```
