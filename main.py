from bluepy import btle
import paho.mqtt.client as mqtt
from time import sleep
import binascii

class XiaoMiTemp(btle.DefaultDelegate):
    def __init__(self,client,deviceid,location):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here
        self.client = client
        self.DEVICEID=deviceid
        self.LOC=location

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        databytes=bytearray(data)
        print(binascii.hexlify(databytes))
        temp = int.from_bytes(databytes[0:2],"little")/100
        humid = int.from_bytes(databytes[2:3],"little")
        battery = int.from_bytes(databytes[3:5],"little")/1000
        data1 = "{},location={} temperature={}".format(self.DEVICEID,self.LOC,temp)
        data2 = "{},location={} humidity={}".format(self.DEVICEID,self.LOC,humid)
        data3 = "{},location={} battery={}".format(self.DEVICEID,self.LOC,battery)
        print(data1)
        print(data2)
        print(data3)
        client.publish("sensors/{}".format(DEVICEID),data1)
        client.publish("sensors/{}".format(DEVICEID),data2)
        client.publish("sensors/{}".format(DEVICEID),data3)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

DEVICEID="Xiaomi"
LOC="7736"

client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect("180.180.242.94",1883,60)
except Exception as e:
    print(e)

# Initialisation  -------
address="A4:C1:38:D7:8D:90"
p = btle.Peripheral( )
p.setDelegate( XiaoMiTemp(client,DEVICEID,LOC) )

# start MQTT loop
client.loop_start()

try:
    p.connect(address)
    p.waitForNotifications(15.0)
except Exception as e:
    print(e)
finally:
    client.disconnect()
    p.disconnect()
