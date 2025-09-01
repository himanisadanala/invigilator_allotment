from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('allotment.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def generate_allotment(teachers, rooms):
    """
    Randomly assigns teachers to rooms for invigilation.
    Ensures an even distribution of duties.
    """
    # Create a list of all required slots (one invigilator per room for simplicity)
    all_rooms = rooms * (len(teachers) // len(rooms)) + rooms[:len(teachers) % len(rooms)]

    if len(teachers) < len(all_rooms):
        return None  # Not enough teachers for the required slots

    # Shuffle both lists to ensure no partiality
    random.shuffle(teachers)
    random.shuffle(all_rooms)
    
    allotment = {}
    for i in range(len(teachers)):
        room = all_rooms[i]
        teacher = teachers[i]
        
        if room not in allotment:
            allotment[room] = []
        allotment[room].append(teacher)
        
    return allotment

@app.route('/')
def index():
    """Renders the main page with the option to trigger allotment."""
    return render_template('index.html')

@app.route('/allot', methods=['POST'])
def allot():
    """Handles allotment generation using data from the database."""
    conn = get_db_connection()
    
    # Retrieve all teachers from the database
    teachers_data = conn.execute('SELECT name FROM teachers').fetchall()
    teachers = [row['name'] for row in teachers_data]

    # Retrieve all rooms from the database
    rooms_data = conn.execute('SELECT room_number FROM rooms').fetchall()
    rooms = [row['room_number'] for row in rooms_data]
    
    conn.close()

    # Call the allotment function
    allotment_result = generate_allotment(teachers, rooms)
    
    if allotment_result is None:
        return "Error: Not enough teachers for the number of rooms.", 400

    # Render the results page with the generated allotment
    return render_template('results.html', allotment=allotment_result)

if __name__ == '__main__':
    app.run(debug=True)
