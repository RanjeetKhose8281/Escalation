import os
from flask import Flask, request, render_template_string, session, redirect, url_for
import pymysql.cursors
import datetime

app = Flask(__name__)

# Establish MySQL connection
connection = pymysql.connect(
    host='localhost',
    user='RanjeetKhose',
    password='Ranjeet@2025',
    database='pantan',
    cursorclass=pymysql.cursors.DictCursor
)

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define folders relative to the current script directory
log_directory = os.path.join(current_dir, "Daily Escalation Sheet Login Data")
UNC_PATH = os.path.join(current_dir, "Daily Escalation Sheet Data")


def get_current_date():
    return datetime.datetime.now().strftime("%d-%m-%Y")

def authenticate_user(username, password):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM login WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
    except Exception as e:
        print("Error authenticating user:", e)
        return False

def log_login(username):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
   
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file_path = os.path.join(log_directory, f"log_{today_date}.txt")
   
    current_time = datetime.datetime.now().strftime('%Y-%m-%d ^ %H:%M:%S')
   
    log_data = f"{username} ^ {current_time} ^ {request.remote_addr}\n"
    try:
        with open(log_file_path, 'a') as f:
            f.write(log_data)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            log_login(username)  # Log the successful login
            return redirect(url_for('index'))
        else:
            error_message = 'Invalid username or password'
    return render_template_string(login_template, error_message=error_message)

login_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐃𝐚𝐢𝐥𝐲 𝐄𝐬𝐜𝐚𝐥𝐚𝐭𝐢𝐨𝐧 𝐒𝐡𝐞𝐞𝐭</title>
    <link rel="icon" href="https://cdn.oaistatic.com/assets/favicon-miwirzcw.ico" type="image/x-icon">
   
   
    <style>
     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}
body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #1f293a;

}
.container {
    position: relative;
    width: 256px;
    height: 256px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.container span {
    position: absolute;
    left: 0;
    width: 32px;
    height: 6px;
    background: #2c4766;
    border-radius: 8px;
    transform-origin: 128px;
    transform: scale(2.2) rotate(calc(var(--i) * (360deg / 50)));
    animation: animateBlink 3s linear infinite;
    animation-delay: calc(var(--i) * (3s / 50));
}
@keyframes animateBlink {
    0% {
        background: #0ef;
    }
    25% {
        background: #2c4766;
    }
}
.login-box {
    position: absolute;
    width: 400px;
}
.login-box form {
    width: 100%;
    padding: 0 50px;
}
h2 {
    font-size: 2em;
    color: #0ef;
    text-align: center;
}
.input-box {
    position: relative;
    margin: 25px 0;
}
.input-box input {
    width: 100%;
    height: 50px;
    background: transparent;
    border: 2px solid #2c4766;
    outline: none;
    border-radius: 40px;
    font-size: 1em;
    color: #fff;
    padding: 0 20px;
    transition: .5s ease;
}
.input-box input:focus,
.input-box input:valid {
    border-color: #0ef;
}
.input-box label {
    position: absolute;
    top: 50%;
    left: 20px;
    transform: translateY(-50%);
    font-size: 1em;
    color: #fff;
    pointer-events: none;
    transition: .5s ease;
}
.input-box input:focus~label,
.input-box input:valid~label {
    top: 1px;
    font-size: .8em;
    background: #1f293a;
    padding: 0 6px;
    color: #0ef;
}
.forgot-pass {
    margin: -15px 0 10px;
    text-align: center;
}
.forgot-pass a {
    font-size: .85em;
    color: #fff;
    text-decoration: none;
}
.forgot-pass a:hover {
    text-decoration: underline;
}
.btn {
    width: 100%;
    height: 45px;
    background: #0ef;
    border: none;
    outline: none;
    border-radius: 40px;
    cursors: pointer;
    font-size: 1em;
    color: #1f293a;
    font-weight: 600;
}
.signup-link {
    margin: 20px 0 10px;
    text-align: center;
}
.signup-link a {
    font-size: 1em;
    color: #0ef;
    text-decoration: none;
    font-weight: 600;
}
.signup-link a:hover {
    text-decoration: underline;
}

  .error-message {
            color: red;
            text-align: center;
            margin-bottom: 10px;
        }


    </style>
     <script>
      setInterval(function() {
         location.reload();
      }, 30000);  // Refresh every 5 minute
   </script>



  <script>
        
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.shiftKey && event.key === 'I') {
                event.preventDefault();
                alert("Inspect Element is Block by Ranjeet khose");
            }
        });
    </script>

    <script>
    // JavaScript to block right-click (context menu)
    document.addEventListener('contextmenu', function (event) {
      event.preventDefault(); // Prevents the right-click menu from appearing
      alert("Right-click Is Block by Ranjeet khose");
    });
  </script>


 <script>
        
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.key === 'u') {
                event.preventDefault();
                alert("Block by Ranjeet");
            }
        });
    </script>
  
