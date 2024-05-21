#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define SERVICE_UUID "d8c1e1e3-7e68-4d84-9f91-c1e6d47dbdd7"
#define CHARACTERISTIC_UUID "f364a19d-36b5-4f3b-a53a-fdbb3d14e4b5"

static BLEAddress *pServerAddress;
static boolean doConnect = false;
static boolean connected = false;
static BLERemoteCharacteristic* pRemoteCharacteristic;
static unsigned long scanStartTime;
static unsigned long scanDuration = 60000; // 60 seconds

class MyClientCallback : public BLEClientCallbacks {
  void onConnect(BLEClient* pclient) {
    connected = true;
    Serial.println("Connected to the server");
  }

  void onDisconnect(BLEClient* pclient) {
    connected = false;
    Serial.println("Disconnected from the server");
  }
};

bool connectToServer(BLEAddress pAddress) {
  Serial.print("Connecting to server: ");
  Serial.println(pAddress.toString().c_str());

  BLEClient*  pClient  = BLEDevice::createClient();
  pClient->setClientCallbacks(new MyClientCallback());
  pClient->connect(pAddress);

  Serial.println("Connected to server");

  BLERemoteService* pRemoteService = pClient->getService(SERVICE_UUID);
  if (pRemoteService == nullptr) {
    Serial.println("Failed to find our service UUID");
    pClient->disconnect();
    return false;
  }

  pRemoteCharacteristic = pRemoteService->getCharacteristic(CHARACTERISTIC_UUID);
  if (pRemoteCharacteristic == nullptr) {
    Serial.println("Failed to find our characteristic UUID");
    pClient->disconnect();
    return false;
  }

  if (pRemoteCharacteristic->canRead()) {
    std::string value = pRemoteCharacteristic->readValue();
    Serial.print("The characteristic value was: ");
    Serial.println(value.c_str());
  }

  connected = true;
  return true;
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    Serial.print("Advertised Device found: ");
    Serial.println(advertisedDevice.toString().c_str());

    if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(BLEUUID(SERVICE_UUID))) {
      Serial.print("Found our device! Address: ");
      Serial.println(advertisedDevice.getAddress().toString().c_str());
      pServerAddress = new BLEAddress(advertisedDevice.getAddress());
      doConnect = true;
      BLEDevice::getScan()->stop();
    }
  }
};

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Starting BLE Client...");

  BLEDevice::init("");

  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);

  scanStartTime = millis();
  pBLEScan->start(scanDuration / 1000);
  Serial.println("Scanning started...");
}

void loop() {
  if (doConnect == true) {
    if (connectToServer(*pServerAddress)) {
      Serial.println("We are now connected to the BLE Server.");
    } else {
      Serial.println("We have failed to connect to the server; there is nothing more we will do.");
    }
    doConnect = false;
  }

  if (connected) {
    // Logic when connected to the BLE server
  } else if (millis() - scanStartTime > scanDuration) {
    Serial.println("Failed to find the BLE Server within the scan time.");
    BLEDevice::getScan()->stop();
    scanStartTime = millis(); // reset scan start time
  }

  delay(1000);
}
