Project Title:
Daily Escalation Sheet Web Application

Description:
This project is a Flask-based web application designed to manage and log daily escalation reports for a business process (such as PAN/TAN application escalations). It provides a secure user login system connected to a MySQL database for user authentication. Upon successful login, users can submit escalation details such as Acknowledgment Number, Remark, and Agent Remark, which are stored in a file system organized by date.

Key features include:

User Authentication: Secure login system verifying credentials against a MySQL database (pantan database, login table).

Login Logging: Successful logins are recorded along with the username, timestamp, and IP address in a structured file format.

Daily Data Collection:

Escalation entries (acknowledgment number, selected remark, agent remark) are saved into daily text files inside a UNC-specified folder structure (C:\InfoVortex\Daily Escalation Sheet Data).

Each day's data is stored in a new folder named by date.

Frontend:

A custom-designed responsive login page with user-friendly animations and security features like disabling right-click and inspect element.

A clean and interactive submission form for escalation data after login.

Security Measures:

Session-based login management.

Auto logout after 30 minutes of inactivity.

Frontend restrictions on context menus, viewing page source (Ctrl+U), and developer tools (Ctrl+Shift+I).

File Organization:

Creates daily logs in specific directories.

Adds headers to files if not present.

Credits:
Developed by Ranjeet Khose & Prasad Phadnis.

Technologies Used:
Backend: Python (Flask), pymysql

Frontend: HTML, CSS (Poppins font and animations), JavaScript

Database: MySQL

Hosting: Localhost, but ready to deploy on Linux servers as well

File Storage: Windows UNC path structure
