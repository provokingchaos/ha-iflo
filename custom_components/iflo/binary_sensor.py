from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    
    if "data" in coordinator.data:
        for location in coordinator.data["data"]:
            for device in location.get("devices", []):
                sensors.append(IFloConnectionBinarySensor(coordinator, device))
    
    async_add_entities(sensors)

class IFloConnectionBinarySensor(CoordinatorEntity, BinarySensorEntity):
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
        }

    @property
    def name(self): return f"{self._device.get('name')} Connection Issue"
    @property
    def unique_id(self): return f"{self._device_id}_connection_issue"
    @property
    def device_class(self): return BinarySensorDeviceClass.PROBLEM
    
    @property
    def is_on(self):
        if "data" in self.coordinator.data:
            for location in self.coordinator.data["data"]:
                for d in location.get("devices", []):
                    if d["id"] == self._device_id:
                        return d.get("hasConnectionIssue", False)
        return False
