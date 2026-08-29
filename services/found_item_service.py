import csv
import os

from models.found_item import FoundItem
from services.lost_item_service import get_lost_items, update_lost_item_status, get_lost_item_by_id
from services.auth_service import get_user_by_id


def generate_found_id():
    file_path = "data/found_items.csv"

    if not os.path.exists(file_path):
        return "F001"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        items = list(reader)

    return f"F{len(items) + 1:03d}"


def find_lost_item(lost_id):
    lost_items = get_lost_items()
    for item in lost_items:
        if item.get_lost_id() == lost_id: return item
    return None


def report_found_item(lost_id, finder_user_id, found_date, found_location):
    lost_item = find_lost_item(lost_id)

    if lost_item is None:
        return "Lost Item Not Found"

    if lost_item.get_status() != "LOST":
        return "This Item Is No Longer Available"

    found_id = generate_found_id()
    found_item = FoundItem(found_id, lost_id, finder_user_id, found_date, found_location, "FOUND")

    with open("data/found_items.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            found_item.get_found_id(),
            found_item.get_lost_id(),
            found_item.get_finder_user_id(),
            found_item.get_found_date(),
            found_item.get_found_location(),
            found_item.get_status()
        ])

    update_lost_item_status(lost_id, "FOUND")
    return found_item


def get_found_items():
    found_items = []

    try:
        with open("data/found_items.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                found_item = FoundItem(
                    row["found_id"],
                    row["lost_id"],
                    row["finder_user_id"],
                    row["found_date"],
                    row["found_location"],
                    row["status"]
                )
                found_items.append(found_item)

    except FileNotFoundError:
        print("Found items data file not found")

    return found_items


def display_found_items(found_items):
    if len(found_items) == 0:
        return False

    for item in found_items:
        print("\n" + "-" * 45)
        print("Found ID       :", item.get_found_id())
        print("Lost ID        :", item.get_lost_id())
        print("Finder User ID :", item.get_finder_user_id())
        print("Found Date     :", item.get_found_date())
        print("Found Location :", item.get_found_location())
        print("Status         :", item.get_status())
        print("-" * 45)

    return True


def get_my_found_items(user_id):
    found_items = get_found_items()
    my_items = []

    for item in found_items:
        if item.get_finder_user_id() == user_id:
            my_items.append(item)

    return my_items


def get_found_item_by_id(found_id):
    found_items = get_found_items()
    for item in found_items:
        if item.get_found_id() == found_id: return item
    return None


def update_found_item_status(found_id, status):
    found_items = get_found_items()
    found = False

    for item in found_items:
        if item.get_found_id() == found_id:
            item.set_status(status)
            found = True
            break

    if not found:
        return False

    with open("data/found_items.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["found_id", "lost_id", "finder_user_id", "found_date", "found_location", "status"])

        for item in found_items:
            writer.writerow([
                item.get_found_id(),
                item.get_lost_id(),
                item.get_finder_user_id(),
                item.get_found_date(),
                item.get_found_location(),
                item.get_status()
            ])

    return True


def claim_found_item(found_id, user_id):
    found_item = get_found_item_by_id(found_id)

    if found_item is None:
        return "Found Item Not Found"

    lost_item = get_lost_item_by_id(found_item.get_lost_id())

    if lost_item is None:
        return "Lost Item Not Found"

    if lost_item.get_user_id() != user_id:
        return "Only the Owner Can Claim This Item"

    if found_item.get_status() != "FOUND":
        return "Item Is Already Returned"

    update_lost_item_status(found_item.get_lost_id(), "RETURNED")
    update_found_item_status(found_id, "RETURNED")

    return True


def get_contact_details(found_id, user_id):
    found_item = get_found_item_by_id(found_id)

    if found_item is None:
        return None

    lost_item = get_lost_item_by_id(found_item.get_lost_id())

    if lost_item is None:
        return None

    owner_id = lost_item.get_user_id()
    finder_id = found_item.get_finder_user_id()

    if user_id == owner_id:
        contact_user = get_user_by_id(finder_id)
        return {"role": "owner", "contact": contact_user}

    if user_id == finder_id:
        contact_user = get_user_by_id(owner_id)
        return {"role": "finder", "contact": contact_user}

    return {"role": "other", "contact": None}