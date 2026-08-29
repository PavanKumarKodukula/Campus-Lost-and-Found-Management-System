import csv

def get_statistics():

    try:
        with open("data/lost_items.csv", "r", newline="") as file:
            lost_items = list(csv.DictReader(file))

        with open("data/found_items.csv", "r", newline="") as file:
            found_items = list(csv.DictReader(file))

    except FileNotFoundError:
        print("Required data file not found")
        return None

    total_lost = len(lost_items)
    total_found = len(found_items)

    currently_lost = 0
    currently_found = 0
    returned_items = 0

    for item in lost_items:
        if item["status"] == "LOST":
            currently_lost += 1
        elif item["status"] == "FOUND":
            currently_found += 1
        elif item["status"] == "RETURNED":
            returned_items += 1

    return_rate = 0

    if total_found > 0:
        return_rate = (returned_items / total_found) * 100

    return {
        "total_lost": total_lost,
        "total_found": total_found,
        "currently_lost": currently_lost,
        "currently_found": currently_found,
        "returned_items": returned_items,
        "return_rate": return_rate
    }