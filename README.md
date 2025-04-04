
# VehicleSound-AnnoyanceSurveyApp

A web-based application to collect and analyze human perception of vehicle sound annoyance.

## Project Overview

This app allows users to listen to vehicle sounds (car, motorcycle, truck or other), classify them, and rate their loudness(annoyance level). Responses are stored for further analysis.

## Technology Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS
- **Database:** MySQL
- **Data Analysis:** Python (Pandas, NumPy)

## User Roles
- Administrator: 
    - Has complete access to all features and resources.
    - Able to manage users, generate reports, and configure system settings.
- Standard User: 
    - Can access and interact with resources. 
    - Does not have permission to modify configurations or manage other users.

## User Credentials
- Users authenticate using their email address and password.
- Email: Serves as a unique identifier for each user.
- Password: Must be at least ?? characters long.
- The password is securely stored by hashing it with MD5.

## Authentication Process
- Registration: Users create an account by providing their email and setting a password.
- The system ensures the password meets the minimum length of 3 characters and is re-entered correctly to prevent errors.
- Passwords are hashed using MD5 before they are stored in the database for security.
- Login: Users log in by entering their email and password.
- The system validates the email and compares the entered password with the MD5 hashed password stored in the database.
- If the credentials are correct, a session is created to track the user’s activity throughout their session.
## Session Management:
- Upon successful login, a session is initiated to monitor the user's interactions with the application.

## Relational diagram
![alt text](images/relational_schema.png)

## SQL view queries
- CREATE TABLE mm_user (
    UserID INT AUTO_INCREMENT PRIMARY KEY, Fname VARCHAR(50) NOT NULL, Lname VARCHAR(50) NOT NULL, email VARCHAR(50) NOT NULL, role VARCHAR(50) NOT NULL, UserName VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, AccessCode INT NOT NULL, CreatedTime DATETIME NOT NULL) ENGINE=MyISAM;

- CREATE TABLE mm_experiment ( ExperimentID INT AUTO_INCREMENT PRIMARY KEY, ExperimentName VARCHAR(100) NOT NULL,
    StartDate DATETIME NOT NULL, EndDate DATETIME NOT NULL, Description VARCHAR(100) NOT NULL,
    CreatedTime DATETIME NOT NULL, UpdatedDate DATETIME NOT NULL) ENGINE=MyISAM;

- CREATE TABLE mm_media ( MediaID INT AUTO_INCREMENT PRIMARY KEY, FilePath VARCHAR(100) NOT NULL, AutomobileType VARCHAR(50) NOT NULL,
    Duration DATETIME NOT NULL, CreatedTime DATETIME NOT NULL, ExperimentID INT NOT NULL,
    FOREIGN KEY (ExperimentID) REFERENCES mm_experiment(ExperimentID)) ENGINE=MyISAM;

- CREATE TABLE mm_question ( QuestionID INT AUTO_INCREMENT PRIMARY KEY, QuestionText VARCHAR(1000) NOT NULL,
    QuestionType VARCHAR(50) NOT NULL, CreatedTime DATETIME NOT NULL, ExperimentID INT NOT NULL,
    MediaID INT NOT NULL, FOREIGN KEY (ExperimentID) REFERENCES mm_experiment(ExperimentID),
    FOREIGN KEY (MediaID) REFERENCES mm_media(MediaID)) ENGINE=MyISAM;

- CREATE TABLE mm_response ( ResponseID INT AUTO_INCREMENT PRIMARY KEY, Value INT NOT NULL, VehicleGuess VARCHAR(50) NOT NULL,
    CorrectGuess CHAR(1) NOT NULL, CreatedTime DATETIME NOT NULL, Duration DATETIME NOT NULL,
    UserID INT NOT NULL,  QuestionID INT NOT NULL, FOREIGN KEY (UserID) REFERENCES mm_user(UserID),
    FOREIGN KEY (QuestionID) REFERENCES mm_question(QuestionID)) ENGINE=MyISAM;