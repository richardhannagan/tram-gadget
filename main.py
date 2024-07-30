import urequests as requests
import time
import utime
import ntptime
import RGB1602
import secrets
import network

lcd = RGB1602.RGB1602(16, 2)

rp2.country('AU')

ssid = secrets.SSID
password = secrets.PASSWORD
signature1 = secrets.SIGNATURE1
signature2 = secrets.SIGNATURE2

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 60
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
ntptime.settime()

def parse_utc_time(utc_time_str):
    year = int(utc_time_str[0:4])
    month = int(utc_time_str[5:7])
    day = int(utc_time_str[8:10])
    hour = int(utc_time_str[11:13])
    minute = int(utc_time_str[14:16])
    second = int(utc_time_str[17:19])
    return (year, month, day, hour, minute, second, 0, 0)

def time_until(utc_time_str):
    utc_time = parse_utc_time(utc_time_str)
    utc_timestamp = utime.mktime(utc_time)
    now_utc_timestamp = utime.time()
    time_difference = utc_timestamp - now_utc_timestamp
    minutes, seconds = divmod(int(time_difference), 60)
    return minutes, seconds

while True:
    try:
        response_tm = requests.get(f"https://timetableapi.ptv.vic.gov.au/v3/departures/route_type/1/stop/3174?max_results=2&devid=3002941&signature={signature1}")
        if response_tm.status_code == 200:
            data_tm = response_tm.json()
            departures_tm = data_tm.get('departures', [])
            if departures_tm:
                next_departure_tm_1 = departures_tm[0]
                estimated_departure_tm_1 = next_departure_tm_1.get('estimated_departure_utc')
                minutes_tm_1, seconds_tm_1 = time_until(estimated_departure_tm_1)
                next_departure_tm_2 = departures_tm[1]
                estimated_departure_tm_2 = next_departure_tm_2.get('estimated_departure_utc')
                minutes_tm_2, _ = time_until(estimated_departure_tm_2)
            else:
                minutes_tm_1 = "No data"
                seconds_tm_1 = "No data"
                minutes_tm_2 = "No data"
        response_tm.close()

        response_tn = requests.get(f"https://timetableapi.ptv.vic.gov.au/v3/departures/route_type/0/stop/1165?direction_id=1&max_results=2&devid=3002941&signature={signature2}")
        if response_tn.status_code == 200:
            data_tn = response_tn.json()
            departures_tn = data_tn.get('departures', [])
            if departures_tn:
                next_departure_tn_1 = departures_tn[0]
                estimated_departure_tn_1 = next_departure_tn_1.get('estimated_departure_utc')
                minutes_tn_1, seconds_tn_1 = time_until(estimated_departure_tn_1)
                next_departure_tn_2 = departures_tn[1]
                estimated_departure_tn_2 = next_departure_tn_2.get('estimated_departure_utc')
                minutes_tn_2, _ = time_until(estimated_departure_tn_2)
            else:
                minutes_tn_1 = "No data"
                seconds_tn_1 = "No data"
                minutes_tn_2 = "No data"
        response_tn.close()

        lcd.setRGB(120, 190, 31)
        lcd.setCursor(0, 0)
        lcd.printout(f"{minutes_tm_1} min {seconds_tm_1} sec                ")
        lcd.setCursor(0, 1)
        lcd.printout(f"{minutes_tm_2} min                ")
        time.sleep(3)

        lcd.setRGB(245, 126, 182)
        lcd.setCursor(0, 0)
        lcd.printout(f"{minutes_tn_1} min {seconds_tn_1} sec                ")
        lcd.setCursor(0, 1)
        lcd.printout(f"{minutes_tn_2} min                ")
        time.sleep(3)

    except Exception as e:
        lcd.setRGB(128, 0, 0)
        e_str = str(e)
        first_sixteen = e_str[:16]
        remainder = e_str[16:]
        lcd.setCursor(0, 0)
        lcd.printout(first_sixteen)
        lcd.setCursor(0, 1)
        lcd.printout(remainder)
        time.sleep(3)
        print(str(e))