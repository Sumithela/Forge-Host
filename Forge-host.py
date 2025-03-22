import os
import sys
import time
import shutil
import threading

# Step 1: Install required packages
def install_packages():
    try:
        import flask, psutil  
    except ImportError:
        print("Installing required packages...")
        os.system(f"{sys.executable} -m pip install flask psutil")
        import flask, psutil  

install_packages()
import psutil
from flask import Flask, send_from_directory

# Step 2: Create "website" folder if not exists
website_folder = "website"
if not os.path.exists(website_folder):
    os.makedirs(website_folder)

# Step 3: Write the enhanced `index.html` if it doesn't exist
index_html_path = os.path.join(website_folder, "index.html")
if not os.path.exists(index_html_path):
    with open(index_html_path, "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Forge-Host</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100..900&display=swap"
      rel="stylesheet"
    />
    <style>
      * {
        margin: 0;
        padding: 0;
        font-family: Montserrat;
      }
      .container {
        background-color: #17181c;
        height: 100vh;
        width: 100%;
      }
      .container .logo {
        background-color: #23262f;
        height: 80px;
        width: 100%;
        display: flex;
        align-items: center;
      }
      .container .logo h4 {
        color: #fff;
        text-transform: capitalize;
        font-size: 35px;
        margin-left: 40px;
      }
      .container .logo h4 span {
        color: #ff1b1b;
      }
      .container .main {
        width: 100%;
        height: 80vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }
      .container .main h3 {
        color: #fff;
        font-size: 60px;
        text-transform: capitalize;
        margin-bottom: 10px;
      }
      .container .main h3 span {
        color: #ff1b1b;
      }
      .container .main p {
        color: #fff;
        text-transform: capitalize;
        font-size: 30px;
        font-weight: 600;
      }
      .container .main p span{
        color: #5CB85C;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="logo">
        <h4>dev <span>forge</span> .</h4>
      </div>
      <div class="main">
        <h3>forge-<span>host</span></h3>
        <p>status : <span>running</span>.</p>
      </div>
    </div>
  </body>
</html>""")

# Step 4: Set up Flask app
app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory(website_folder, "index.html")

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(website_folder, filename)

# Step 5: Function to monitor CPU & RAM usage
def monitor_system():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        print(f"\rCPU: {cpu_usage}% | RAM: {ram_usage}%", end="")
        time.sleep(2)

# Step 6: Run server and system monitoring in parallel
if __name__ == "__main__":
    threading.Thread(target=monitor_system, daemon=True).start()
    print("\nStarting ForgeHost server at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
