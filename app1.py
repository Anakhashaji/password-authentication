from flask import Flask, render_template

app = Flask(__name__)

# Configuring the static files (CSS, JS, images, etc.)
app.static_folder = 'static'

@app.route('/')
def index():
    # Render the HTML template
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
