
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

""" MODES
    OFF = 1
    ELECTRIC_MODE = 2
    ENERGY_SAVING = 3
    HEAT_PUMP_ONLY = 4
    HIGH_DEMAND = 5
    GAS = 6
    ENERGY_SAVER = 7
    PERFORMANCE = 8
    VACATION = 9
    ELECTRIC = 10
    HEAT_PUMP = 11
    UNKNOWN = 99"""

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
        self.goNow(self)
        self.http = urllib3.PoolManager()

    # Data Grab from API
    async def getInformed(self):
        api = await EcoNetApiInterface.login(self.email, self.password)
        all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        try:
            api = await EcoNetApiInterface.login(self.email, password=self.password)
            r = all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    LOGGER.info(f"\nName: {equipment.device_name}\n")
                    
                    LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                    self.setDriver('GV1', str(f"{equipment.set_point}"))
                    
                    LOGGER.info(f"\nOperation mode: {equipment.mode.value}\n")  # Operation mode: WaterHeaterOperationMode.GAS
                    self.setDriver('GV2', int(f"{equipment.mode.value}"))

                    LOGGER.info(f"\nSerial #: {equipment.serial_number}\n")
                    self.setDriver('GV3', str(f"{equipment.serial_number}"))
                    
                    LOGGER.info(f"\nOperation modes: {equipment.modes}\n")  # Operation modes: [<WaterHeaterOperationMode.OFF: 1>, <WaterHeaterOperationMode.GAS: 6>]
                    self.setDriver('GV4', str(f"{equipment.modes}"))
                    
                    #LOGGER.info("{}" .format(f"{equipment.set_point}"))
                    
                    LOGGER.info(f"\nOperation mode: {equipment.device_id}\n")
                    self.setDriver('GV5', str(f"{equipment.device_id}"))

                    LOGGER.info(f"\nEnabled: {equipment.enabled}\n")
                    if str(f"{equipment.enabled}") == 1:
                        self.setDriver('GV6', 1)
                    else:
                        self.setDriver('GV6', 0)

                return equip_list
            else:
                print.error("Rheem Econet Error:  " + equip_list)
                return None
        except Exception as e:
            LOGGER.info("Error: " + str(e))

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.reportDrivers()
        else:
            self.goNow(self)
            LOGGER.debug('longPoll (node)')
        
        # commands here
    
    def goNow(self, command):
        #LOGGER.debug("Query sensor {}".format(self.address))
        asyncio.run(self.getInformed())
        #self.reportDrivers()     

    def query(self,command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 17},
        {'driver': 'GV2', 'value': 0, 'uom': 25 },
        {'driver': 'GV3', 'value': 0, 'uom': 56 },
        {'driver': 'GV4', 'value': 0, 'uom': 25},
        {'driver': 'GV5', 'value': 0, 'uom': 56},
        {'driver': 'GV6', 'value': True, 'uom': 2},
        ]

    id = 'rheemnodeid'

    commands = {
                    'GONOW': goNow
                    
                }
