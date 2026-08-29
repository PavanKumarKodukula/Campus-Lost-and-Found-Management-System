import csv
import os

from models.lost_item import LostItem


def generate_lost_id():
    file_path = "data/lost_items.csv"

    if not os.path.exists(file_path):
        return "L001"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        items = list(reader)

    return f"L{len(items) + 1:03d}"


def report_lost_item(user_id, item_name, category, description, location, date):
    lost_id = generate_lost_id()

    lost_item = LostItem(
        lost_id,
        user_id,
        item_name,
        category,
        description,
        location,
        date,
        "LOST"
    )

    with open("data/lost_items.csv", "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            lost_item.get_lost_id(),
            lost_item.get_user_id(),
            lost_item.get_item_name(),
            lost_item.get_category(),
            lost_item.get_description(),
            lost_item.get_location(),
            lost_item.get_date(),
            lost_item.get_status()
        ])

    return lost_item


def get_lost_items():
    lost_items = []

    try:
        with open("data/lost_items.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                lost_item = LostItem(
                    row["lost_id"],
                    row["user_id"],
                    row["item_name"],
                    row["category"],
                    row["description"],
                    row["location"],
                    row["date"],
                    row["status"]
                )

                lost_items.append(lost_item)

    except FileNotFoundError:
        print("Lost items data file not found")

    return lost_items


def update_lost_item_status(lost_id, status):
    lost_items = get_lost_items()
    found = False

    for item in lost_items:
        if item.get_lost_id() == lost_id:
            item.set_status(status)
            found = True
            break

    if not found:
        return False

    with open("data/lost_items.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "lost_id",
            "user_id",
            "item_name",
            "category",
            "description",
            "location",
            "date",
            "status"
        ])

        for item in lost_items:
            writer.writerow([
                item.get_lost_id(),
                item.get_user_id(),
                item.get_item_name(),
                item.get_category(),
                item.get_description(),
                item.get_location(),
                item.get_date(),
                item.get_status()
            ])

    return True


def display_lost_items(lost_items):
    if len(lost_items) == 0:
        return False

    for item in lost_items:
        print("\n" + "-" * 45)
        print("Lost ID     :", item.get_lost_id())
        print("Item Name   :", item.get_item_name())
        print("Category    :", item.get_category())
        print("Description :", item.get_description())
        print("Location    :", item.get_location())
        print("Date        :", item.get_date())
        print("Status      :", item.get_status())
        print("-" * 45)

    return True


def get_my_lost_items(user_id):
    lost_items = get_lost_items()
    my_items = []

    for item in lost_items:
        if item.get_user_id() == user_id:
            my_items.append(item)

    return my_items


def get_lost_item_by_id(lost_id):
    lost_items = get_lost_items()

    for item in lost_items:
        if item.get_lost_id() == lost_id:
            return item

    return None
