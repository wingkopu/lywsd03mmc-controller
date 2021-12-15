from bluepy import btle

print("Connecting...")
dev = btle.Peripheral("A4:C1:38:D7:8D:90")

service=dev.getServiceByUUID("0000180f-0000-1000-8000-00805f9b34fb")
character=service.getCharacteristics()
print(character[0].read())
