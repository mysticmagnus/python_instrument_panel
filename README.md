# Python Instrument Panel Controller

This project is a PC-side automation script (Python) that demonstrates two-way communication with a custom Arduino-based "Instrument Panel."

## Features

* **Object-Oriented Control:** Uses a reusable `Instrument` class to manage the `pySerial` connection, hiding low-level details.
* **Two-Way Communication:**
    * **Control (Write):** Sends `DISP:MSG` commands to write text directly to the instrument's OLED screen.
    * **Query (Read):** Sends `MEAS:POT?` commands to request data from the instrument's potentiometer.
* **Test Sequencing:** Runs a configurable loop to log data over time.
* **Data Logging:** Saves all sensor readings to a timestamped `.csv` file, which is correctly ignored by Git.
* **Verification:** Performs an `*IDN?` check on connection to ensure the correct device is attached.
* **Robustness:** Uses a `try...finally` block to guarantee the serial port is always closed cleanly, even if an error occurs.

## How to Use

1.  **Hardware:** Upload the corresponding "Instrument Panel" Arduino sketch to an Arduino Uno using the Sensor Kit Base.
2.  **Repo:** Clone this repository and create a virtual environment.
3.  **Install:** Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure:** Open `panel_control.py` and update the `SERIAL_PORT` variable to match your Arduino's COM port.
5.  **Run:** Execute the script from your terminal:
    ```bash
    python panel_control.py
    ```

The script will run, update the OLED, log 20 samples to `potentiometer_log.csv`, and update the OLED again.