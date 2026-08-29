import csv
import os

from models.student import Student
from models.admin import Admin


def generate_student_id():

    file_path = "data/users.csv"

    if not os.path.exists(file_path):
        return "S101"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        users = list(reader)

    student_count = 0

    for user in users:
        if user["role"] == "student":
            student_count += 1

    return f"S{101 + student_count:03d}"


def check_duplicate_student(college_id, email):

    try:
        with open("data/users.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for user in reader:

                if user["college_id"] == college_id:
                    return "College ID already registered"

                if user["email"] == email:
                    return "Email already registered"

    except FileNotFoundError:
        return None

    return None


def register_student(name, college_id, email, phone, password):

    duplicate = check_duplicate_student(college_id, email)

    if duplicate is not None:
        return duplicate

    user_id = generate_student_id()

    student = Student(
        user_id,
        name,
        college_id,
        email,
        phone,
        password
    )

    with open("data/users.csv", "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            student.get_user_id(),
            student.get_name(),
            student.get_college_id(),
            student.get_email(),
            student.get_phone(),
            student.get_password(),
            student.get_role()
        ])

    return student


def login(email, password):

    try:
        with open("data/users.csv", "r", newline="") as file:

            reader = csv.DictReader(file)

            for user in reader:

                if user["email"] == email and user["password"] == password:

                    if user["role"] == "student":

                        return Student(
                            user["user_id"],
                            user["name"],
                            user["college_id"],
                            user["email"],
                            user["phone"],
                            user["password"]
                        )

                    elif user["role"] == "admin":

                        return Admin(
                            user["user_id"],
                            user["name"],
                            user["college_id"],
                            user["email"],
                            user["phone"],
                            user["password"]
                        )

    except FileNotFoundError:

        print("User data file not found")
        return None

    return None


def get_user_by_id(user_id):

    with open("data/users.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for user in reader:

            if user["user_id"] == user_id:

                return {
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "email": user["email"],
                    "phone": user["phone"]
                }

    return None


def get_all_students():

    students = []

    with open("data/users.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for user in reader:

            if user["role"] == "student":
                students.append(user)

    return students