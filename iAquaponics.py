import RPi.GPIO as GPIO
import time
import datetime
from threading import Thread
import signal

#PUMP1_PIN = 24 # In1: Pump from aquarium to garden # port is in raspberry
PUMP2_PIN = 25  # In2: Pump from garden to aquarium # port is in raspberry
LIGHT_PLANTS_PIN = 16  # In3: Light for plants (07:00 - 21:00) # port is in raspberry 
PUMP1_PIN = 23 # in4: Light for fish (07:00 - 18:00) -> change to In1: Pump from aquarium to garden -> # port is in raspberry

PUMP1_ON_TIME = 3 * 60 # 3 minutes on
PUMP2_ON_TIME = 6 * 60 # 6 minutes on
WAIT_TIME = 10 * 60 # 10 minutes wait time  

# Light schedule (in hours)
PLANT_LIGHT_ON = 7
PLANT_LIGHT_OFF = 21
#AQUARIUM_LIGHT_ON = 7
#AQUARIUM_LIGHT_OFF = 18

GPIO.setmode(GPIO.BCM)

def pump_cycle():
    """Control the pumps with specific timings."""
    while True:
        GPIO.setmode(GPIO.BCM)
        # Turn on Pump1 (from aquarium to garden)
        GPIO.setup(PUMP1_PIN, GPIO.OUT)
        pump1_time = datetime.datetime.now()
        print("time is:" + pump1_time.strftime("%d-%m %H:%M:%S") + " Pump 1 on")
        GPIO.output(PUMP1_PIN, GPIO.LOW)

        time.sleep(PUMP1_ON_TIME)

        GPIO.output(PUMP1_PIN, GPIO.HIGH)
        # Plants remain in water for 10 minutes (WAIT_TIME)
        plants_time = datetime.datetime.now()
        print("time is: " + plants_time.strftime("%d-%m %H:%M:%S") + " Plants in water")
        GPIO.cleanup(PUMP1_PIN)
        time.sleep(WAIT_TIME)
        
        # Turn on Pump2 (from garden to aquarium)
        pump2_time = datetime.datetime.now()
        print("Time is: " + pump2_time.strftime("%d-%m %H:%M:%S") + " Pump 2 on")
        GPIO.setup(PUMP2_PIN, GPIO.OUT)
        GPIO.output(PUMP2_PIN, GPIO.LOW)

        time.sleep(PUMP2_ON_TIME)
        GPIO.output(PUMP2_PIN, GPIO.HIGH)
        GPIO.cleanup(PUMP2_PIN)

        # Wait for remaining cycle time
        sleep_time = datetime.datetime.now()
        print("Time is: " + sleep_time.strftime("%d-%m %H:%M:%S") + " Waiting for next pump cycle")
        time.sleep(54 * 60 ) # 54 min total - Pump2 ON time

def control_lights():
    """Control lights based on the time of day."""
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        GPIO.setmode(GPIO.BCM)
        
        # Control plant light (07:00 to 21:00)
        if PLANT_LIGHT_ON <= hour < PLANT_LIGHT_OFF:
            GPIO.setup(LIGHT_PLANTS_PIN, GPIO.OUT)
            GPIO.output(LIGHT_PLANTS_PIN, GPIO.HIGH)
#            print("Plants on")
        else:
            GPIO.setup(LIGHT_PLANTS_PIN, GPIO.OUT)
            GPIO.output(LIGHT_PLANTS_PIN, GPIO.LOW)
            GPIO.cleanup(LIGHT_PLANTS_PIN)
            
        '''# Control fish light (08:00 to 18:00)
        if AQUARIUM_LIGHT_ON <= hour < AQUARIUM_LIGHT_OFF:
            GPIO.setup(LIGHT_AQUARIUM_PIN, GPIO.OUT)
            GPIO.output(LIGHT_AQUARIUM_PIN, GPIO.HIGH)
            print("Fishes on ")
        else:
            GPIO.setup(LIGHT_AQUARIUM_PIN, GPIO.OUT)
            GPIO.output(LIGHT_AQUARIUM_PIN, GPIO.LOW)
            GPIO.cleanup(LIGHT_AQUARIUM_PIN)'''
        
        # Sleep for 60 seconds before checking again
        time.sleep(60)

def cleanup_gpio():
    """Ensure all GPIO outputs are off."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUMP1_PIN, GPIO.OUT)
    GPIO.setup(PUMP2_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_PLANTS_PIN, GPIO.OUT)
    
    GPIO.output(PUMP1_PIN, GPIO.HIGH)
    GPIO.output(PUMP2_PIN, GPIO.HIGH)
    GPIO.output(LIGHT_PLANTS_PIN, GPIO.LOW)
    GPIO.cleanup()
    
def handle_termination_signal(signum, frame):
    cleanup_gpio()
    sys.exit(0)

def main():
    signal.signal(signal.SIGTERM, handle_termination_signal)
    try:
        # Start pump and light control threads
        cleanup_gpio()
        pump_thread = Thread(target=pump_cycle)
        light_thread = Thread(target=control_lights)
        
        pump_thread.start()
        light_thread.start()
        
        pump_thread.join()
        light_thread.join()

    except KeyboardInterrupt:
        # If the application is interrupted, clean up the GPIO pins
        cleanup_gpio()
        exit()

if __name__ == "__main__":
    main()
