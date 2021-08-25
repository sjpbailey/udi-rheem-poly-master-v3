import asyncio
import logging
import aiohttp
#import time
#import getpass

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType
#from pyeconet.equipment.water_heater import WaterHeaterOperationMode
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


async def main():
    email = "sjpbailey@comcast.net" #input("Enter your email: ").strip()
    password = "NatiqueRheem61" #getpass.getpass(prompt='Enter your password: ')
    api = await EcoNetApiInterface.login(email, password=password)
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER]) #, EquipmentType.THERMOSTAT
    #api.subscribe()
    #await asyncio.sleep(5)
    #for equip_list in all_equipment.values():
    #    for equipment in equip_list:
                #discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
                #dict_values([[<pyeconet.equipment.water_heater.WaterHeater object at 0x10d4ed410>]])
    #            print(f"\nName: {all_equipment.values}")
    #            print("\n{equipment}")
    #            print("\n" f"{all_equipment.values}")
    #            print("\n{}" .format(equipment.device_name))
    #            print(f"\nName: {equipment.device_name}\n")
    #            print("\n")
                #2print("{}" .format(equipment.set_point))
                #3print("{}" .format(equipment.modes))
                #4print("{}" .format(equipment.device_id))
                #5print("{}" .format(equipment.serial_number))
                #6print("{}" .format(equipment.mode))
                #7print("{}" .format(all_equipment.values))
                #print("{}" .format(logging.basicConfig()))
                #print(logging.getLogger().setLevel(logging.DEBUG))
                #payload = {"@SETPOINT": equipment.set_point}
                #api.publish(payload, equipment.device_id, equipment.serial_number)
                    #discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
    #for options in all_equipment:
    #    for key in options:
    #        options[key] = int(options[key])

    #for equip_list in all_equipment.values():
    #    print([equip_list])
    #    print("{}".format(all_equipment.values))
    #    print([all_equipment.values])
        #print("\n{}" .format(equipment.device_name))
    for equip_list in all_equipment.values():
        for equipment in equip_list:
            #discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
            #dict_values([[<pyeconet.equipment.water_heater.WaterHeater object at 0x10d4ed410>]])  
            print(f"\nName: {equipment.device_name}\n")
            print("{}" .format(equipment.set_point))
            payload = {"@SETPOINT": equipment.set_point}
            print(all_equipment (equipment.set_point))


    """await asyncio.sleep(5)
    for equip_list in all_equipment.values():
        for equipment in equip_list:
    #        pass
            print(f"\nName: {equipment.device_name}\n")
            print(f"\nSet point: {equipment.set_point}\n")
            print(f'{equipment.set_point}')
            print(f"\nSupports modes: {equipment._supports_modes()}\n")
            print(f"\nOperation modes: {equipment.modes}\n")
            print(f"\nOperation mode: {equipment.mode}\n")
            #print(f"\nOperation mode: {WaterHeaterOperationMode}\n")
            print(f"\nDevice id: {equipment.device_id}\n")
            print(f"\nSerial #: {equipment.serial_number}\n")
            print(f"\nDevice Mode: {equipment.mode}\n")
            #print(f"\All Values:{all_equipment.values}\n")
            #print(f"\nSerial #: {equipment.device_type}\n")
            #await equipment._get_energy_usage()
            "{equipment.set_point == 20}"
            #equipment.set_mode(OperationMode.GAS)
            #payload = {"@SETPOINT": set_point}
    #await asyncio.sleep(300000)
    #api.unsubscribe()"""



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
