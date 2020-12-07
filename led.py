import RPi.GPIO as GPIO

class Led(object):
    def __init__(self):
        """
        index=0 is the center led (green)
        index=1 is the left most led (red)
        the right most led indicates power
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self._outputList = [20,21]
        GPIO.setup(self._outputList, GPIO.OUT)

    def cleanup(self):
        GPIO.cleanup()

    def set_output(self, index=None, state=False):
        """index and state are lists, both arguments are optional
        if index and state are omitted, set all leds OFF
        if index omitted and state a list, state list maps to outputs
        if index omitted and state true/false, all outputs are true/false
        if index set and state omitted, output[index] is false
        if index set and state set true/false, output[index]=state
        """
        if index is None:
            GPIO.output(self._outputList, state)
        else:
            GPIO.output(self._outputList[index], state)

    def read_output(self, index=None):
        if index is None:
            return [GPIO.input(pin) for pin in self._outputList]
        else:
            return GPIO.input(self._outputList[index])

if __name__ == '__main__':
    from time import sleep

    led = Led()

    # all on
    led.set_output(state=True)
    print(led.read_output())
    sleep(3)

    # all off
    led.set_output()
    print(led.read_output())
    sleep(3)

    # green center on, red left off
    led.set_output(state=[1,0])
    print(led.read_output())
    sleep(3)

    # red left on, green center off 
    led.set_output(state=[0,1])
    print(led.read_output())
    sleep(3)

    # all off
    led.set_output(state=[0,0])
    print(led.read_output())

