from datetime import datetime

def calculate_age(birthdate_str):
    """
    Calculate age based on the birthdate string in 'YYYY-MM-DD' format.
    """
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

if __name__ == "__main__":
    birthdate_input = input("Enter your birthdate (YYYY-MM-DD): ")
    try:
        age = calculate_age(birthdate_input)
        print(f"You are {age} years old.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")