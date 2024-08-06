# Building API endpoints with Flask:

## Description:
This project is a Flask-based web application that provides user authentication and administration functionality. The application allows users to register, log in, and manage their profiles, while administrators can manage user accounts. The project integrates with PostgreSQL for data storage and uses JWT for secure authentication. It also includes features for password reset via email and provides API documentation through Swagger for easy exploration and testing of the endpoints.

## Requirements:

1.Python 3.x

2.PostgreSQL

## Project Structure:

Flask_project/ 
├── app.py 
├── admin_routes.py 
├── models.py  
├── auth_routes.py 
├── user_routes.py  
└── utils.py  
├── config.py 
└── requirements.txt

## Installation and run the project:

1. git clone 'repository-url'

2. cd 'project-directory'

3. python3 -m venv venv(For ubuntu)
   
4. Activating the Virtual Environment
   
   -> On Windows: venv\Scripts\activate
   
   -> On Mac/Linux: source venv/bin/activate

6. Install dependencies:

   pip install -r requirements.txt


## Configuration:
 In the config file of the project make your database set up and JWT Secret Key in the following format:

 SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:PORT(Default:5432)/database_name'

 JWT_SECRET_KEY=your_secret_key

*** While Testing API in AUTHENTICATION TOKEN Make Sure to put Bearer before placing the token

 ## Database Set Up:

 1. Ensure PostgreSQL is running.
 2. createdb database_name

## Running the server:

1. python app.py
2. The server should now be running at http://localhost:5000.

## API Documentation
1. Access the Swagger UI at 'http://localhost:5000/swagger/' endpoint after starting the server.
2. Explore and test the API endpoints using the Swagger documentation.

## Usage
1. Register a User:

   -> Endpoint: POST /register
   
   -> Provide required parameters (username, first_name, last_name, password, email).
   
3. Login:

   -> Endpoint: POST /login
   
   -> Provide username and password to receive an access token.
   
3. Retrieve User Profile:

    -> Endpoint: GET /user
   
    -> Requires JWT token in the Authorization header.
   
4. Update User Profile:

    -> Endpoint: PUT /user
   
    -> Requires JWT token and allows updating first_name, last_name, email.
5. Forgot Password:

    -> Endpoint: POST /forgot-password
   
    -> Provide email to receive a password reset link.
7. Reset Password:

     -> Endpoint: POST /reset-password/<token>
     
     -> Provide password along with the token received via email to reset the password.
8. Admin Operations:

     -> Admins can manage users (GET, PUT, DELETE) via /admin/users and /admin/users/<user_id> endpoints.
   
     -> Requires admin privileges and JWT token.


