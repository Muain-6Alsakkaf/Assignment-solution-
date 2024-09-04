import requests
import logging
import time
import struct

# Constants
UNIT = 0x1
DEVICE_ADDRESS = "169.254.20.1"
DEVICE_PORT = 502
SERVER_ADDRESS = "http://localhost:5000"
DATA_END_POINT = "/data"
PERIOD = 5

# Simulated Modbus data for voltage and frequency (12 registers each for 3 channels)
SIMULATED_VOLTAGE_REGISTERS = [49709, 17262, 20887, 15905, 45177, 15748, 0, 0, 0, 0, 0, 0]
SIMULATED_FREQUENCY_REGISTERS = [54339, 16973, 54339, 16973, 43051, 16949, 0, 0, 0, 0, 0, 0]

# Address and count of registers for voltage and frequency (12 registers for each, 3 channels)
DATA_CHANNELS = {
    "VOLTAGE": (352, 12),    # Voltage (RMS) for 3 channels
    "FREQUENCY": (424, 12)   # Frequency for 3 channels
}

def send_to_server(data: dict):
    """Send sensor data to the server."""
    try:
        url = SERVER_ADDRESS + DATA_END_POINT
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"[+] Data sent successfully: {data}")
            return True
        else:
            print(f"[-] Error in server response, status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] Error sending data to server: {e}")
        return False

def convert_registers_to_float32(registers):
    """Convert Modbus register values to float32."""
    if len(registers) == 2:  # We expect two registers per float32 value
        # Combine two 16-bit registers into one 32-bit float using struct (big endian)
        raw_value = struct.pack('>HH', registers[1], registers[0])  # Big-endian format
        return struct.unpack('>f', raw_value)[0]
    else:
        raise ValueError("Invalid register count, expected 2 registers for a float32 value")

def process_channel_data(registers):
    """Convert a block of 12 registers into three float32 values for three channels."""
    channels = {}
    for i in range(0, len(registers), 2):  # Step through the registers in pairs
        channel_number = i // 2 + 1
        channel_value = convert_registers_to_float32(registers[i:i+2])
        channels[f"Channel{channel_number}"] = channel_value
    return channels

def simulate_modbus_response(address):
    """Simulate Modbus response by returning the corresponding data for voltage or frequency."""
    if address == 352:  # Simulated voltage data
        return SIMULATED_VOLTAGE_REGISTERS
    elif address == 424:  # Simulated frequency data
        return SIMULATED_FREQUENCY_REGISTERS
    else:
        return None

def get_sensor_data():
    """Simulate fetching sensor data for voltage and frequency."""
    data = {}
    
    try:
        for key, (address, count) in DATA_CHANNELS.items():
            # Simulate reading 12 registers (for 3 channels, 2 registers each)
            registers = simulate_modbus_response(address)
            if registers is None:
                print(f"Error reading {key} from simulated Modbus.")
                continue
            # Convert the 12 registers into 3 float32 values (for 3 channels)
            channel_values = process_channel_data(registers)
            data[key] = channel_values

    except Exception as e:
        print(f"Error during Modbus read: {e}")

    return data

def loop():
    """Continuous loop to fetch data and send it to the server."""
    while True:
        # Simulate getting sensor data (voltage and frequency)
        sensor_data = get_sensor_data()

        # Prepare the data in a format that can be sent to the server
        formatted_data = {}
        for key, channels in sensor_data.items():
            for channel, value in channels.items():
                formatted_data[f"{key}_{channel}"] = value

        # Send the data to the server
        response = send_to_server(formatted_data)
        
        if not response:
            print("[-] Error sending data to server")
        else:
            print("[+] Data sent successfully to server")

        time.sleep(PERIOD)

def main():
    loop()

if __name__ == "__main__":
    main()

