from flask import Flask, render_template, jsonify, request
import sqlite3
import time
import random

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('water_conservation.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS campaigns
          (id INTEGER PRIMARY KEY, name TEXT, goal INTEGER, progress INTEGER, start_date TEXT, end_date TEXT)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS users
          (id INTEGER PRIMARY KEY, name TEXT, points INTEGER, pledges TEXT)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS resources
          (id INTEGER PRIMARY KEY, title TEXT, type TEXT, content TEXT)
          ''')

conn.commit()

# Mock data
campaigns = [
    {'id': 1, 'name': 'Save 100,000 Liters', 'goal': 100000, 'progress': 25000, 'start_date': '2024-08-01', 'end_date': '2024-12-31'},
    {'id': 2, 'name': 'Reduce Household Water Use by 20%', 'goal': 50000, 'progress': 12000, 'start_date': '2024-08-01', 'end_date': '2024-12-31'}
]

users = [
    {'id': 1, 'name': 'Alice', 'points': 150, 'pledges': 'Shorter showers, Use a broom instead of a hose'},
    {'id': 2, 'name': 'Bob', 'points': 200, 'pledges': 'Fix leaks, Install water-efficient fixtures'}
]

resources = [
    {'id': 1, 'title': '10 Tips to Save Water at Home', 'type': 'Article', 'content': 'Tip 1: Fix leaks...'},
    {'id': 2, 'title': 'How to Reduce Water Waste', 'type': 'Video', 'content': 'https://example.com/video'}
]

# Initialize database with mock data
def initialize_db():
    c.executemany('INSERT OR IGNORE INTO campaigns (id, name, goal, progress, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)', 
                  [(c['id'], c['name'], c['goal'], c['progress'], c['start_date'], c['end_date']) for c in campaigns])
    c.executemany('INSERT OR IGNORE INTO users (id, name, points, pledges) VALUES (?, ?, ?, ?)', 
                  [(u['id'], u['name'], u['points'], u['pledges']) for u in users])
    c.executemany('INSERT OR IGNORE INTO resources (id, title, type, content) VALUES (?, ?, ?, ?)', 
                  [(r['id'], r['title'], r['type'], r['content']) for r in resources])
    conn.commit()

initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/campaigns')
def get_campaigns():
    c.execute('SELECT * FROM campaigns')
    campaigns = c.fetchall()
    return jsonify(campaigns)

@app.route('/users')
def get_users():
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    return jsonify(users)

@app.route('/resources')
def get_resources():
    c.execute('SELECT * FROM resources')
    resources = c.fetchall()
    return jsonify(resources)

@app.route('/add_pledge', methods=['POST'])
def add_pledge():
    user_id = request.form['user_id']
    pledge = request.form['pledge']
    c.execute('UPDATE users SET pledges = pledges || ", " || ? WHERE id = ?', (pledge, user_id))
    conn.commit()
    return jsonify({'status': 'Pledge added successfully'})

@app.route('/add_points', methods=['POST'])
def add_points():
    user_id = request.form['user_id']
    points = int(request.form['points'])
    c.execute('UPDATE users SET points = points + ? WHERE id = ?', (points, user_id))
    conn.commit()
    return jsonify({'status': 'Points added successfully'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Water Conservation Campaign</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }}
        header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        section {{
            margin: 20px;
            padding: 20px;
            background-color: white;
            border-radius: 5px;
        }}
        h2 {{
            color: #4CAF50;
        }}
        .campaign-box, .user-box {{
            display: flex;
            justify-content: space-around;
        }}
        .item {{
            text-align: center;
            width: 30%;
            padding: 10px;
            background-color: #e0f7fa;
            border-radius: 10px;
        }}
        footer {{
            text-align: center;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            position: fixed;
            bottom: 0;
            width: 100%;
        }}
        .pledge-box {{
            margin: 20px;
            padding: 20px;
            background-color: #e0f7fa;
            border-radius: 5px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Water Conservation Campaign Dashboard</h1>
        <p>Join the movement to save water!</p>
    </header>

    <section>
        <h2>Current Campaigns</h2>
        <div class="campaign-box" id="campaigns">
            <!-- Campaigns will be inserted here -->
        </div>
    </section>

    <section>
        <h2>User Engagement</h2>
        <div class="user-box" id="users">
            <!-- Users will be inserted here -->
        </div>
    </section>

    <section>
        <h2>Educational Resources</h2>
        <div class="user-box" id="resources">
            <!-- Resources will be inserted here -->
        </div>
    </section>

    <section>
        <h2>Take the Pledge</h2>
        <div class="pledge-box">
            <input type="text" id="pledge" placeholder="Enter your pledge here">
            <button onclick="addPledge()">Submit Pledge</button>
        </div>
    </section>

    <footer>
        <p>&copy; 2024 Water Conservation Campaign</p>
    </footer>

    <script>
        function fetchData(endpoint, elementId) {{
            fetch(endpoint)
                .then(response => response.json())
                .then(data => {{
                    const container = document.getElementById(elementId);
                    container.innerHTML = '';
                    data.forEach(item => {{
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'item';
                        itemDiv.innerHTML = `
                            <h4>${{item[1]}}</h4>
                            <p>Goal: ${{item[2]}}</p>
                            <p>Progress: ${{item[3]}}</p>
                            <p>Start Date: ${{item[4]}}</p>
                            <p>End Date: ${{item[5]}}</p>
                        `;
                        container.appendChild(itemDiv);
                    }});
                }});
        }}

        function addPledge() {{
            const pledge = document.getElementById('pledge').value;
            const userId = 1;  // For simplicity, assume user ID is 1
            fetch('/add_pledge', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded'
                }},
                body: `user_id=${{userId}}&pledge=${{pledge}}`
            }})
            .then(response => response.json())
            .then(data => {{
                alert(data.status);
                fetchData('/users', 'users');
            }});
        }}

        setInterval(() => fetchData('/campaigns', 'campaigns'), 1000);
        setInterval(() => fetchData('/users', 'users'), 1000);
        setInterval(() => fetchData('/resources', 'resources'), 1000);
    </script>
</body>
</html>
"""

# Save the HTML template
with open('templates/index.html', 'w') as f:
    f.write(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting Water Conservation Campaign...")
    
    # Initialize database with mock data
    initialize_db()
    
    # Start the Flask web server
    app.run(debug=True)
