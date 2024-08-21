This repository aims to extract wifi channel state information (CSI) data from a ESP32C6 board which is far cheaper than other alternatives.
All available ESP32 based CSI tools till now, are not suitable for ESP32C6 as this is a new chipset having new features like wifi6 . The CSI data is of 256 subcarriers of wifi 6 which can be further analyzed.
*****INSTALLATION*****
Please install ESP-IDF from official website of espressif.
After installation, clone this repository to your local system.
Go to the cloned directory.
Open powershell as administator in that directory.
Connect the ESP32C6 board.
Enable CSI by executing menuconfig.
Flash the source code using IDF.py Flash set-target ESP32C6
Open any serial monitor and connect to the com port.
If you want to plot the CSI, Download the .ipynb fles (Matplotlib or Plotly) and execute using jupyter notebbok.
