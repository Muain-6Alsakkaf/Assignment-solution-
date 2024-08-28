import requests
import logging
from pymodbus.client import ModbusTcpClient as ModbusClient
import time
import struct

UNIT = 0x1
DEVICE_ADDRESS = "169.254.20.1"
DEVICE_PORT = 502
SERVER_ADDRESS = "http://localhost:5000"
DATA_END_POINT = "/data"
PERIOD = 5

# The addresses and register count for each data channel
DATA_CHANNELS = {
    "VOLTAGE": (352, 2),    # Voltage (RMS)
    "FREQUENCY": (424, 2)   # Frequency
}

def send_to_server(data: dict):
    """Send sensor data to server."""
    try:
        url = SERVER_ADDRESS + DATA_END_POINT
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error sending data to server: {e}")
        return False

def convert_registers_to_float32(registers):
    """Convert Modbus register values to float32."""
    if len(registers) == 2:  # We expect two registers for float32 values
        # Combine two 16-bit registers into one 32-bit float using struct
        raw_value = struct.pack('>HH', registers[1], registers[0])  # Big endian format
        return struct.unpack('>f', raw_value)[0]
    else:
        raise ValueError("Invalid register count, expected 2 registers for a float32 value")

def get_sensor_data():
    """Fetch sensor data from the Modbus ."""
    client = ModbusClient(DEVICE_ADDRESS, port=DEVICE_PORT)
    client.connect()
    data = {}
    
    try:
        for key, (address, count) in DATA_CHANNELS.items():
            response = client.read_input_registers(address=address, count=count, unit=UNIT)
            if response.isError():
                print(f"Error reading {key} from Modbus.")
                continue
            # Convert registers to float32
            data[key] = convert_registers_to_float32(response.registers)
    except Exception as e:
        print(f"Error during Modbus read: {e}")
    finally:
        client.close()
    
    return data

def loop():
    """Continuous loop to fetch data and send it to the server."""
    while True:
        #data = get_sensor_data()
        #print(f"Sensor Data: {data}")
        data = {"VOLTAGE":[11],"FREQUENCY":[11]}
        response = send_to_server(data)
        
        if not response:
            print("[-] Error sending data to server")
        else:
            print("[+] Data sent successfully to server")
        
        time.sleep(PERIOD)

def main():
    loop()

if __name__ == "__main__":
    main()