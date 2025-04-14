'''
This is the subscriber that will GET from the test/ resource and print the payload.
All it does is connect and GET.
'''
from coapthon.client.helperclient import HelperClient

# Get the test/ resource from the server then exit.
def subscribe_data(host, port):
    client = HelperClient(server=(host, port))
    response = client.get("/door") # We should make a GET request for the payload
    print("Response from server:", response.payload)
    client.stop()

def main():
    host = "127.0.0.1" 
    port = 9999
    subscribe_data(host, port)

if __name__ == '__main__':
    main()
