'''This is the main application. All it really does is run'''
'''This is a demo for a web application that can track medicine usage for a bunch of users
Users contain info like name, gender, age, weight, and perscriptions
'''


# This is flask. It's like apache tomcat for running a web server on localhost
from flask import Flask, session, render_template, request, g, jsonify

# This is the coapthon subscriber module. Use it to GET some data
from coapthon.client.helperclient import HelperClient

# serial writer 
import serial


# This is the module to read from the serial ports
import ArduinoListener

# Set up the serial to listen on the named COM or USB.
# ===============================
# IMPORTANT. Change the name of the Port to be device specific.
# Run the ListPorts.py script to show all the comms ports. Windows is COM3 for me
#=========================


# We will keep these globals around and subscribe later on
host = "127.0.0.1" 
port = 9999





# Create the Flask app
app = Flask(__name__)

# Tear down the application by closing up the database connection 
# We should probably just close the subscribed connection to the server
@app.teardown_appcontext
def close_connection(exception):
  print("App Closing")

 

# Index page endpoint that shows a textbox to subscribe and a button for status
@app.route("/")
def index():
  return render_template("index.html")



# Get the test/ resource from the server then exit.
def subscribe_data(host, port):
  client = HelperClient(server=(host, port))
  response = client.get("/door") # We should make a GET request for the payload
  
  client.stop()

  return response.payload


# Make an alert with the PUT request 
# The Arduino is expecting us to send a response back to scan again
def alert_data(host, port, content):
  client = HelperClient(server=(host,port))
  payload = content
  response = client.put("/door", payload)
  client.stop()


@app.route("/door/alarm", methods=['PUT'])
def alarm_door():
  content = request.get_json(silent=True).get("state") # GEt the state of the door and change the coap request
  print(content)
  alert_data(host,port,content)

  return "Message sent", 200



# Just get the status of the door and jsonify it
@app.route("/door", methods=['GET'])
def get_door():

 



  state = subscribe_data(host, port)

  # If the status is none type just say door is unknown

  if state is None:
    json_data = {'status': 'idk'}
    return jsonify(json_data), 200



  json_data = {'status': state}


  # We got the door data and return 200
  return jsonify(json_data), 200





# Start the ArduinoListener and then start the web app
if __name__ == '__main__':

  
  # We are doing this to give us the ability to write and read from COM4

  app.run(debug = True, use_debugger=True, port = 8080)



