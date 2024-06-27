from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    # Create tables if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            email TEXT UNIQUE,  -- Make email column unique
            age INTEGER,
            gender TEXT,
            profile_image TEXT,
            selected_pattern TEXT,
            status INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the database
initialize_db()

# Routes
# ... (Your existing routes)
@app.route('/')
def index():
    return render_template('admin/index.html')

@app.route('/home')
def home():
     conn = sqlite3.connect('database/database.sqlite')
     cursor = conn.cursor()
     cursor.execute('SELECT * FROM users WHERE status IS NULL')
     users_data = cursor.fetchall()
     print("user_data",users_data)
     conn.close()
     return render_template('admindashboard/index.html',users_data=users_data)
 
 
 
@app.route('/accepteduser')
def accepteduser():
     conn = sqlite3.connect('database/database.sqlite')
     cursor = conn.cursor()
     cursor.execute('SELECT * FROM users WHERE status = 1')
     users_data = cursor.fetchall()
     print("user_data",users_data)
     conn.close()
     return render_template('admindashboard/accepteduser.html',users_data=users_data)
 
@app.route('/rejecteduser')
def rejecteduser():
     conn = sqlite3.connect('database/database.sqlite')
     cursor = conn.cursor()
     cursor.execute('SELECT * FROM users WHERE status = 0')
     users_data = cursor.fetchall()
     print("user_data",users_data)
     conn.close()
     return render_template('admindashboard/rejecteduser.html',users_data=users_data)
 
 

