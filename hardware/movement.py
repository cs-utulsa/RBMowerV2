import PNGtoArray
import serial
import time

# Set up serial communication
print("Program starting...")
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# Delay for the Arduino to initialize
time.sleep(2)
print("Connection established!")

binary_array = [[random.randint(0, 1) for j in range(64)] for i in range(64)]

numrows = len(binary_array)
numcols = len(binary_array[0])

screen_width = numcols * 10
screen_height = numrows * 10
bool = True
rows = 0


def moveForwardOrBackward(bool):
    if bool == True:
        ser.write(bytes([0x01]))
    else:
        ser.write(bytes([0x02]))


def movePenUpOrDown(bool):
    if bool == True:
        ser.write(bytes([0x10]))
    else:
        ser.write(bytes([0x20]))


def onecycle():
    global rows
    for i in range(numcols):
        if binary_array[rows][i] == 1:
            movePenUpOrDown(True)
            moveForwardOrBackward(bool)
            time.sleep(3)
        else:
            movePenUpOrDown(False)
            moveForwardOrBackward(bool)
            time.sleep(3)
    rows += 1


for i in range(numrows):
    onecycle()
    if rows % 2 == 1:
        ser.write(bytes([0x04]))
        time.sleep(3)
        movePenUpOrDown(False)
        moveForwardOrBackward(bool)
        time.sleep(3)
        ser.write(bytes([0x04]))
        time.sleep(3)
    else:
        ser.write(bytes([0x03]))
        time.sleep(3)
        movePenUpOrDown(False)
        moveForwardOrBackward(bool)
        time.sleep(3)
        ser.write(bytes([0x03]))
        time.sleep(3)
    if (bool == True):
        bool = False
    else:
        bool = True
