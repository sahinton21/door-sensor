'''
This is the publisher that will make a PUT request to the test/ resource.
Its payload will replace the data at that resource.
'''
from coapthon.client.helperclient import HelperClient

# Connect to the server at port 9999 on localhost and publish some input data
def publish_data(host, port):
    client = HelperClient(server=(host, port))
    
    payload = input("Enter the info you want published:\n")
    client.put("/door", payload)
    print("Published data:", payload)
    client.stop()

def main():
    host = "127.0.0.1" 
    port = 9999         
    publish_data(host, port)

if __name__ == '__main__':
    main()
