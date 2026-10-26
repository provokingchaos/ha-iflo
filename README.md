# iFLO HVAC Custom Integration for Home Assistant

A HACS-compatible custom integration for monitoring your iFLO Smart Automated A/C Drain Line Cleaning System via the cloud API.

## Features
Creates a Device in Home Assistant for each iFLO device on your account, populated with the following sensors:
- **Battery Level**
- **WiFi Connection Level** 
- **Cartridge ID / Bottle ID**
- **Date Installed**
- **Dispenses Remaining**
- **Protected Until Date**
- **Next Dispense Date**
- **Connection Issue** (Binary Sensor)

## Installation
1. Upload the `custom_components/iflo` directory to your Home Assistant `custom_components` directory, or add this repository as a Custom Repository in HACS.
2. Restart Home Assistant.
3. In Home Assistant, go to **Settings > Devices & Services > Add Integration**, and search for **iFLO HVAC**.
4. Enter your `x-access-token` (JWT) obtained from inspecting the web traffic on app.iflo.com.

*Note: Your JWT expires 1 year from the date it is issued.*
