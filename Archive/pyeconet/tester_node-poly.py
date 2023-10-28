import asyncio
import logging
import aiohttp
import json
import time
#import getpass

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType
#from pyeconet.equipment.water_heater import WaterHeaterOperationMode
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


async def main():
    email = "sjpbailey@comcast.net"  # input("Enter your email: ").strip()
    # getpass.getpass(prompt='Enter your password: ')
    password = "my acess!"
    api = await EcoNetApiInterface.login(email, password=password)
    # , EquipmentType.THERMOSTAT
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])

    api.subscribe()
    await asyncio.sleep(5)
    """for equip_list in all_equipment.values():
        for equipment in equip_list:
            discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
            print("{}" .format(equipment.set_point))
            #print("{}" .format(equipment.temperature_unit))
            print("{}" .format(equipment.modes))
            #print("{}" .format(equipment.device_id))
            print("{}" .format(equipment.serial_number))
            print("{}" .format(equipment.mode))
            #print("{}" .format(all_equipment.values))
            print("{}" .format(equipment.enabled))"""
    
    for equip_list in all_equipment.values():
        for equipment in equip_list:
            #discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
            #dict_values([[<pyeconet.equipment.water_heater.WaterHeater object at 0x10d4ed410>]])
            # equipment.set_set_point()
            print(f"\nName: {equipment.device_name}\n")
            print("{}" .format(equipment.set_set_point))
            print(f"\nOperation mode: {equipment.modes[0]}\n")
            
            print("{}" .format(equipment.set_point))
            #time.sleep(10)
            #equipment.set_mode(1)
            #time.sleep(10)
            equipment.set_mode(1)
            #time.sleep(3)
            #equipment.set_set_point(140)
            #time.sleep(10)
            #equipment.set_set_point(120)
            #equipment.set_away_mode(False)
            #print(equipment.get_energy_usage)
            # print(json.dump)
            #print(all_equipment,{equipment.device_name}, {equipment.set_point==130})
            # print(pyeconet.api)
            # print(f"user/{equipment.user_id}/device/desired")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
