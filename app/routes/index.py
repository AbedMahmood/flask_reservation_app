# index.py
import os, secrets
from flask import Blueprint, request, current_app, redirect, url_for, flash
from datetime import datetime
from app.utils import (if_validated_reserve, 
write_record_to_json, render_page, count_records,
generate_sample_data, update_record_by_hash_key, 
delete_record_by_hash_key, get_record_by_hash_key, 
get_json_data )

from config import Config

bp = Blueprint('main', __name__)

@bp.route('/error')
def error():
    return render_page('pages/error.html', "Error")


@bp.route('/')
@bp.route('/<page_name>')
def main(page_name='home'):
    if page_name not in current_app.config['ALLOWED_PAGES']:
        return redirect(url_for('main.error'))

    template_path = 'pages/main.html' if page_name == 'home' else f'pages/{page_name}.html'
    template_full_path = os.path.join(current_app.root_path, 'templates', template_path)

    if os.path.exists(template_full_path):
        return render_page(template_path, page_name.capitalize())
    else:
        return redirect(url_for('main.error'))
    


@bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        if count_records(Config.DATA_FILE) >= 10:
            flash('Sorry, we have reached the maximum number of reservations.', 'error')
            return redirect(url_for('main.error'))

        reservation_data = request.form.to_dict()
        is_valid, message = if_validated_reserve(reservation_data)
        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('main.reserve'))

        try:
            reservation_data['reservation_key'] = secrets.token_hex(3)  # Unique 6-character key
            write_record_to_json(reservation_data, Config.DATA_FILE)
            return render_page('pages/reservation.html', 'Reservation Confirmed', reservation_data=reservation_data)
        except Exception as e:
            current_app.logger.error(f"Error during reservation: {e}")
            flash('There was an error processing your reservation. Please try again.', 'error')
            return redirect(url_for('main.reserve'))

    reservation_types = current_app.config['RESERVATION_TYPES']
    return render_page('pages/reserve.html', 'Make a Reservation', reservation_types=reservation_types)



@bp.route('/reservations', methods=['GET'])
def reservations():
    DATA_FILE = Config.DATA_FILE
    RESERVATION_TYPES = current_app.config['RESERVATION_TYPES']

    if not os.path.isfile(DATA_FILE):
        generate_sample_data(RESERVATION_TYPES, DATA_FILE)

    reservations = get_json_data(DATA_FILE)
    if len(reservations) < 3:
        generate_sample_data(RESERVATION_TYPES, DATA_FILE)
        reservations = get_json_data(DATA_FILE)

    return render_page('pages/reservations.html', 'Upcoming Appointments', reservations=reservations)




@bp.route('/reservations/update/<hash_key>', methods=['POST'])
def update_reservation(hash_key):
    updated_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],  # Ensure 'email' is used here
        'reservation_type': request.form['reservation_type'],
        'reservation_date': request.form['reservation_date'],
        'reservation_time': request.form['reservation_time']
    }

    update_record_by_hash_key(hash_key, updated_data, Config.DATA_FILE)
    return redirect(url_for('main.reservations'))



@bp.route('/reservations/delete/<hash_key>', methods=['POST'])
def delete_reservation_action(hash_key):
    if delete_record_by_hash_key(hash_key, Config.DATA_FILE):
        flash('Reservation deleted successfully.', 'success')
    else:
        flash('Reservation not found.', 'error')
    return redirect(url_for('main.reservations'))



@bp.route('/reservations/edit/<hash_key>', methods=['GET', 'POST'])
def edit_reservation(hash_key):
    if request.method == 'POST':
        try:
            updated_data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'reservation_type': request.form['reservation_type'],
                'reservation_date': request.form['reservation_date'],
                'reservation_time': request.form['reservation_time']
            }
            update_record_by_hash_key(hash_key, updated_data, Config.DATA_FILE)
            return redirect(url_for('main.reservations'))
        except Exception:
            return render_page('pages/error.html', 'Error', error_message="An error occurred while updating the reservation.")

    reservation = get_record_by_hash_key(hash_key)
    
    if reservation is None:
        return redirect(url_for('main.reservations'))

    reservation_types = current_app.config['RESERVATION_TYPES']
    return render_page('pages/edit_reservation.html', 'Edit Reservation', reservation=reservation, reservation_types=reservation_types)



@bp.route('/reservations/confirm_delete/<hash_key>', methods=['GET'])
def confirm_delete_reservation(hash_key):
    reservation = get_record_by_hash_key(hash_key)
    
    if reservation:
        # Ensure the date is a datetime object
        if isinstance(reservation['reservation_date'], str):
            reservation['reservation_date'] = datetime.strptime(reservation['reservation_date'], '%Y-%m-%d')
        
        return render_page('pages/delete_reservation.html', 'Confirm Delete Reservation', reservation=reservation)
    
    flash('Reservation not found.', 'error')
    return redirect(url_for('main.reservations'))





