from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Monitoring</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
        .container { max-width: 800px; margin: 0 auto; }
        .form-group { margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather Monitoring System</h1>
        <form action="/" method="post">
            <div class="form-group">
                <label for="city">Enter City Name:</label><br>
                <input type="text" id="city" name="city" required>
                <input type="submit" value="Get Weather">
            </div>
        </form>

        {% if weather_data %}
            <h2>Weather Information for {{ city_name }}</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>City</th>
                    <th>Average Temp (°C)</th>
                    <th>Max Temp (°C)</th>
                    <th>Min Temp (°C)</th>
                    <th>Feels Like (°C)</th>
                    <th>Weather</th>
                </tr>
                {% for entry in weather_data %}
                <tr>
                    <td>{{ entry[0] }}</td>
                    <td>{{ entry[1] }}</td>
                    <td>{{ "%.1f"|format(entry[2]) }}</td>
                    <td>{{ "%.1f"|format(entry[3]) }}</td>
                    <td>{{ "%.1f"|format(entry[4]) }}</td>
                    <td>{{ "%.1f"|format(entry[5]) }}</td>
                    <td>{{ entry[6] }}</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            {% if city_name %}
                <p>No data available for {{ city_name }}.</p>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

def fetch_weather_data(city_name):
    print(f"Fetching weather data for {city_name} from the database...")
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM daily_summary WHERE city=? ORDER BY date DESC", (city_name,))
    data = c.fetchall()
    
    conn.close()
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city_name = None
    
    if request.method == 'POST':
        city_name = request.form.get('city')
        if city_name:
            weather_data = fetch_weather_data(city_name)
    
    return render_template_string(HTML_TEMPLATE, weather_data=weather_data, city_name=city_name)

if __name__ == '__main__':
    app.run(debug=True)
