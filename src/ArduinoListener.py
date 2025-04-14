'''
This is the listener. We need to listen to a serial port and print out some stuff
On a door open signal <OPEN> or <CLOSED> we should send a CoAPPPublisher PUT request
'''

# This is the coapthon publisher module to PUT data
from coapthon.client.helperclient import HelperClient

# This is the module to read from the serial ports
import serial

# Set up the serial to listen on the named COM or USB.
# ===============================
# IMPORTANT. Change the name of the Port to be device specific.
# Run the ListPorts.py script to show all the comms ports. Windows is COM3 for me
#=========================
port = 'COM4'




serialPort = None
def set_serial():
  serialPort = serial.Serial(port, 9600, timeout=5)
  return serialPort

# Make a CoAP PUT request
#==========================================
# The CoAP serer must be running for this to work
def publish_content(content):
  client = HelperClient(server=("127.0.0.1", 9999))


  # Get the previous content to send to the Arduino
  prev = client.get("/door")


  client.put("/door", content)

  client.stop()

  return prev



# Entry point
if __name__ == "__main__":
  serialPort = set_serial()

  # Now write out what we see
  message = serialPort.readline()

  print(message)

  message = serialPort.readline().decode().strip()
  content = message.split('<')[1].split('>')[0]
  publish_content(content)


  # We are ready to receive input now

  # We should probably just run a while loop and keep reading
  try:
    while True and serialPort:
      message = serialPort.readline().decode().strip()

      # Only do something on a reception of something
      if message:
        #print(message)


      # Now that we have recieved a message we have to do something
      
      # Make a CoAP PUT request on the state changes
      # Strip the message by trimming out the stuff between the <>
      # Use a split operation to get out the <>
      # Maybe in the future more information is passed but for now it will just be the one message

      # remove the initial < and get the remaining strip. Then remove that closing > and grab the string within
        content = message.split('<')[1].split('>')[0]
        print(content)

        # Get the coap resource's contents first before updating

        prev = publish_content(content)

        # Now ACK the message from the Arduino or send some data
        # We will respond with the previous resource from the /door endpoint
        # If it is an <Alert> we will have to do something on the Arduino device


        prev = '<' + prev.payload + '>'
        serialPort.write(prev.encode('utf-8'))

      # Now make a CoAP request on OPEN or CLOSED




  except KeyboardInterrupt:
    serialPort.close()