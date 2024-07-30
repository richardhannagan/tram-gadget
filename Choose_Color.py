import RGB1602
import time
import math
colorR = 64
colorG = 128
colorB = 64

lcd=RGB1602.RGB1602(16,2)

blue = (0,128,128)
green = (64,255,0)

def parse_utc_time(utc_time_str):
    year = int(utc_time_str[0:4])
    month = int(utc_time_str[5:7])
    day = int(utc_time_str[8:10])
    hour = int(utc_time_str[11:13])
    minute = int(utc_time_str[14:16])
    second = int(utc_time_str[17:19])
    return (year, month, day, hour, minute, second, 0, 0)

while True:
    lcd.setRGB(green[0], green[1], green[2])
    lcd.setCursor(0, 0)
    lcd.printout("Next Tram       ")
    lcd.setCursor(0, 1)
    lcd.printout("1 min, 6 min    ")
    time.sleep(2)
    
    lcd.setRGB(blue[0], blue[1], blue[2])
    lcd.setCursor(0, 0)
    lcd.printout("Next Train      ")
    lcd.setCursor(0, 1)
    lcd.printout("10 min, 28 min  ")
    time.sleep(2)