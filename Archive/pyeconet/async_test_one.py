import asyncio

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType


# import getpass


# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)

async def main():
    email = "sjpbailey@comcast.net"  # input("Enter your email: ").strip()
    # getpass.getpass(prompt='Enter your password: ')
    password = "AcxessExess61!"
    api = await EcoNetApiInterface.login(email, password)
    all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])

    try:
        # r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
        api = await EcoNetApiInterface.login(email, password=password)
        r = all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        # w = all_equipment = await api.post_equipment_by_type([EquipmentType.WATER_HEATER])

        for equip_list in all_equipment.values():
            for equipment in equip_list:
                # print(str(equip_list))
                print(f"\nName: {equipment.device_name}\n")
                print(f"\nSerial #: {equipment.serial_number}\n")
                print(f"\nDevice ID: {equipment.device_id}\n")
                print(f"\nSet point: {equipment.set_point}\n")
                print(f"\nOperation mode: {equipment.mode}\n")
                print(f"\nOperation modes: {equipment.modes}\n")
                print(f"\nRunning ?: {equipment.running_state}\n")
                print(str(equipment.modes[-1]))
                print(str(equipment.modes[0]))  # WaterHeaterOperationMode.OFF
                print(str(equipment.modes[::]))  # WaterHeaterOperationMode.OFF
                print(str(equipment.device_id))  # # "{}".format(var2,var1))
                
                # print(f"\nOperation modes: {equipment.phone_number}\n") #WaterHeaterOperationMode
                # print(type({equipment}))
                # print(f"\nOperation modes: {equipment}\n") #set_point_limits
                # print(f"\nOperation modes: {equipment}\n")
                # equipment.set_set_point(api.publish(130, {equipment.device_id}, {equipment.serial_number}))
                # api.publish(0, {equipment.device_id}, {equipment.serial_number})
                # print(type({equipment.set_point}))
                # speedE2 = 'Speed -' + str(speed)
                #set_point = 137
                #a = str(a)
                if equipment.set_point is not None:
                    print(equipment.set_point)
                else:
                    pass
                equipment.set_set_point(136+1)
                #equipment.set_set_point(equipment.set_point + 1)
                #equipment.set_set_point(120)
                # await asyncio.sleep(300000)
                # WaterHeaterOperationMode.GAS #{}".format(var2,var1))
                
                # api:["results"]["locations"][0]["equiptments"][0]['@SETPOINT']['value'] = '135'

                # equipment._api.publish({equipment.set_point}, {equipment.device_id}, {equipment.serial_number})
                print(equipment.set_point)

            return equip_list

        else:
            print.error("Rheem Econet Error:  " + r)
            return None

    except Exception as e:
        print("Error: " + str(e))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
