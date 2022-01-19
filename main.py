from bluepy import btle
from time import sleep
import binascii,json
import pika

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
        data = {
            "id": self.DEVICEID,
            "data": [
                {
                    "name": "temp",
                    "value": temp
                },
                {
                    "name": "humid",
                    "value": humid
                },
                {
                    "name": "batt",
                    "value": battery
                },
                {
                    "name": "loc",
                    "value": self.LOC
                }
            ]
        }
        print(json.dumps(data))
        channel.basic_publish(exchange='',
                        routing_key='upload',
                        body=json.dumps(data)
                        )

DEVICEID="xiaomi-01"
LOC=[
        13.7903309,
        100.3770453
    ]

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
except Exception as e:
    print(e)

# Initialisation  -------
address="A4:C1:38:D7:8D:90"
p = btle.Peripheral( )
p.setDelegate( XiaoMiTemp(channel,DEVICEID,LOC) )


try:
    p.connect(address)
    p.waitForNotifications(15.0)
except Exception as e:
    print(e)
finally:
    connection.close()
    p.disconnect()
