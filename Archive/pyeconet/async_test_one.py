import asyncio
import logging
#import time
#import getpass
import requests
from requests.auth import HTTPBasicAuth #HTTP

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType


async def main():
    
    email = "sjpbailey@comcast.net" #input("Enter your email: ").strip()
    password = "NatiqueRheem61" #getpass.getpass(prompt='Enter your password: ')  
    api = await EcoNetApiInterface.login(email, password)
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
    try:
        #r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
        api = await EcoNetApiInterface.login(email, password=password)
        r = all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        for equip_list in all_equipment.values():
            for equipment in equip_list:
                print(f"\nName: {equipment.device_name}\n")
                print(f"\nSerial #: {equipment.serial_number}\n")
                print(f"\nOperation mode: {equipment.device_id}\n")
                print(f"\nSet point: {equipment.set_point}\n")
                print(f"\nOperation mode: {equipment.mode}\n")
                print(f"\nOperation modes: {equipment.modes}\n")
                print(f"\nOperation modes: {equipment}\n")
                

            return equip_list
        else:
            print.error("Rheem Econet Error:  " + equip_list)
            return None

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())        