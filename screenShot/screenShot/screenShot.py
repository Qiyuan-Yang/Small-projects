from PIL import ImageGrab
import time

def wait(s):
    time.sleep(s)

for i in range(10):
    filename = str(i) + '.jpg'
    ImageGrab.grab().save('C:\\Users\\yangq\\Downloads\\sc\\' + filename)
    wait(1)
