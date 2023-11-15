import asyncio
import logging
#import time
#import getpass

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType
from pyeconet.equipment.water_heater import WaterHeaterOperationMode

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


async def main():
    email = ""  # input("Enter your email: ").strip()
    # getpass.getpass(prompt='Enter your password: ')
    password = "access!"
    api = await EcoNetApiInterface.login(email, password=password)
    # , EquipmentType.THERMOSTAT
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
    api.subscribe()
    await asyncio.sleep(5)
    # print(all_equipment)
    max_temp = None
    for equip_list in all_equipment.values():
        for equipment in equip_list:
            #equipment.min_temp(85)
            #equipment.max_temp(130)
            equipment.set_set_point(125)
            # equipment.set_set_point(equipment._api.publish(str(
            # equipment.max_temp == 135, equipment.device_id, equipment.serial_number)))
            equipment.set_set_point(140)
            print("{}" .format(equipment.set_point))
            equipment.operation_mode = False
            print(equipment.max_temp)
            print(equipment.min_temp)
            print(equipment.set_point)
            print(equipment.energy_usage)

            #["results"]["locations"][0]["equiptments"][0]['@SETPOINT']['value'] = 137
            print(f"\nName: {equipment.device_name}\n")
            print(
                f"\nSet point: {equipment.set_point} {equipment.set_set_point}\n")
            #print(f"\nSupports modes: {equipment._supports_modes}\n")
            print(f"\nOperation modes: {equipment.modes}\n")
            print(f"\nOperation mode: {equipment.mode}\n")
            #print(f"\nOperation mode: {WaterHeaterOperationMode}\n")
            print(f"\nDevice id: {equipment.device_id}\n")
            print(f"\nSerial #: {equipment.serial_number}\n")
            print(f"\nDevice Mode: {equipment.mode}\n")
            # print(f"\nSerial #: {equipment.device_type}\n")
            # await equipment._get_energy_usage()
            # equipment.set_mode(OperationMode.GAS)
            # await asyncio.sleep(300000)
            # api.unsubscribe()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
