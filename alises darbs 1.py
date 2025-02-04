from flask import Flask, render_template_string, request, redirect, url_for, flash
from datetime import datetime, timedelta
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Nepieciešams Flash ziņojumiem

# HTML veidne
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Reģistrācijas sistēma</title>
</head>
<body style="background-color:#87ceeb; text-align: center; font-family: Arial, sans-serif;">
    {% if step == 'start' %}
        <h1>Reģistrēšanās sākums</h1>
        <form action="/register" method="get">
            <button type="submit">Reģistrēties</button>
        </form>

    {% elif step == 'register' %}
        <h1>Ievadi datus</h1>
        <form method="POST" action="/register">
            <label>Vārds:</label><br>
            <input type="text" name="name" required><br><br>

            <label>Uzvārds:</label><br>
            <input type="text" name="surname" required><br><br>

            <label>Klase:</label><br>
            <input type="text" name="user_class" required><br><br>

            <input type="submit" value="Turpināt">
        </form>

    {% elif step == 'books' %}
        <h1>Tavi dati un grāmatu izvēle</h1>
        <p><strong>Vārds:</strong> {{ user_data.name }}</p>
        <p><strong>Uzvārds:</strong> {{ user_data.surname }}</p>
        <p><strong>Klase:</strong> {{ user_data.user_class }}</p>

        <form method="POST" action="/submit">
            <label>Izvēlies grāmatu:</label><br>
            {% for book in books %}
                <input type="radio" name="selected_book" value="{{ book }}" {% if loop.first %}checked{% endif %}> {{ book }}<br>
            {% endfor %}<br>

            <input type="hidden" name="name" value="{{ user_data.name }}">
            <input type="hidden" name="surname" value="{{ user_data.surname }}">
            <input type="hidden" name="user_class" value="{{ user_data.user_class }}">

            <input type="submit" value="Apstiprināt">
        </form>

        <h3>Pieejamās grāmatas:</h3>
        {% for book in available_books %}
            <p>{{ book }}</p>
        {% endfor %}
    {% endif %}

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul style="color: red;">
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template, step='start')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        user_class = request.form['user_class']

        if not name or not surname or not user_class:
            flash("Visi lauki jābūt aizpildītiem!")
            return redirect(url_for('register'))

        user_data = {
            'name': name,
            'surname': surname,
            'user_class': user_class
        }

        return render_template_string(html_template, step='books', user_data=user_data, 
                                      books=["Matemātika 101", "Grega Dienasgrāmata", "Vēsture", "Šekspīrs"],
                                      available_books=["Hamiltons", "Dzejas grāmata", "Latviešu valoda", "Fizika"])
    return render_template_string(html_template, step='register')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    surname = request.form['surname']
    user_class = request.form['user_class']
    selected_book = request.form['selected_book']
    return_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    # Saglabāšana CSV failā
    with open('registracija.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, surname, user_class, selected_book, return_date])

    flash(f"Tavs izvēlētais grāmata: {selected_book}. Atgriešanas datums: {return_date}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)















