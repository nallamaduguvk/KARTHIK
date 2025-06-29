import json

def get_student_details():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    grade = input("Grade: ")
    age = input("Age: ")
    phone_number = input("Phone Number: ")
    email = input("Email: ")
    address = input("Address: ")
    father_name = input("Father's Name: ")
    mother_name = input("Mother's Name: ")
    return {
        "first_name": first_name,
        "last_name": last_name,
        "grade": grade,
        "age": age,
        "phone_number": phone_number,
        "email": email,
        "address": address,
        "father_name": father_name,
        "mother_name": mother_name
    }

def save_student_to_json(student, filename='students.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(student)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    print("Enter student details:")
    student = get_student_details()
    save_student_to_json(student)
    print("Student details saved to JSON file.")

if __name__ == "__main__":
    main()
