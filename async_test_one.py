import asyncio
import logging
#import time
#import getpass
import json
import requests
from requests.auth import HTTPBasicAuth  # HTTP

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType

logging.basicConfig()  # format='%(asctime)s %(message)s'
logging.getLogger().setLevel(logging.DEBUG)


async def main():

    email = "email"  # input("Enter your email: ").strip()
    # getpass.getpass(prompt='Enter your password: ')
    password = "password"
    api = await EcoNetApiInterface.login(email, password)
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])

    # print([EquipmentType.WATER_HEATER]) #[<EquipmentType.WATER_HEATER: 1>] so if greater than 2 addNode water heater

    try:
        #r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
        api = await EcoNetApiInterface.login(email, password=password)
        r = all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        for equip_list in all_equipment.values():
            for equipment in equip_list:
                # equipment.set_mode(False)
                equipment.set_point(equipment._api.publish(
                    '140', {equipment.device_id}, {equipment.serial_number}))

                #print(equipment.set_point == 140)
                #print(equipment.set_set_point == 140)
                # equipment.set_set_point(equipment._api.publish(
                #    str(85), {equipment.device_id}, {equipment.serial_number}))

                # print({"results"})
                #equipment.set_set_point(equipment._api.publish(equipment.set_point ==85, {equipment.device_id}, {equipment.serial_number}))
                # print(f"\nActive: {equipment.location}\n") #Active: True
                # print(f"\nTests: {equipment} \n") # tanklessWaterHeater
                # print([0]["locations"][0]["@LOCATION_INFO"])
                """
                print(equip_list) # [<pyeconet.equipment.water_heater.WaterHeater object at 0x109154350>]
                print(f"\nActive: {equipment.active}\n") #Active: True
                print(f"\nName: {equipment.device_name}\n") #Name: Tankless Water Heater
                print(f"\nSerial #: {equipment.serial_number}\n") #Serial #: 40-9F-38-42-40-57-4160
                print(f"\nOperation mode: {equipment.device_id}\n") # Operation mode: 6309535886154236
                print({equipment.mode}) # {<WaterHeaterOperationMode.GAS: 6>}}
                print(f"\nModes: {equipment.modes}\n") # Modes: [<WaterHeaterOperationMode.OFF: 1>, <WaterHeaterOperationMode.GAS: 6>]
                print(f"\nRunning: {equipment.running}\n") # Running: False
                print(f"\nEnabled: {equipment.enabled}\n") # Enabled: True
                print({equipment.set_mode}) # {<bound method WaterHeater.set_mode of <pyeconet.equipment.water_heater.WaterHeater object at 0x10eb70f50>>}
                print(f"\nType: {equipment.generic_type} \n") # tanklessWaterHeater
                print("\n")
                print(("{}" .format(equipment.set_point==140), {equipment.device_id}, {equipment.serial_number})) # True {'6309535886154236'} {'40-9F-38-42-40-57-4160'} True when matching current setpoint
                print(f"\nSet point limits: {equipment.set_point_limits}\n") # Set point limits: (85, 140)
                print(f"\nSet point: {equipment.set_point}\n") # Set point: 138 (138 = or what current setpoint is)
                print("{}" .format(equipment.set_point ==138)) # True if equal to current setpoint
                print(f"\nSet Set point: {equipment.set_set_point}\n") # Set Set point: <bound method WaterHeater.set_set_point of <pyeconet.equipment.water_heater.WaterHeater object at 0x109154350>>
                """

            return equip_list
        else:
            print.error("Rheem Econet Error:  ")
            return None

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
