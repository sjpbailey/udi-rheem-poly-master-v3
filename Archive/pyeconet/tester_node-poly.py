import asyncio
import logging
import aiohttp
import json
#import time
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
    password = "AcxessExess61!"
    api = await EcoNetApiInterface.login(email, password=password)
    # , EquipmentType.THERMOSTAT
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])

    api.subscribe()
    await asyncio.sleep(5)
    for equip_list in all_equipment.values():
        for equipment in equip_list:
            discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
    #        dict_values([[<pyeconet.equipment.water_heater.WaterHeater object at 0x10d4ed410>]])
    #            print(f"\nName: {all_equipment.values}")
    #            print("\n{equipment}")
    #            print("\n" f"{all_equipment.values}")
    #            print("\n{}" .format(equipment.device_name))
    #            print(f"\nName: {equipment.device_name}\n")
    #            print("\n")
            print("{}" .format(equipment.set_point))
    # 3print("{}" .format(equipment.modes))
    # 4print("{}" .format(equipment.device_id))
    # 5print("{}" .format(equipment.serial_number))
    # 6print("{}" .format(equipment.mode))
    # 7print("{}" .format(all_equipment.values))
    #print("{}" .format(logging.basicConfig()))
    # print(logging.getLogger().setLevel(logging.DEBUG))
    #payload = {"@SETPOINT": equipment.set_point}
    #(payload, equipment.device_id, equipment.serial_number)
    #discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
    # for options in all_equipment:
    #    for key in options:
    #        options[key] = int(options[key])

    # for equip_list in all_equipment.values():
    #    print([equip_list])
    #    print("{}".format(all_equipment.values))
    #    print([all_equipment.values])
    #print("\n{}" .format(equipment.device_name))
    for equip_list in all_equipment.values():
        for equipment in equip_list:
            #discover: {'address': 'controller', 'cmd': 'DISCOVER', 'query': {}}
            # dict_values([[<pyeconet.equipment.water_heater.WaterHeater object at 0x10d4ed410>]])
            # equipment.set_set_point()
            print(f"\nName: {equipment.device_name}\n")
            print("{}" .format(equipment.set_set_point))
            print(f"\nOperation mode: {equipment.modes[0]}\n")

            # payload = json.loads(equipment.set_set_point + 1) #payload = 140
            # _mqtt_client.publish(
            #    f"user/{self._account_id}/device/desired", payload=json.dumps(publish_payload))
            # AttributeError: 'NoneType' object has no attribute 'publish'
            # equipment.set_set_point(equipment.set_set_point(135),
            #                        'device_id', 'serial_number')
            #payload =  equipment.set_point(130) #json.dumps({"@SETPOINT": equipment.set_point})

            equipment.set_set_point(135)
            print("{}" .format(equipment.set_point))
            # print(json.dump)
            #print(all_equipment,{equipment.device_name}, {equipment.set_point==130})
            # print(pyeconet.api)
            # print(f"user/{equipment.user_id}/device/desired")

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
            print(f"\nOperation mode: {WaterHeaterOperationMode}\n")
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
