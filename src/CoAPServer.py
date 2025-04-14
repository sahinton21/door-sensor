'''
This server creates the /test resource and manages various requests.
The TestResource is a class that has the GET and PUT methods along with a constructor.

The CoAPServer is the server that runs and uses the test/ resource.

We just loop and listen for connections.
'''
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

# This is the resoucre info for test/. It constructs with an empty payload and needs the publisher to change info
class TestResource(Resource):
    def __init__(self, name="TestResource", coap_server=None):
        super(TestResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "IDK"
        self.resource_type = "rt1"
        self.content_type = "text/plain"

    # Return the payload of the message to the subscriber
    def render_GET(self, request):
        return self
    # Get the message from the request
    def render_PUT(self, request):
        self.payload = request.payload

# Initialize the test/ resoure on the specified port and IP
class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('/door', TestResource())

# Start the server on localhost port 9999
def main():
    server = CoAPServer("127.0.0.1", 9999)
    try:
        server.listen(10)  
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        

if __name__ == '__main__':
    main()
