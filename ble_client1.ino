#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEClient.h>
#include <BLEAddress.h>

#define SERVER_NAME "ESP32_BLE_Server"
#define SERVICE_UUID "d8c1e1e3-7e68-4d84-9f91-c1e6d47dbdd7"
#define CHARACTERISTIC_UUID "f364a19d-36b5-4f3b-a53a-fdbb3d14e4b5"

static BLEAddress *pServerAddress = nullptr;
static boolean connected = false;
static BLERemoteCharacteristic* pRemoteCharacteristic = nullptr;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    Serial.print("Advertised Device found: ");
    Serial.println(advertisedDevice.toString().c_str());

    if (advertisedDevice.haveName() && advertisedDevice.getName() == SERVER_NAME) {
      Serial.println("Found our device!");
      BLEDevice::getScan()->stop();
      pServerAddress = new BLEAddress(advertisedDevice.getAddress());
    }
  }
};

class MyClientCallback : public BLEClientCallbacks {
  void onConnect(BLEClient* pClient) {
    connected = true;
    Serial.println("Connected to server");
  }

  void onDisconnect(BLEClient* pClient) {
    connected = false;
    Serial.println("Disconnected from server");
  }
};

void notificationCallback(BLERemoteCharacteristic* pBLERemoteCharacteristic, uint8_t* pData, size_t length, bool isNotify) {
  Serial.print("Notification received: ");
  Serial.write(pData, length);
  Serial.println();
}

bool connectToServer(BLEAddress pAddress) {
  BLEClient* pClient = BLEDevice::createClient();
  pClient->setClientCallbacks(new MyClientCallback());

  Serial.print("Connecting to server: ");
  Serial.println(pAddress.toString().c_str());

  if (!pClient->connect(pAddress)) {
    Serial.println("Failed to connect to server");
    return false;
  }
  Serial.println("Connected to server");

  BLERemoteService* pRemoteService = pClient->getService(SERVICE_UUID);
  if (pRemoteService == nullptr) {
    Serial.print("Failed to find our service UUID: ");
    Serial.println(SERVICE_UUID);
    pClient->disconnect();
    return false;
  }
  Serial.println("Found our service");

  pRemoteCharacteristic = pRemoteService->getCharacteristic(CHARACTERISTIC_UUID);
  if (pRemoteCharacteristic == nullptr) {
    Serial.print("Failed to find our characteristic UUID: ");
    Serial.println(CHARACTERISTIC_UUID);
    pClient->disconnect();
    return false;
  }
  Serial.println("Found our characteristic");

  if (pRemoteCharacteristic->canNotify()) {
    pRemoteCharacteristic->registerForNotify(notificationCallback);
  }

  return true;
}

void setup() {
  Serial.begin(115200);
  Serial.println("Starting Arduino BLE Client application...");

  BLEDevice::init("");

  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  Serial.println("Scanning for BLE devices...");
  BLEScanResults scanResults = pBLEScan->start(30); // Scan for 30 seconds

  if (pServerAddress != nullptr) {
    Serial.println("Found server, attempting to connect...");
    if (connectToServer(*pServerAddress)) {
      Serial.println("Connected to server successfully");
    } else {
      Serial.println("Failed to connect to the server");
    }
  } else {
    Serial.println("Failed to find BLE server.");
  }
}

void loop() {
  // Do nothing here.
}
