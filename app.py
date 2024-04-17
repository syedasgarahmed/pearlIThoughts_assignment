from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data for doctors and their schedules
doctors = [
    {
        "id": "1",
        "name": "Dr. John Doe",
        "specialization": "Cardiologist",
        "location": "Hospital XYZ",
        "schedule": {
            "Monday": ["17:00", "18:00"],
            "Tuesday": ["17:00", "18:00"],
            "Wednesday": ["17:00", "18:00"],
            "Thursday": ["17:00", "18:00"],
            "Friday": ["17:00", "18:00"],
            "Saturday": [],
            "Sunday": []
        }
    },
    {
        "id": "2",
        "name": "Dr. Jane Smith",
        "specialization": "Dermatologist",
        "location": "Hospital XYZ",
        "schedule": {
            "Monday": ["17:00", "18:00"],
            "Tuesday": ["17:00", "18:00"],
            "Wednesday": ["17:00", "18:00"],
            "Thursday": ["17:00", "18:00"],
            "Friday": ["17:00", "18:00"],
            "Saturday": [],
            "Sunday": []
        }
    }
]
import json
import os

# Directory to store appointment data JSON files
DATA_DIR = 'appointments_data'

# Function to save appointment data to a JSON file
def save_appointment_data(data):
    # Create the appointments_data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Generate a unique filename for the appointment data JSON file
    filename = os.path.join(DATA_DIR, f"appointment_{data['doctor_id']}_{data['date']}_{data['time']}.json")
    
    # Write the appointment data to the JSON file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Route for booking appointments
@app.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    patient_name = data.get('patient_name')
    date = data.get('date')
    time = data.get('time')

    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if doctor:
        # Check if the requested date and time slot are available
        if date in doctor['schedule'] and time in doctor['schedule'][date]:
            # Book the appointment
            appointment_details = {
                'doctor_id': doctor_id,
                'doctor_name': doctor['name'],
                'patient_name': patient_name,
                'date': date,
                'time': time
            }
            # Save the appointment data to a JSON file
            save_appointment_data(appointment_details)
            return jsonify({'message': 'Appointment booked successfully!', 'appointment_details': appointment_details})
        else:
            return jsonify({'message': 'The requested date or time slot is not available for the selected doctor.'}), 400
    else:
        return jsonify({'message': 'Doctor not found.'}), 404


@app.route('/about')
def about():
    return 'This is the about page!'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
