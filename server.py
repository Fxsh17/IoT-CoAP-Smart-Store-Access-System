from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
unicode = str()
total=0 
max_customers=5
current_customers=0
class StoreResource(Resource):
    def __init__(self, name="StoreResource", coap_server=None):
        super(StoreResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = name
        self.resource_type = "rtf1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_PUT(self, request):
        # Handle sensor triggers
        global total
        global max_customers
        global current_customers
        sensor_action = request.payload
        if sensor_action == "enter":
            if current_customers < max_customers:
                total+=1  
                current_customers += 1
                response_payload = "True"
            else:
                response_payload = "False"
        elif sensor_action == "exit":
            if current_customers > 0:
                current_customers -= 1
                response_payload = "Exit"
        self.payload = response_payload.encode('utf-8')  
        print("The total number of entrants: ", total)
        print("Customers in the store: ", current_customers)
        print("Remaining entries: ", 5 - current_customers)
        return self

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('sensor1', StoreResource('sensor1'))
        self.add_resource('sensor2', StoreResource('Sensor2'))

   
           
def main():
    server = CoAPServer("172.20.10.7", 5683)
    print(" Start")
  
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    main()