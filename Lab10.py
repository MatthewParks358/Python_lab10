import asyncio
import shelve
from time import strftime, gmtime, sleep
from bleak import BleakScanner

KNOWN_DEVICES = {
    "ResMed 804611": "8C:F6:81:0F:F7:3F",
    "moto e": "38:E3:9F:CB:FD:96"
}

#test

async def scan_for_devices():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover(5.0)
    for device in devices:
        print(f"Device Name: {device.name}, Address: {device.address}")
    return devices

async def check_for_known_devices():
    devices = await BleakScanner.discover()
    nearby_known_devices = {}

    for device in devices:
        if device.address in KNOWN_DEVICES.values():
            device_name = [name for name, addr in KNOWN_DEVICES.items() if addr == device.address][0]
            print(f"{device_name} is nearby!")
            nearby_known_devices[device_name] = device.address

    return nearby_known_devices

def log_devices(devices):
   with shelve.open( "device_log" ) as db:
       for name, address in devices.items():
           key = name + '_' + address
           formatted_time = strftime( "%Y-%m-%d %H:%M:%S", gmtime())
           if key in db:
               time_list = db[key]
               time_list.append(formatted_time)
               db[key] = time_list
           else:
               db[key] = [formatted_time]
   print( "Logged devices in the shelf database." )

async def scan():
    nearby_devices = await check_for_known_devices()
    if nearby_devices:
        log_devices( nearby_devices )
    else:
        print( "No known devices nearby." )

#I tried to do implement the cleanup_logs function, but I couldn't figure out how with the restrictions the lab imposed.
#DO NOT GIVE ME EXTRA CREDIT FOR TRYING, MY GRADE IS ALREADY AT 99% AND I"M WORRIED THAT IT WILL INTEGER OVERFLOW AT 100% /s
#async def cleanup_logs():
#    with shelve.open("device_log") as db:
#        db.clear()
#    print("Cleared the device log.")

def main():
    # asyncio.run( scan_for_devices() )
    while True:
        print("Scanning...")
        asyncio.run( scan() )
        print("sleeping till next loop...")
        sleep(10)
        print("Verifying log...")
        with shelve.open("device_log") as db:
            for name, address in db.items():
                print(f"{name}: {address}")

if __name__ == '__main__':
    main()