from bluepy import btle

print("Connecting...")
dev = btle.Peripheral("A4:C1:38:D7:8D:90")

print("Services...")

for svc in dev.services:
    print(str(svc))
    print(svc.uuid)
