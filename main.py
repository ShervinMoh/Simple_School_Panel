from flask import Flask, render_template , request
import json

app = Flask(__name__)

'''User class for save datas into JSON file'''
class User:
    def __init__(self, username, password, job):
        self.username = username
        self.password = password
        self.job = job
    
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'job': self.job
        }

# main page
@app.route('/')
def main_page():
    return render_template('index.html')

# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get the user input from the form
        username = request.form['username']
        password = request.form['password']
        job = request.form['job']
        
        # load existing user data from the JSON file
        with open('user_data.json', 'r') as f:
            existing_data = json.load(f)
        
        # check if the username already exists in the JSON file
        for user_data in existing_data:
            if user_data['username'] == username:
                return 'Username already exists'
            # check input job
            if user_data['job'] != 'student' or user_data['job'] != 'teacher' :
                return 'You must be a Student or Teacher to sign up'
        # create a User object with the input data
        user = User(username, password, job)
        
        # add the new user data to the existing data
        existing_data.append(user.to_dict())
        
        # write the updated data to the JSON file
        with open('user_data.json', 'w') as f:
            json.dump(existing_data, f) 
        # code to handle sign up logic using the user input  
        return 'Sign up successful'
    
    else:
        # render the signup page with input bars for username, password, and job
        return render_template('signup.html')
    
# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the user input from the form
        username = request.form['username']
        password = request.form['password']
        
        # load existing user data from the JSON file
        with open('user_data.json', 'r') as f:
            existing_data = json.load(f)
        
        # check if the username exists in the JSON file
        for user_data in existing_data:
            if user_data['username'] == username:
                # check if the password is correct
                if user_data['password'] == password:
                    # check users job
                    if user_data['job'] == 'student':
                        return 'Welocome to Student panel'
                    elif user_data['job'] == 'teacher':
                        return 'Welcome to Teacher panel'
                else:
                    return 'Incorrect password'
        # if the username doesn't exist in the JSON file
        return 'Username not found'
    else:
        # render the login page with input bars for username and password
        return render_template('login.html')

if __name__ == '__main__':
    app.run()