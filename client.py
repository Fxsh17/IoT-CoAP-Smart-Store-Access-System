import microcoapy
import _thread
import time
from machine import Pin
import network
from machine import Pin, ADC
from neopixel import NeoPixel
PbA= Pin(4, Pin.IN)
PbB= Pin(5, Pin.IN)
led = Pin(48, Pin.OUT)             						# set GPIO48  to output to drive NeoPixel

neo = NeoPixel(led, 1) # create NeoPixel driver on GPIO48 for 1 pixel
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Faisal’s iPhone", "Faisal2001")
station.isconnected()
station.ifconfig()
neo[0] = (255, 0, 0) 
neo.write()  

def receivedMessageCallback(packet, sender):
    server_response = packet.payload.decode('utf-8')
    print('Message payload:', server_response)
    if server_response == "True":  
        neo[0] = (0, 255, 0)  # Green light
        neo.write()

def trigger_sensor(sensor_type,action):
    neo[0] = (255, 0, 0) 
    neo.write() 
    client = microcoapy.Coap()
    client.responseCallback = receivedMessageCallback
    client.start()

    _SERVER_IP = "172.20.10.7"
    _SERVER_PORT = 5683
    resource_path = "sensor" + sensor_type 
    if action=="A":
        payload= "enter"
    else:
        payload="exit"
    bytesTransferred = client.put(_SERVER_IP, _SERVER_PORT, resource_path, payload)
    print(f"[{sensor_type.upper()}] Sent bytes: ", bytesTransferred)
    client.poll(3000)  
   
    client.stop()
def sensor1():
    while True:
        if PbA.value()== 1:
            action= "A"
            print("A")
            trigger_sensor("1","A")
        time.sleep(1)  




def sensor2():
    while True:
        if PbB.value()== 1:
            print("B")
            neo[0] = (0, 255, 0) # set the first pixel to white
            neo.write()
            time.sleep(1)  
            trigger_sensor("2","B")
        time.sleep(1)  


# Start the sensor threads
_thread.start_new_thread(sensor1, ())
_thread.start_new_thread(sensor2, ())

# Keep the main thread alive
while True:
    time.sleep(10)
