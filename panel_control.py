import serial
import time
import datetime
import csv
import os

# --- CONFIGURATION ---

SERIAL_PORT = 'COM3'  # !! CHANGE THIS to your Arduino's port
BAUD_RATE = 9600
TIMEOUT = 1
# This MUST match the *IDN? response from your Arduino sketch
INSTRUMENT_ID = 'ArduinoSensorKit,v1.0,SN:SK12345'
LOG_FILE = 'potentiometer_log.csv'
SAMPLES_TO_TAKE = 20
DELAY_BETWEEN_SAMPLES = 0.5

# ---------------------

class Instrument:
    """
    A class to represent an Arduino-based Instrument.
    """
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        # This is the VARIABLE that holds the serial object
        self.connection = None

    # FIX: Renamed from 'connection' to 'connect' to avoid conflict
    def connect(self):
        """
        Opens the serial connection.
        """
        try:
            # We assign the open port to the self.connection variable
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Connecting to port {self.port}...")
            time.sleep(2)
            print("Connection established.")
            return True
        except serial.SerialException as e:
            print(f"Error: Could not connect to port {self.port}. {e}")
            return False

    def disconnect(self):
        """
        Closes the serial connection.
        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            print(f"Disconnected from {self.port}.")

    def query(self, command):
        """
        Sends a command and returns the response.
        """
        if not self.connection or not self.connection.is_open:
            print("Error: Not connected.")
            return None
        try:
            self.connection.write(command.encode('utf-8') + b'\n')
            response_bytes = self.connection.readline()
            response_str = response_bytes.decode('utf-8').strip()
            return response_str
        except serial.SerialException as e:
            print(f"Error during query '{command}': {e}")
            return None

# --- Helper Functions ---

def init_log_file(filepath):
    """
    Creates the CSV log file and writes the header row.
    """
    file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'pot_value_percent'])
            print(f"Created new log file: {filepath}")

def run_test_sequence(device, num_samples, delay):
    """
    Runs the main test loop.
    """
    print(f"Starting test sequence: {num_samples} samples, {delay}s delay...")

    # 1. Send message to OLED
    ack = device.query('DISP:MSG Logging...')
    print(f"OLED command acknowledged: {ack}")

    for i in range(num_samples):
        pot_value = device.query("MEAS:POT?")
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()

        if pot_value:
            print(f" Sample {i + 1}/{num_samples}: {pot_value}%")
            with open(LOG_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, pot_value])
        else:
            print(f" Sample {i + 1}/{num_samples}: Error reading value.")

        time.sleep(delay)

    print("Test sequence complete.")
    ack = device.query('DISP:MSG Complete!')
    print(f"OLED command acknowledged: {ack}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":

    init_log_file(LOG_FILE)
    my_device = Instrument(SERIAL_PORT, BAUD_RATE, TIMEOUT)

    try:
        # FIX: We now call the renamed method .connect()
        if my_device.connect():
            idn_response = my_device.query("*IDN?")
            print(f"Instrument ID: {idn_response}")

            if idn_response == INSTRUMENT_ID:
                run_test_sequence(my_device, SAMPLES_TO_TAKE, DELAY_BETWEEN_SAMPLES)
            else:
                print("Error: Connected to wrong instrument!")
                print(f"Expected: {INSTRUMENT_ID}")
                print(f"Received: {idn_response}")
    except Exception as e:
        print(f"An unhandled error occurred: {e}")
    finally:
        my_device.disconnect()