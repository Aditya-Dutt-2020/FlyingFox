import RPi.GPIO as GPIO
import time

# Set GPIO mode and input pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define function to run when button is pressed
def button_callback(channel):
    # Ignore button events that occur too quickly
    if time.time() - button_callback.last_call < 0.1:
        return
    button_callback.last_call = time.time()

    # Check button state before printing message
    if GPIO.input(17) == GPIO.LOW:
        print("Button pressed")

button_callback.last_call = 0

# Add event listener for button press
GPIO.add_event_detect(17, GPIO.FALLING, callback=button_callback, bouncetime=200)

# Keep the script running until it's stopped
while True:
    pass
