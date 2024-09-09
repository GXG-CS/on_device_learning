import asyncio
from bleak import BleakScanner, BleakClient

# Target MAC address of the ESP32 device
TARGET_MAC = "44:17:93:E4:E3:7E"  # Replace with your ESP32 MAC address

# UUID for the custom service and characteristic
CUSTOM_SERVICE_UUID = "0000ff00-0000-1000-8000-00805f9b34fb"
CUSTOM_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"

# Function to handle received notifications
def notification_handler(sender, data):
    print(f"Received data from ESP32: {data.decode('utf-8')}")

# Function to connect to the ESP32 device and listen for notifications
async def connect_to_device():
    print(f"Scanning for BLE devices with MAC {TARGET_MAC}...")

    devices = await BleakScanner.discover()
    target_device = None
    for device in devices:
        if device.address == TARGET_MAC:
            target_device = device
            print(f"Found target device: {device.name} - {device.address}")
            break

    if not target_device:
        print(f"Target device {TARGET_MAC} not found. Scanning again...")
        return

    # Connect to the target ESP32 device
    async with BleakClient(target_device) as client:
        print(f"Connected to {target_device.name}")

        # Start receiving notifications from the custom characteristic
        await client.start_notify(CUSTOM_CHARACTERISTIC_UUID, notification_handler)

        print("Listening for node info notifications from ESP32...")
        try:
            while True:
                await asyncio.sleep(5)  # Keep listening
        except KeyboardInterrupt:
            print("Stopping notifications...")
            await client.stop_notify(CUSTOM_CHARACTERISTIC_UUID)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(connect_to_device())
        print("Scanning again in 5 seconds...")
        loop.run_until_complete(asyncio.sleep(5))
