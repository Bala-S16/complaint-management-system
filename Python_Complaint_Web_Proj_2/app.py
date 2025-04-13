from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

app = Flask(__name__)
COMPLAINT_FILE = "complaints.txt"

def generate_id():
    return f"CMP{int(datetime.datetime.now().timestamp())}"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        complaint = request.form['complaint']
        complaint_id = generate_id()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(COMPLAINT_FILE, "a") as file:
            file.write(f"{complaint_id}|{name}|{complaint}|{time}\n")
        return redirect(url_for('home'))
    return render_template("submit.html")

@app.route('/view')
def view():
    complaints = []
    if os.path.exists(COMPLAINT_FILE):
        with open(COMPLAINT_FILE, "r") as file:
            for line in file:
                complaint_id, name, complaint, time = line.strip().split('|')
                complaints.append({
                    'id': complaint_id,
                    'name': name,
                    'complaint': complaint,
                    'time': time
                })
    return render_template("view.html", complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)