@app.route('/update_status/<int:user_id>', methods=['POST'])
def update_status(user_id):
    if request.method == 'POST':
        if 'accept' in request.form:
            new_status = 1
        elif 'reject' in request.form:
            new_status = 0

        # Update status in the database
        conn = sqlite3.connect('database/database.sqlite')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET status = ? WHERE id = ?', (new_status, user_id))
        conn.commit()
        conn.close()

    return redirect(url_for('home'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Handle registration logic here
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        
        con=sqlite3.connect("database/database.sqlite")
        cur=con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            error_message = "Email is already registered registered. Please sign up."
            return render_template('register.html',error_message=error_message)
        
        cur.execute("insert into users( first_name,last_name, phone_number, email, age, gender) values (?,?,?,?,?,?)",(first_name,last_name,phone_number,email,age,gender))
        user_id=cur.lastrowid
        con.commit()
        flash('User Added','success')
        
        

        return redirect(url_for('select_image', user_id=user_id))

    return render_template('register.html')




@app.route('/updateuser/<int:user_id>', methods=['GET', 'POST'])
def updateuser(user_id):
    con = sqlite3.connect("database/database.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user_data = cur.fetchone()
    
    if request.method == 'POST':
        # Handle form submission
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        
        cur.execute("UPDATE users SET first_name=?, last_name=?, phone_number=?, email=?, age=?, gender=? WHERE id=?", (first_name, last_name, phone_number, email, age, gender, user_id))
        con.commit()
        con.close()

        # Redirect to user profile page after update
        return redirect(url_for('user_profile'))

    return render_template('updateuser.html', user_data=user_data)






@app.route('/select_image', methods=['GET'])
def select_image():
    return render_template('select_image.html')

@app.route('/selected_pattern', methods=['GET', 'POST'])
def selected_pattern():
    image_name = request.args.get('image')
    user_id = request.args.get('user_id')
    
    if request.method == 'POST':
        
        user_id = request.args.get('user_id') 
        
        if user_id:
            # Get selected pattern data from the request
            selected_data = request.json.get('selectedData')
            image_name = request.json.get('image')
            print(image_name)

            # Update selected pattern data in the user's record
            update_selected_pattern_data(user_id, selected_data,image_name)

            ## error return redirect(url_for('login'))
            return jsonify({'success': True})
        
        

    
  
    return render_template('selected_pattern.html', img=image_name,user_id=user_id)



def update_selected_pattern_data(user_id, selected_data,image_name):
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()
    print("image_name",image_name)
    # Update the selected pattern data in the user's record
    cursor.execute('UPDATE users SET selected_pattern = ?,profile_image= ?  WHERE id = ?', (selected_data,image_name, user_id))

    conn.commit()
    conn.close()
    return redirect(url_for('login'))





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        email = request.form.get('email')
       # password = request.form.get('password')  # You need to handle password securely, consider hashing.
        if email == 'admin@gmail.com':
            print('hallo')
            # return render_template('admin/index.html')
            return redirect(url_for('home'))
        conn = sqlite3.connect('database/database.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND status = ?', (email, 1))
        account=cur.fetchone()
        
        ##cur = mysql.connection.cursor()
        ##cur.execute('SELECT * FROM user WHERE email= %s',(email,)) 
        
        #user_id=account[0]
        print(account)
        if account: 
            user_id=account[0]
            return redirect(url_for('login_select_image',email=email, user_id=user_id))
        else:
            error_message = "Email is not registered or admin is not approved. Please sign up."
            return render_template('login.html', error_message=error_message)
        
        
        
        

    return render_template('login.html')







@app.route('/resetpasslogin', methods=['GET', 'POST'])
def resetpasslogin():
    if request.method == 'POST':
        # Handle login logic here
        email = request.form.get('email')
       # password = request.form.get('password')  # You need to handle password securely, consider hashing.
        conn = sqlite3.connect('database/database.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ?', (email,))
        account=cur.fetchone()
        
        ##cur = mysql.connection.cursor()
        ##cur.execute('SELECT * FROM user WHERE email= %s',(email,)) 
        
        user_id=account[0]
        print(account)
        if account: 
            return redirect(url_for('restlogin_select_image',email=email, user_id=user_id))
        

    return render_template('resetpasswordlogin.html')






@app.route('/login_select_image', methods=['GET', 'POST'])
def login_select_image():
    
    
    #if request.method == 'POST':
        # Handle image selection logic for login here
       # return redirect(url_for('login_selected_pattern'))

    return render_template('login_select_image.html')



@app.route('/restlogin_select_image', methods=['GET', 'POST'])
def restlogin_select_image():
    
    
    #if request.method == 'POST':
        # Handle image selection logic for login here
       # return redirect(url_for('login_selected_pattern'))

    return render_template('restlogin_select_image.html')



@app.route('/login_selected_pattern', methods=['GET', 'POST'])
def login_selected_pattern():
    image_name = request.args.get('image')
    # print(image_name)
    email = request.args.get('email')
    # print(email)
    user_id = request.args.get('user_id')
    
    if request.method == 'POST':
        # Handle pattern selection logic for login here
        selected_data = request.json.get('selectedData')
        image_name = request.json.get('image')
        email = request.json.get('email')
        user_id = request.json.get('user_id')
        
        # print(user_id)
        # print(email)

        # Fetch user data from the database based on the email
        conn = sqlite3.connect('database/database.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND id = ?', (email, user_id,))

        user_data = cur.fetchone()
        print(user_data[7])
        print(user_data[8])
         
        if user_data:
            print(image_name)
            print(selected_data)
            # Check if the selected image name, and pattern match the user's data
            if str(user_data[7]) == str(image_name) and str(user_data[8]) == str(selected_data):
                session['email'] = user_data[4]
                #return jsonify(user_data)
                return jsonify({'success': True, 'data': user_data})
                # If matched, redirect to the user profile page
                # return redirect(url_for('user_profile'))
            else:
                  return jsonify({'error': 'Invalid pattern or image'})
            
    return render_template('login_selected_pattern.html', img=image_name, email=email, user_id=user_id)



@app.route('/resetlogin_selected_pattern', methods=['GET', 'POST'])
def resetlogin_selected_pattern():
    image_name = request.args.get('image')
    # print(image_name)
    email = request.args.get('email')
    # print(email)
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    
    if request.method == 'POST':
        # Handle pattern selection logic for login here
        selected_data = request.json.get('selectedData')
        image_name = request.json.get('image')
        email = request.json.get('email')
        user_id = request.json.get('user_id')
        
        # print(user_id)
        # print(email)

        # Fetch user data from the database based on the email
        conn = sqlite3.connect('database/database.sqlite')
        cur = conn.cursor()
        cur.execute('UPDATE users SET selected_pattern = ?, profile_image = ? WHERE email = ? AND id = ?',
                       (selected_data, image_name, email, user_id))
        conn.commit()
        

        # Return a success response
        return jsonify({'success': True, 'message': 'Pattern and image updated successfully.'})

         
    return render_template('resetlogin_selected_pattern.html', img=image_name, email=email, user_id=user_id)


@app.route('/user_profile')
def user_profile():
    # Retrieve user profile information from the database using the session email
    
    email = session.get('email')
    print("email",email)
    
    
    # Fetch user data from the database based on the email
    conn = sqlite3.connect('database/database.sqlite')
    cur = conn.cursor()
    a=cur.execute('SELECT id,first_name, last_name, phone_number, gender, age FROM users WHERE email = ?', (email,))
    
    user_profile_info = cur.fetchone()
    print(user_profile_info)

    conn.close()

    # Use the retrieved user profile information in the template
    return render_template('user_profile.html', user_profile_info=user_profile_info)





# @app.route('/user_profile')
# def user_profile():
#     # Retrieve user profile information from the database using the session email
#     email = session.get('email')
#     # Use the email to fetch the user's information from the database and pass it to the template

#     return render_template('user_profile.html', user_profile_info=user_profile_info)

@app.route('/logout')
def logout():
    # Handle logout logic, clear session, and redirect to the home page
    session.clear()
    return redirect(url_for('index'))









# def get_user_id_by_email(email):
#     conn = sqlite3.connect('database/database.db')
#     cursor = conn.cursor()

#     cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
#     user_id = cursor.fetchone()

#     conn.close()

#     return user_id[0] if user_id else None



# def update_selected_pattern_data(user_id, selected_data,image_name):
#     conn = sqlite3.connect('database/database.sqlite')
#     cursor = conn.cursor()
#     print("image_name",image_name)
#     # Update the selected pattern data in the user's record
#     cursor.execute('UPDATE users SET selected_pattern = ?,profile_image= ?  WHERE id = ?', (selected_data,image_name, user_id))

#     conn.commit()
#     conn.close()
#     return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
