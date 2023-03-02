from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import pdfkit

# Set up the Flask app
app = Flask(__name__)

# Set up the SQLite database connection
conn = sqlite3.connect('clinic.db', check_same_thread=False)
cursor = conn.cursor()

# Create the patients table
cursor.execute('''CREATE TABLE IF NOT EXISTS patients
                  (id INTEGER PRIMARY KEY,
                   patient_id INTEGER,
                   name TEXT,
                   dob TEXT,
                   gender TEXT,
                   phone TEXT,
                   address TEXT,
                   timestamp TEXT)''')

# Create the appointments table
cursor.execute('''CREATE TABLE IF NOT EXISTS appointments
                  (id INTEGER PRIMARY KEY,
                   name TEXT,
                   phone TEXT,
                   doctor TEXT,
                   date TEXT,
                   time TEXT,
                   notes TEXT,
                   timestamp TEXT)''')

# Create the prescriptions table
cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions
                  (id INTEGER PRIMARY KEY,
                   patient_id INTEGER,
                   doctor TEXT,
                   date TEXT,
                   medication TEXT,
                   dosage TEXT,
                   instructions TEXT,
                   timestamp TEXT)''')


# Define the routes for the web application
@app.route('/')
def home():
  return render_template('home.html')


@app.route('/reception')
def reception():
  # Retrieve all patients from the database
  cursor.execute('SELECT * FROM patients')
  patients = cursor.fetchall()
  return render_template('reception.html', patients=patients)


@app.route('/reception/search', methods=['GET', 'POST'])
def reception_search():
  if request.method == 'POST':
    # Retrieve the search query from the form
    query = request.form['query']

    # Search for the patient by name, ID, or phone number
    cursor.execute(
      'SELECT * FROM patients WHERE name LIKE ? OR id = ? OR phone = ?',
      ('%' + query + '%', query, query))
    patients = cursor.fetchall()

    return render_template('reception.html', patients=patients)
  else:
    return redirect(url_for('reception'))


@app.route('/reception/new_patient', methods=['GET', 'POST'])
def reception_new_patient():
  if request.method == 'POST':
    # Add the new patient to the database
    name = request.form['name']
    phone = request.form['phone']
    dob = request.form['dob']
    gender = request.form['gender']
    address = request.form['address']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
      'INSERT INTO patients (name, phone, dob, gender, address, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
      (name, phone, dob, gender, address, timestamp))
    conn.commit()
    return redirect(url_for('reception'))
  else:
    # Generate a new patient ID
    cursor.execute('SELECT MAX(id) FROM patients')
    result = cursor.fetchone()[0]
    if result is None:
      patient_id = 1
    else:
      patient_id = result + 1

    return render_template('new_patient.html', patient_id=patient_id)


@app.route('/reception/<int:patient_id>')
def reception_view_patient(patient_id):
  # Retrieve the patient from the database
  cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id, ))
  patient = cursor.fetchone()

  # Retrieve all appointments for the patient from the database
  cursor.execute('SELECT * FROM appointments WHERE patient_id = ?',
                 (patient_id, ))
  appointments = cursor.fetchall()

  # Retrieve all prescriptions for the patient from the database
  cursor.execute('SELECT * FROM prescriptions WHERE patient_id = ?',
                 (patient_id, ))
  prescriptions = cursor.fetchall()

  return render_template('view_patient.html',
                         patient=patient,
                         appointments=appointments,
                         prescriptions=prescriptions)


@app.route('/reception/<int:patient_id>/new_appointment',
           methods=['GET', 'POST'])
def reception_new_appointment():
  if request.method == 'POST':
    # Add the new appointment to the database
    doctor = request.form['doctor']
    date = request.form['date']
    reason = request.form['reason']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
      'INSERT INTO appointments (patient_id, doctor, date, reason, timestamp) VALUES (?, ?, ?, ?, ?)',
      (patient_id, doctor, date, reason, timestamp))
    conn.commit()
    return redirect(url_for('reception_view_patient', patient_id=patient_id))
  else:
    return render_template('new_appointment.html', patient_id=patient_id)

@app.route('/reception/search_appointment',
           methods=['GET', 'POST'])
def reception_search_appointment():
  if request.method == 'POST':
    # Retrieve the search query from the form
    query = request.form['query']

    # Search for the patient by name, ID, or phone number
    cursor.execute(
      'SELECT * FROM appointments WHERE name LIKE ? OR id = ? OR phone = ?',
      ('%' + query + '%', query, query))
    appointments = cursor.fetchall()

    return render_template('reception.html', appointments=appointments)
  else:
    return redirect(url_for('reception'))

@app.route('/doctor/int:patient_id')
def doctor(patient_id):
  # Retrieve the patient from the database
  cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id, ))
  patient = cursor.fetchone()
  # Retrieve all appointments for the patient from the database
  cursor.execute('SELECT * FROM appointments WHERE patient_id = ?',
                 (patient_id, ))
  appointments = cursor.fetchall()

  # Retrieve all prescriptions for the patient from the database
  cursor.execute('SELECT * FROM prescriptions WHERE patient_id = ?',
                 (patient_id, ))
  prescriptions = cursor.fetchall()

  return render_template('doctor.html',
                         patient=patient,
                         appointments=appointments,
                         prescriptions=prescriptions)


@app.route('/doctor/<int:patient_id>')
def doctor_view_patient(patient_id):
  # Retrieve the patient from the database
  cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id, ))
  patient = cursor.fetchone()

  # Retrieve all appointments for the patient from the database
  cursor.execute('SELECT * FROM appointments WHERE patient_id = ?',
                 (patient_id, ))
  appointments = cursor.fetchall()

  # Retrieve all prescriptions for the patient from the database
  cursor.execute('SELECT * FROM prescriptions WHERE patient_id = ?',
                 (patient_id, ))
  prescriptions = cursor.fetchall()

  return render_template('doctor_view_patient.html',
                         patient=patient,
                         appointments=appointments,
                         prescriptions=prescriptions)


@app.route('/doctor/int:patient_id/update_patient', methods=['GET', 'POST'])
def update_patient(patient_id):
  if request.method == 'POST':
    # Update the patient in the database
    name = request.form['name']
    dob = request.form['dob']
    address = request.form['address']
    phone = request.form['phone']
    gender = request.form['gender']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
      'UPDATE patients SET name = ?, dob = ?, address = ?, phone = ?, email = ?, insurance = ? WHERE id = ?',
      (name, dob, address, phone, gender, timestamp, patient_id))
    conn.commit()
    return redirect(url_for('doctor', patient_id=patient_id))
  else:
    # Retrieve the patient from the database
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id, ))
    patient = cursor.fetchone()
    return render_template('update_patient.html', patient=patient)


@app.route('/doctor/<int:patient_id>/new_prescription',
           methods=['GET', 'POST'])
def doctor_new_prescription(patient_id):
  if request.method == 'POST':
    # Add the new prescription to the database
    doctor = request.form['doctor']
    date = request.form['date']
    medication = request.form['medication']
    dosage = request.form['dosage']
    instructions = request.form['instructions']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
      'INSERT INTO prescriptions (patient_id, doctor, date, medication, dosage, instructions, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
      (patient_id, doctor, date, medication, dosage, instructions, timestamp))
    conn.commit()
    return redirect(url_for('doctor_view_patient', patient_id=patient_id))
  else:
    return render_template('doctor_new_prescription.html',
                           patient_id=patient_id)


# Define the route to print a prescription
@app.route('/doctor/prescriptions/<int:prescription_id>/print')
def doctor_print_prescription(prescription_id):
  # Retrieve the prescription from the database
  cursor.execute('SELECT * FROM prescriptions WHERE id = ?',
                 (prescription_id, ))
  prescription = cursor.fetchone()

  # Generate the HTML content of the prescription
  html = render_template('prescription.html', prescription=prescription)

  # Generate the PDF file and return it
  pdf = pdfkit.from_string(html, False)
  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers[
    'Content-Disposition'] = f'attachment; filename=prescription_{prescription_id}.pdf'
  return response


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)