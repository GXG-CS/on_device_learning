import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "d8c1e1e3-7e68-4d84-9f91-c1e6d47dbdd7"
CHARACTERISTIC_UUID = "f364a19d-36b5-4f3b-a53a-fdbb3d14e4b5"
DATA_FILE = "received_data.txt"

async def connect_to_device():
    print("Starting BLE scan...")
    devices = await BleakScanner.discover()
    esp32_device = None

    for device in devices:
        if device.name is None:
            continue
        print(f"Found device: {device.name}, Address: {device.address}")
        if "ESP32_BLE_Server" in device.name:
            esp32_device = device
            break

    if not esp32_device:
        print("ESP32 BLE Server not found.")
        return

    print(f"Connecting to {esp32_device.name} at {esp32_device.address}")
    async with BleakClient(esp32_device.address) as client:
        print(f"Connected to {esp32_device.name}")
        
        def notification_handler(sender, data):
            print(f"Notification from {sender}: {data}")
            with open(DATA_FILE, "a") as f:
                f.write(f"{data}\n")

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        await asyncio.sleep(30)  # Adjust the sleep time as necessary

        await client.stop_notify(CHARACTERISTIC_UUID)

loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_device())

