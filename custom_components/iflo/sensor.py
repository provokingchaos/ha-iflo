from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from datetime import datetime
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    
    if "data" in coordinator.data:
        for location in coordinator.data["data"]:
            for device in location.get("devices", []):
                sensors.append(IFloBatterySensor(coordinator, device))
                sensors.append(IFloWifiSensor(coordinator, device))
                sensors.append(IFloModeSensor(coordinator, device))
                
                if "bottle" in device:
                    sensors.append(IFloCartridgeSensor(coordinator, device))
                    sensors.append(IFloDispensesSensor(coordinator, device))
                    sensors.append(IFloInstallDateSensor(coordinator, device))
                
                sensors.append(IFloProtectedSensor(coordinator, device))
                sensors.append(IFloNextDispenseSensor(coordinator, device))

    async_add_entities(sensors)

class IFloBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device):
        super().__init__(coordinator)
        self._device = device
        self._device_id = device["id"]

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device.get("name", "iFLO Device"),
            "manufacturer": "iFLO",
            "sw_version": self._device.get("firmwareVersion")
        }

    def get_device_data(self):
        if "data" in self.coordinator.data:
            for location in self.coordinator.data["data"]:
                for d in location.get("devices", []):
                    if d["id"] == self._device_id:
                        return d
        return self._device

    def parse_datetime(self, dt_str):
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except ValueError:
            return None

class IFloBatterySensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Battery"
    @property
    def unique_id(self): return f"{self._device_id}_battery"
    @property
    def device_class(self): return SensorDeviceClass.BATTERY
    @property
    def state_class(self): return SensorStateClass.MEASUREMENT
    @property
    def native_unit_of_measurement(self): return "%"
    @property
    def native_value(self): return self.get_device_data().get("batteryLevel")

class IFloWifiSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} WiFi Signal"
    @property
    def unique_id(self): return f"{self._device_id}_wifi"
    @property
    def native_unit_of_measurement(self): return "%"
    @property
    def native_value(self): return self.get_device_data().get("connectionLevel")
    @property
    def icon(self): return "mdi:wifi"

class IFloModeSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Status Mode"
    @property
    def unique_id(self): return f"{self._device_id}_mode"
    @property
    def native_value(self): return self.get_device_data().get("mode", "unknown").capitalize()
    @property
    def icon(self): return "mdi:information"

class IFloCartridgeSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Cartridge ID"
    @property
    def unique_id(self): return f"{self._device_id}_cartridge_id"
    @property
    def native_value(self): 
        return self.get_device_data().get("bottle", {}).get("id")
    @property
    def icon(self): return "mdi:bottle-tonic"

class IFloDispensesSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Dispenses Remaining"
    @property
    def unique_id(self): return f"{self._device_id}_dispenses"
    @property
    def state_class(self): return SensorStateClass.MEASUREMENT
    @property
    def native_value(self): 
        return self.get_device_data().get("bottle", {}).get("dispenseLeft")
    @property
    def icon(self): return "mdi:counter"

class IFloInstallDateSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Date Installed"
    @property
    def unique_id(self): return f"{self._device_id}_installed"
    @property
    def device_class(self): return SensorDeviceClass.TIMESTAMP
    @property
    def native_value(self):
        return self.parse_datetime(self.get_device_data().get("bottle", {}).get("installedAt"))

class IFloProtectedSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Protected Until"
    @property
    def unique_id(self): return f"{self._device_id}_protected"
    @property
    def device_class(self): return SensorDeviceClass.TIMESTAMP
    @property
    def native_value(self):
        return self.parse_datetime(self.get_device_data().get("protectedUntil"))

class IFloNextDispenseSensor(IFloBaseSensor):
    @property
    def name(self): return f"{self._device.get('name')} Next Dispense Date"
    @property
    def unique_id(self): return f"{self._device_id}_next_dispense"
    @property
    def device_class(self): return SensorDeviceClass.TIMESTAMP
    @property
    def native_value(self):
        return self.parse_datetime(self.get_device_data().get("scheduledDispenseDate"))
