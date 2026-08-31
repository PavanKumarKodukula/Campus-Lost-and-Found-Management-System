# Campus Lost & Found System

A Python-based console application that helps students report, find, claim, and manage lost and found items within a college campus. Built using Object-Oriented Programming (OOP) concepts with CSV files for data storage.

---

## 📌 Project Overview

The Campus Lost & Found System provides separate access for **Students** and **Admins**. Students can report lost items, report found items, view reports, contact the concerned person, and claim found items. Admins can view students, lost items, found items, and system-wide statistics.

**Item lifecycle:**

```
LOST → FOUND → RETURNED
```

- **LOST** – a student reports an item as lost.
- **FOUND** – another student finds the item and reports it.
- **RETURNED** – the verified owner claims the found item.

---

## ✨ Features

### Student
- Registration with automatic student ID generation
- Duplicate College ID / email validation
- Login
- Report lost items
- Report found items
- View all lost / found items
- View personal lost / found reports
- Contact the owner or finder
- Claim found items (owner-verified)
- Logout

### Admin
- Login
- View registered students
- View lost items
- View found items
- View system statistics (total reports, currently lost/found, returned items, return rate)
- Logout

> Note: The current version does not include admin operations for editing or deleting item records.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3 |
| Paradigm | Object-Oriented Programming (OOP) |
| Data Storage | CSV files (`csv` module) |
| File/System Handling | `os` module |
| Interface | Console-based (no GUI/web frontend yet) |

---

## 🏗️ Project Structure

```
Campus-Lost-Found-System/
│
├── models/
│   ├── user.py          # Base User class
│   ├── student.py       # Student (inherits User)
│   ├── admin.py         # Admin (inherits User)
│   ├── lost_item.py     # LostItem model
│   └── found_item.py    # FoundItem model
│
├── services/
│   ├── auth_service.py         # Registration, login, student management
│   ├── lost_item_service.py    # Lost item reporting & retrieval
│   ├── found_item_service.py   # Found item reporting, claiming, contact
│   └── statistics_service.py   # System statistics
│
├── data/
│   ├── users.csv
│   ├── lost_items.csv
│   └── found_items.csv
│
└── main.py
```

**Architecture:** `main.py` → User Interface → Service Layer (Auth / Lost Item / Found Item / Statistics) → Model Layer (User → Student/Admin, LostItem, FoundItem) → CSV Data.

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.x installed

Check your Python version:
```bash
python --version
```

### 1. Clone or download the project
```bash
git clone <repository-url>
cd Campus-Lost-Found-System
```

### 2. Create the CSV data files (required)
Ensure the `models/` and `services/` folders are present, then create a `data/` folder with the three CSV files below **and their header rows already written in**.

> ⚠️ The app writes new records in append mode and does **not** write a header row on first run. If you skip this step, the first record you add (e.g. the first student registration) will be misread as the header row and break `csv.DictReader` parsing for every record after it.

Create `data/users.csv`:
```csv
user_id,name,college_id,email,phone,password,role
```

Create `data/lost_items.csv`:
```csv
lost_id,user_id,item_name,category,description,location,date,status
```

Create `data/found_items.csv`:
```csv
found_id,lost_id,finder_user_id,found_date,found_location,status
```

### 3. Add an admin account manually
There is no admin registration flow in the app (the main menu only offers **Student Registration**), so add at least one admin row to `data/users.csv` yourself, below the header:
```csv
A001,Admin,ADMIN001,admin@campus.com,9999999999,admin@123,admin
```
> ⚠️ Passwords are stored in plain text, so this admin row (and every student row created via the app) will contain a readable password.

### 4. Run the application
```bash
python main.py
```

### 5. Use the menu
```
CAMPUS LOST & FOUND SYSTEM

1. Student Registration
2. Login
3. Exit
```

No external/third-party packages are required — the project only uses Python's standard library (`csv`, `os`).

---

## 🗄️ Database / API Notes

- **No database or REST API is used in the current version.** Persistence is handled entirely through local **CSV files** via Python's `csv` module — a simple, dependency-free storage mechanism suited for this console app.
- `users.csv` — student and admin account records
- `lost_items.csv` — all reported lost items and their status
- `found_items.csv` — all reported found items, linked to lost items by ID, and their status
- ⚠️ Passwords are currently stored in plain text in `users.csv`; this is a known limitation (see below).

---

## 🧠 OOP Concepts Demonstrated

- **Classes & Objects** — `User`, `Student`, `Admin`, `LostItem`, `FoundItem`
- **Inheritance** — `Student(User)` and `Admin(User)`
- **Encapsulation** — private attributes (e.g. `self.__user_id`, `self.__status`) with getters/setters
- **Constructors** — `__init__()` initializes object state
- **`super()`** — used by `Student` and `Admin` to call the parent `User` constructor

---

## ⚠️ Current Limitations

- Data stored in CSV files instead of a database
- Passwords stored in plain text (not hashed)
- Console-based only; no GUI or web frontend
- No image upload support for items
- ID generation is based on existing CSV record counts

## 🔮 Future Enhancements

- MySQL database integration
- Flask REST API
- Web-based frontend
- Email notifications
- Search and filtering
- Admin item management (edit/delete)
- Smarter lost–found item matching

---

## 👥 Team Member Contributions

| Name | Role / Contribution |
|---|---|
| Venkat | Core models (`User`, `Student`, `Admin`), authentication service (registration, login, duplicate ID/email checks, student lookup), and `main.py` console UI / menu flow for both roles |
| Pavan | `LostItem` model, lost item service (report lost item, retrieve/list/update status, per-user lost reports), and statistics service (system-wide counts and return rate) |
| Vignesh | `FoundItem` model and found item service (report found item, claim/return workflow, contact-details lookup between owner and finder, per-user found reports) |
