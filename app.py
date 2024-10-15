from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['medical_service']
patients_collection = db['patients']
doctors_collection = db['doctors']
appointments_collection = db['appointments']

# Route to display the patient form
@app.route('/add_patients_form', methods=['GET'])
def show_add_patients_form():
    return render_template('add_patients.html')

# Route to add patients from the form
@app.route('/add_patients', methods=['POST'])
def add_patients():
    for i in range(1, 4):
        name = request.form[f'name{i}']
        birthday = request.form[f'birthday{i}']
        gender = request.form[f'gender{i}']
        address = request.form[f'address{i}']

        patient = {
            'name': name,
            'birthday': birthday,
            'gender': gender,
            'address': address
        }
        patients_collection.insert_one(patient)
    return redirect('/add_patients_form')

# Route to display the doctor form
@app.route('/add_doctors_form', methods=['GET'])
def show_add_doctors_form():
    return render_template('add_doctors.html')

# Route to add doctors from the form
@app.route('/add_doctors', methods=['POST'])
def add_doctors():
    for i in range(1, 6):
        name = request.form[f'doctor{i}']
        doctor = {'name': name}
        doctors_collection.insert_one(doctor)
    return redirect('/add_doctors_form')

# Route to display the appointment form
@app.route('/add_appointments_form', methods=['GET'])
def show_add_appointments_form():
    return render_template('add_appointments.html')

# Route to add appointments from the form
@app.route('/add_appointments', methods=['POST'])
def add_appointments():
    for i in range(1, 4):
        patient_name = request.form[f'patient_name{i}']
        doctor_name = request.form[f'doctor_name{i}']
        reason = request.form[f'reason{i}']
        date = request.form[f'date{i}']

        appointment = {
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'reason': reason,
            'date': date,
            'status': 'Pending'
        }
        appointments_collection.insert_one(appointment)
    return redirect('/add_appointments_form')

# Route to display report
@app.route('/report', methods=['GET'])
def generate_report():
    appointments = list(appointments_collection.find())
    report_data = []

    for appointment in appointments:
        patient = patients_collection.find_one({'name': appointment['patient_name']})
        report_data.append({
            'patient_name': appointment['patient_name'],
            'birthday': patient['birthday'] if patient else 'N/A',
            'gender': patient['gender'] if patient else 'N/A',
            'address': patient['address'] if patient else 'N/A',
            'doctor_name': appointment['doctor_name'],
            'reason': appointment['reason'],
            'date': appointment['date']
        })

    return render_template('report.html', appointments=report_data)

@app.route('/appointments/today', methods=['GET'])
def get_appointments_today():
    today = datetime.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
    today_appointments = list(appointments_collection.find({'date': today}))
    
    appointments_list = []

    for appointment in today_appointments:
        patient = patients_collection.find_one({'name': appointment['patient_name']})
        appointments_list.append({
            'address': patient['address'] if patient else 'N/A',
            'patient_name': appointment['patient_name'],
            'birthday': patient['birthday'] if patient else 'N/A',
            'gender': patient['gender'] if patient else 'N/A',
            'doctor_name': appointment['doctor_name'],
            'status': appointment['status'],
            'note': 'N/A'  # Placeholder for any additional notes
        })

    # Render the template and pass today's appointments to the HTML
    return render_template('today_appointments.html', appointments=appointments_list)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
