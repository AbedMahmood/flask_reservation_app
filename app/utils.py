# utils.py
import os, re
import json
import secrets
import string
import random
from flask import render_template, current_app
from datetime import datetime, timedelta, date


# --------------------- Data Functions ---------------------
def generate_sample_data(RESERVATION_TYPES, DATA_FILE):
    existing_data = get_json_data(DATA_FILE)
    
    if len(existing_data) >= 10:
        return  # Don't generate new data if there are already 10 or more records

    num_records_to_generate = max(6 - len(existing_data), 0)  # Generate up to 6 records total

    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones"]
    reservation_types = [rtype[0] for rtype in RESERVATION_TYPES]
    times = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

    new_data = []
    for _ in range(num_records_to_generate):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        record = {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "reservation_type": random.choice(reservation_types),
            "reservation_date": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            "reservation_time": random.choice(times),
            "reservation_key": ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        }
        new_data.append(record)

    combined_data = existing_data + new_data

    with open(DATA_FILE, 'w') as file:
        json.dump(combined_data, file, indent=4)


def write_record_to_json(record, DATA_FILE):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(record)
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def get_json_data(DATA_FILE):
    reservations = []
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                content = file.read().strip()
                
                if content:
                    reservations = json.loads(content)
                else:
                    print(f"The file {DATA_FILE} is empty.")
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from file {DATA_FILE}: {e}")
        except Exception as e:
            print(f"Unexpected error while reading file {DATA_FILE}: {e}")
    else:
        print(f"The file {DATA_FILE} does not exist.")
    
    return reservations


def get_record_by_hash_key(hash_key):
    reservations = get_json_data(current_app.config['DATA_FILE'])
    reservation = next((r for r in reservations if r['reservation_key'] == hash_key), None)
    return reservation


def update_record_by_hash_key(hash_key, updated_data, DATA_FILE):
    reservations = get_json_data(DATA_FILE)
    updated_reservations = []
    
    for reservation in reservations:
        if reservation['reservation_key'] == hash_key:
            reservation.update(updated_data)  # Make sure the updated_data keys match
        updated_reservations.append(reservation)
    
    with open(DATA_FILE, 'w') as file:
        json.dump(updated_reservations, file, indent=4)


def delete_record_by_hash_key(hash_key, DATA_FILE):
    reservations = get_json_data(DATA_FILE)
    updated_reservations = [r for r in reservations if r['reservation_key'] != hash_key]
    
    with open(DATA_FILE, 'w') as file:
        json.dump(updated_reservations, file, indent=4)
    
    return len(reservations) != len(updated_reservations)



# --------------------- Helper Functions ---------------------
def render_page(template_name, page_title, **context):
    css_file = get_css_file(template_name)

    if 'reservations' in context:
        for reservation in context['reservations']:
            if isinstance(reservation['reservation_date'], str):
                try:
                    reservation['reservation_date'] = datetime.strptime(reservation['reservation_date'], '%Y-%m-%d')
                except ValueError:
                    pass

    return render_template(
        template_name,
        page_title=page_title,
        website_name=current_app.config['WEBSITE_NAME'],
        year=current_app.config['YEAR'],
        css_file=css_file,
        navigation_items=current_app.config['NAVIGATION_ITEMS'],
        **context
    )


def delete_data_file(DATA_FILE):
    """Delete the JSON file."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        print(f"The file '{DATA_FILE}' has been deleted.")
    else:
        print(f"The file '{DATA_FILE}' does not exist.")


def get_css_file(template_name):
    base_name = os.path.splitext(template_name)[0]
    return f"{base_name}.css"


def count_records(DATA_FILE):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
                return len(data)
        else:
            print("Error: The specified JSON file was not found.")
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def if_validated_reserve(data):
    required_fields = ['first_name', 'last_name', 'email', 'reservation_type', 'reservation_date', 'reservation_time']

    for field in required_fields:
        if not data.get(field):
            return False, f"{field.replace('_', ' ').capitalize()} is required."
    
    # Check email validity
    if not re.match(r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', data.get('email', '')):
        return False, "Invalid email format."

    # Ensure reservation date is in the future
    current_date = datetime.now().date()
    try:
        reservation_date = datetime.strptime(data['reservation_date'], "%Y-%m-%d").date()
        if reservation_date < current_date:
            return False, "Reservation date cannot be in the past."
    except ValueError:
        return False, "Invalid reservation date."

    return True, "Validated"


