
import udi_interface
import sys
import time
import urllib3
import asyncio
import logging

import requests
from requests.auth import HTTPBasicAuth #HTTP

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType

LOGGER = udi_interface.LOGGER

class RheemNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, email, password):
        super(RheemNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address,name)
        

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.email = email
        self.password = password

    def start(self):
        
        self.http = urllib3.PoolManager()

    async def getInformed(self):
        #self.email = email
        #self.password = password
    
        #email = "sjpbailey@comcast.net" #input("Enter your email: ").strip()
        #password = "NatiqueRheem61" #getpass.getpass(prompt='Enter your password: ')  
    
        api = await EcoNetApiInterface.login(self.email, self.password)
        all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        try:
            #r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
            api = await EcoNetApiInterface.login(self.email, password=self.password)
            r = all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    LOGGER.info(f"\nName: {equipment.device_name}\n")
                    LOGGER.info(f"\nSerial #: {equipment.serial_number}\n")
                    LOGGER.info(f"\nOperation mode: {equipment.device_id}\n")
                    LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                    LOGGER.info(f"\nOperation mode: {equipment.mode}\n")
                    LOGGER.info(f"\nOperation modes: {equipment.modes}\n")
                    LOGGER.info("{}" .format(f"{equipment.set_point}"))
                    #time.sleep(1)
                    self.setDriver('GV1', str("{}" .format(f"{equipment.set_point}"))  # self.setDriver('GV1', str(f"{equipment.set_point}"))

                return equip_list
            else:
                print.error("Rheem Econet Error:  " + equip_list)
                return None
        except Exception as e:
            LOGGER.info("Error: " + str(e))

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')
            self.goNow(self)

    def cmd_on(self, command):
        self.setDriver('ST', 1)

    def cmd_off(self, command):
        self.setDriver('ST', 0)

    def goNow(self, command):
        #LOGGER.debug("Query sensor {}".format(self.address))
        asyncio.run(self.getInformed())
        #self.reportDrivers()     

    def query(self,command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 17},
        ]

    id = 'rheemnodeid'

    commands = {
                    'DON': cmd_on,
                    'DOF': cmd_off,
                    'GONOW': goNow
                    
                }