</head>
<body>
    <div class="container">
        <div class="login-box">
            <h2>Login</h2>
            {% if error_message %}
        <p class="error-message">{{ error_message }}</p>
        {% endif %}
            <form method="post" id="loginForm">
                <div class="input-box">
                    <input type="text" name="username" required>
                    <label>Username</label>
                </div>
                <div class="input-box">
                    <input type="password" name="password" required>
                    <label>Password</label>
                </div>
               
                <button type="submit" class="btn" value="Login">Login</button>
               
            </form>
        </div>
        <span style="--i:0;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
        <span style="--i:4;"></span>
        <span style="--i:5;"></span>
        <span style="--i:6;"></span>
        <span style="--i:7;"></span>
        <span style="--i:8;"></span>
        <span style="--i:9;"></span>
        <span style="--i:10;"></span>
        <span style="--i:11;"></span>
        <span style="--i:12;"></span>
        <span style="--i:13;"></span>
        <span style="--i:14;"></span>
        <span style="--i:15;"></span>
        <span style="--i:16;"></span>
        <span style="--i:17;"></span>
        <span style="--i:18;"></span>
        <span style="--i:19;"></span>
        <span style="--i:20;"></span>
        <span style="--i:21;"></span>
        <span style="--i:22;"></span>
        <span style="--i:23;"></span>
        <span style="--i:24;"></span>
        <span style="--i:25;"></span>
        <span style="--i:26;"></span>
        <span style="--i:27;"></span>
        <span style="--i:28;"></span>
        <span style="--i:29;"></span>
        <span style="--i:30;"></span>
        <span style="--i:31;"></span>
        <span style="--i:32;"></span>
        <span style="--i:33;"></span>
        <span style="--i:34;"></span>
        <span style="--i:35;"></span>
        <span style="--i:36;"></span>
        <span style="--i:37;"></span>
        <span style="--i:38;"></span>
        <span style="--i:39;"></span>
        <span style="--i:40;"></span>
        <span style="--i:41;"></span>
        <span style="--i:42;"></span>
        <span style="--i:43;"></span>
        <span style="--i:44;"></span>
        <span style="--i:45;"></span>
        <span style="--i:46;"></span>
        <span style="--i:47;"></span>
        <span style="--i:48;"></span>
        <span style="--i:49;"></span>
    </div>
    <script>
        window.onload = function() {
            var errorMessage = document.querySelector('.error-message');
            if (errorMessage) {
                setTimeout(function() {
                    errorMessage.style.display = 'none';
                }, 5000);
            }
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return '''
        <!DOCTYPE html>
    <html>
    <head>
        <title>Escalation Portal</title>
        <link rel="icon" href="https://cdn.oaistatic.com/assets/favicon-miwirzcw.ico" type="image/x-icon">
        <script src="https://efpage.de/DML/DML_homepage/lib/DML-min.js"></script>
           <style>

              body{

                    background-color:black;
                    font-size: 18px;
                    background-size: cover;
                    background-position: center;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color:#F4C430;
                    height: 100vh; /* Ensure full viewport height */
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-repeat: no-repeat; /* Prevent background image from repeating */

                    }

             .Ranjeet{

                    background-color:none;
                   
                    margin-top: 10px;
                    margin-left: 100px;
                    margin-right: 100px;
                    border: 1px solid #00ccff;
                    height: 550px;
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                 
 
                    }

             .Raje {
                 
                    background-color:none;
                   
                    margin-top: -70px;
                   
                    color:#F4C430;
                    font-size: 25px;
                    font-weight: bold;
                    border: 4px solid #00ccff;
                    margin-left: 30px;
                    margin-right: 30px;
                    height: 323px;



                   }

             .Khose{

                    margin-top: 50px;
                    margin-left: 100px;
                    margin-right:85px
                 


                   }
       
             

            select{
           
                   height: 35px;
                   width: 400px;
                   font-size: 18px;
                   font-weight: bold;
                   cursors:pointer;
                   background-color: #ffffff ;

                    }

             input{
                   
                    height: 25px;
                    width: 400px;
                    font-size: 18px;
                    font-weight: bold;
                    background-color:#ffffff;
                   

                   }

              input[type="submit"] {
               
                    background-color: #00FFFF ;
                    width:550px;
                    color:Black;
                    margin-left:20px;
                    margin-right:80px;
                    cursors: pointer;
                    height:35px
                   }



              input[type="submit"]:hover {
             
                    background-color: crimson;
                    width:550px;
                    color:#00FFFF;
                    margin-left:20px;
                    margin-right:80px;
                    cursors: pointer;
                    height:35px
                    }

             

     

         td, th , tr  {

                    border:3px solid #00ccff ;
                    align-items: center;
                    text-align: center;

                    width: 350px;
                    padding: 8px;
                    color:#00FFFF ;

                    }


       #clockContainer {
                    position: relative;
                    width: 100px; /* Adjust as needed */
                    height: 100px; /* Adjust as needed */
                    margin: 0 auto; /* Center horizontally */
                    border: 3px solid #282828;
                    border-radius: 50%;
                    background-image: url('https://static.vecteezy.com/system/resources/previews/000/549/810/original/vector-abstract-technology-background-technology-digital-world-of-business-information-futuristic-blue-virtual-graphic-interface.jpg');
                    overflow: hidden;
                    margin-top: -70px;
                    margin-right: 20px;
                    }

          </style>

          <style>
           /* Scrolling message */
        .marquee-container {
            position: fixed;
            bottom: -8px;
            right: 0;
            width: 100%;
            text-align: center;
            overflow: hidden;
        }

        .marquee {
            display: inline-block;
            white-space: nowrap;
            animation: marqueeAnimation 10s linear infinite;
            font-size: 13px;
            color: #00FFFF;
        }

        @keyframes marqueeAnimation {
            0% {
                transform: translateX(100%);
            }
            100% {
                transform: translateX(-100%);
            }
        }
          </style>





  <script>
        
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.shiftKey && event.key === 'I') {
                event.preventDefault();
                alert("Inspect Element is Block by Ranjeet Khose");
            }
        });
    </script>

    <script>
    // JavaScript to block right-click (context menu)
    document.addEventListener('contextmenu', function (event) {
      event.preventDefault(); // Prevents the right-click menu from appearing
      alert("Right-click Is Block by Ranjeet khose");
    });
  </script>


 <script>
        
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.key === 'u') {
                event.preventDefault();
                alert("Block by Ranjeet khose");
            }
        });
    </script>
  
   


         </head>
           <body>
       
               <div class="Ranjeet">
         
             
             <center><h1><b style="color:#00FFFF;">Daily Escalation Sheet  © </b></h1></center><br>
             <div id="clockContainer"></div>

             <marquee id="Heading" direction="left" style="color:#00FFFF ; margin-right:122px; margin-left:140px;  onmouseover="this.stop();" onmouseout="this.start();" >
            <h2>Welcome, ''' + username + '''!</h2>
             </marquee>
               
                    <script>
                            "use strict";
                            let cx = 50, cy = 50; // Reduced radius for smaller size
                            const _clockstyle = "width: " + (2 * cx) + "px;  height: " + (2 * cy) + "px;"
                            + "border-radius: 50%;"
                            + "box-shadow: -2px -2px 5px rgba(67,67,67,0.5), inset 2px 2px 5px rgba(0,0,0,0.5),"
                            + "inset -2px -2px 5px rgba(67,67,67,0.5), 2px 2px 5px rgba(0,0,0,0.3);";

                            // Create clock container div with specified style
                            const clockContainer = document.getElementById("clockContainer");

                            // Function to draw clock ticks and hands
                            function drawClock() {
                            // Get canvas context
                            const canvas = document.createElement("canvas");
                            canvas.width = 2 * cx;
                            canvas.height = 2 * cy;
                            const ctx = canvas.getContext("2d");
                            ctx.lineCap = "round";

                            // Function to draw tick marks
                            function tick(color, width, angle, length, innerlength = 0) {
                            function ls(length) { return length * Math.sin(angle / 180.0 * Math.PI) }
                            function lc(length) { return -length * Math.cos(angle / 180.0 * Math.PI) }
                            ctx.strokeStyle = color;
                            ctx.lineWidth = width;
                            ctx.beginPath();
                            ctx.moveTo(cx + ls(innerlength), cy + lc(innerlength));
                            ctx.lineTo(cx + ls(length), cy + lc(length));
                            ctx.stroke();
                            }

                            // Draw ticks
                            for (let i = 0; i < 360; i += 30) {
                            if ((i % 90) == 0) tick("#00FFFF", 6, i, 38, 35); // Hour ticks
                            else tick("#7FFFD4", 3, i, 38, 35); // Minute ticks
                            }

                            // Get current time
                            const t = new Date();
                            // Draw hands
                            tick("Darkred", 3, t.getHours() * 30, 30); // Hour hand
                            tick("red", 1, t.getMinutes() * 6, 40); // Minute hand
                            tick("LightBlue", 1, t.getSeconds() * 6, 45); // Second hand

                            // Draw center
                            ctx.fillStyle = "#00FFFF";
                            ctx.beginPath();
                            ctx.arc(cx, cy, 6, 0, 2 * Math.PI);
                            ctx.fill();
       
                            // Append canvas to clock container div
                            clockContainer.innerHTML = '';
                            clockContainer.appendChild(canvas);
                            }

                            // Initial draw
                            drawClock();
                            setInterval(drawClock, 1000); // Update every second
                  </script>
                       


                     <div class="Raje">
                       

                         <div class="Khose">
     

                           <form   method="post" action="/submit">


                            <table>

                       

                              <tr>
                                   <td><label for="Acknowledge_Number"> Acknowledgement  Number</label> </td>
                                   <td> <input type="text" id="Acknowledge_Number" name="Acknowledge_Number" maxlength="15"  pattern="[0-9]{14,15}"    title="Enter the Valid Ack Number"/  required  autocomplete="off"><br>
                                       
                                   
                                 </td>
                              </tr>

                                 

                              <tr>
                 

                                   <td> <label for="Remark">Remark </label>  </td>
                                   <td>  
                             
                                   <select name="Remark" id="Remark">
                             
                              <option value="">Select </option>
                              <option value="Appreciation Call">Appreciation Call (Mention Contact# in Agent Remark)  </option>
                              <option value="Pending With ITD Greater Than 7 Days">Pending With ITD Greater Then  7 Days </option>
                              <option value="Logistics Issue - All issues related to Logistics TAB">Logistics issue -All  issuess related  to Logistics TAB </option>
                              <option value="Valid Document  - Escalate to Process">Valid Document  - Escalate to Process</option>
                              <option value="Assisted Application - PSVR Blank">Assisted Application - PSVR Blank </option>
                              <option value="Online Application  - PSVR Blank">Online Application  - PSVR Blank  </option>
                              <option value="Language  Case (Other  Language  Document)">Language  Case (Other  Language  Document) </option>
                              <option value="Online Case - Pending for Processing > 3 Days"> Online Case - Pending for Processing > 3 Days</option>
                              <option value="Annexure  Case - Pending for Processing > 3 Days"> Annexure  Case - Pending for Processing > 3 Days </option>
                              <option value="Email Revert To Be Sent Urgent -Req ID"> Email Revert To Be Sent Urgent -Req ID </option>
                              <option value="Email Docs Not Uploaded  - Req ID ">Email Docs Not Uploaded  - Req ID  </option>
                              <option value="PAN/TAN Sync Issue/PAN/TAN Showing Invalid - PAN/TAN Alloted >3 Days">PAN/TAN Sync Issue/PAN/TAN Showing Invalid - PAN/TAN Alloted >3 Days</option>
                              <option value="Same PAN/TAN Alloted">Same PAN/TAN Alloted</option>
                              <option value="Refund Not Received - Only if application Failed > 7 Days">Refund Not Received - Only if application Failed > 7 Days</option>
                              <option value="Reprint Request Pending From Long Time">Reprint Request Pending From Long Time</option>
                              <option value="Discrepancy Letter Not Generated">Discrepancy Letter Not Generated</option>
                              <option value="E- PAN / E- TAN Not Received">E- PAN / E- TAN Not Received</option>
                              <option value="Docs Adjustment Request">Docs Adjustment Request</option>
                              <option value="Digitization Error - Offline Cases">Digitization Error - Offline Cases</option>
                              <option value="Not Uploaded - Offline Cases">Not Uploaded - Offline Cases</option>
                              <option value="Discrepancy Resolved But Status Not Changed">Discrepancy Resolved But Status Not Changed</option>
                              <option value="Docs Not Received - POD Available (Post / Courier)">Docs Not Received - POD Available (Post / Courier)</option>
                              <option value="Payment Adjustment (PNR)">Payment Adjustment (PNR)</option>
                              <option value="Payment Not Received (PNR)">Payment Not Received (PNR)</option>
                              <option value="49 A Required (49A Offline Ack Number)">49 A Required (49A Offline Ack Number)</option>
                              <option value="Wrong Processing of CR Application By Protean">Wrong Processing of CR Application By Protean</option>
                              <option value="Wrong processing of Online application By Protean">Wrong processing of Online application By Protean</option>
                             
                             

                                </select><br>
                       
                                   </td>

                             </tr>

               

                             <tr>
                 
                                   <td>  <label for="Agent_Remark"> Agent Remark</label> </td>
                                   <td>   <input type="text" id="Agent_Remark" name="Agent_Remark" required autocomplete="off"><br></td>

                             </tr>




                               <tr>

                                    <td colspan=2>    <center> <input type="submit" value="Submit"></center></td>

                                   
                               </tr>

                               <tr style="border:none">

                                    <td colspan=2 style="border:none ; color :red"> <center id="message"> </center></td>

                                   
                               </tr>

           
                             </table>
                             
                             
                             
                          </form>
                        </div>
                          <marquee id="Heading" direction="left" style="color:#00FFFF ; margin-right:2px; margin-left:1px;  onmouseover="this.stop();" onmouseout="this.start();" >
                        <h3>If Ack Num not present ,  Enter 15 Digits as 8 </h3>
                        </marquee>
                    </div>
                  </div>

                  <script>
                            document.querySelector('form').addEventListener('submit', async (event) => {
                            event.preventDefault();
                            const formData = new FormData(event.target);
                            const response = await fetch('/submit', {
                            method: 'POST',
                            body: formData
                           });


                           const result = await response.text();
                           document.getElementById('message').textContent = result;
       
       
                            event.target.reset();
       
     
                          setTimeout(() => {
                          location.reload();
                            }, 1000);
                           });
                 </script>
<script>
    // Auto logout after a specified number of minutes of inactivity
    var logoutTimer;

    function resetLogoutTimer() {
        clearTimeout(logoutTimer);
        // Set the timeout to 30 minutes
        var minutes = 30;
        logoutTimer = setTimeout(function() {
            window.location.href = '/logout'; // Redirect to logout page
        }, minutes * 60000); // 1 minute = 60000 ms
    }

    function updateDateInput() {
        var input = document.getElementById("date");
        var today = new Date().toISOString().split("T")[0];
        input.value = today;
    }

    window.onload = function() {
        resetLogoutTimer();
        updateDateInput();
        document.getElementById('myForm').addEventListener('submit', function(event) {
            var dateInput = document.getElementById('date').value;
            if (!dateInput) {
                alert('Please select a date.');
                event.preventDefault();
            }
        });
    }

    // Detects user activity to reset the logout timer
    document.addEventListener('mousemove', resetLogoutTimer);
    document.addEventListener('keydown', resetLogoutTimer);

    // If the user gets logged out, refresh the page and redirect to login
    window.addEventListener('load', function() {
        if (window.location.pathname === '/logout') {
            setTimeout(function() {
                window.location.href = '/login'; // Redirect to login page after logout
            }, 1000); // Wait 1 second before redirecting to login
        }
    });
</script>

              <div class="marquee-container">
                <div class="marquee">
                    <p>Developed by Ranjeet Khose</p>
                </div>
            </div>

             </body>
          </html>
        '''
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit_data():
    if 'username' in session:
        username = session['username']
        current_date = get_current_date()
        current_datetime = datetime.datetime.now().strftime("%d-%m-%Y^%H:%M:%S")
        Acknowledge_Number = request.form.get('Acknowledge_Number')
        Remark = request.form.get('Remark')
        Agent_Remark = request.form.get('Agent_Remark')

        if Acknowledge_Number and Remark and Agent_Remark:
            date_directory = os.path.join(UNC_PATH, current_date)
            if not os.path.exists(date_directory):
                os.makedirs(date_directory)

            filename = f"{current_date}.txt"
            file_path = os.path.join(date_directory, filename)
           
            # Check if file exists; if not, write title row
            write_title_row = not os.path.exists(file_path)
           
            with open(file_path, 'a') as file:
                if write_title_row:
                    file.write("Agent Name^Date^Time^Acknowledge Number^Remark^Agent Remark\n")
               
                file.write(f"{username}^{current_datetime}^{Acknowledge_Number}^{Remark}^{Agent_Remark}\n")
           
            return 'Data submitted successfully'
        else:
            return 'Incomplete form submission'
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True, host='0.0.0.0', port=5000)
