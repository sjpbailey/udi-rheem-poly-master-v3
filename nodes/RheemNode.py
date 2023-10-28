
from tempfile import gettempdir
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
        self.query()
        self.http = urllib3.PoolManager()

    # Temperature Setpoint Statuses
    async def setTemp(self, command):
        ivr_one = 'percent'
        percent = int(command.get('value'))

        def set_percent(self, command):
            percent = int(command.get('value')*10)
        if percent < 110 or percent > 140:
            LOGGER.error('Invalid Level {}'.format(percent))
        else:
            self.setDriver('GV7', percent)
            api = await EcoNetApiInterface.login(self.email, self.password)
            all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            api.subscribe()
            await asyncio.sleep(5)
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    equipment.set_set_point(percent)
                    LOGGER.info("{}" .format(equipment.set_point))
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
                    
                    LOGGER.info(f"\nDevice Id: {equipment.device_id}\n")
                    self.setDriver('GV5', str(f"{equipment.device_id}"))

                    LOGGER.info(f"\nEnabled: {equipment.enabled}\n")
                    if str(f"{equipment.enabled}") == 1:
                        self.setDriver('GV6', 1)
                    else:
                        self.setDriver('GV6', 0)
                    
        
        return percent
        LOGGER.info(percent)
        
    # Data Grab from API
    """async def getInformed(self):
        #percent = percent=setTemp
        #LOGGER.info(percent)
        api = await EcoNetApiInterface.login(self.email, self.password)
        all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        api.subscribe()
        await asyncio.sleep(5)
        for equip_list in all_equipment.values():
            for equipment in equip_list:
                #equipment.set_set_point(115)
                LOGGER.info("{}" .format(equipment.set_point))
        try:
            api = await EcoNetApiInterface.login(self.email, password=self.password)
            all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            api.subscribe()
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    LOGGER.info(f"\nName: {equipment.device_name}\n")
                    #equipment.set_set_point(137)
                    LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                    self.setDriver('GV1', str(f"{equipment.set_point}"))
                    #LOGGER.info(f"\nDriver GV7:" 'GV7')
                    
                    LOGGER.info(f"\nOperation mode: {equipment.mode.value}\n")  # Operation mode: WaterHeaterOperationMode.GAS
                    self.setDriver('GV2', int(f"{equipment.mode.value}"))

                    LOGGER.info(f"\nSerial #: {equipment.serial_number}\n")
                    self.setDriver('GV3', str(f"{equipment.serial_number}"))
                    
                    LOGGER.info(f"\nOperation modes: {equipment.modes}\n")  # Operation modes: [<WaterHeaterOperationMode.OFF: 1>, <WaterHeaterOperationMode.GAS: 6>]
                    self.setDriver('GV4', str(f"{equipment.modes}"))
                    
                    #LOGGER.info("{}" .format(f"{equipment.set_point}"))
                    
                    LOGGER.info(f"\nDevice Id: {equipment.device_id}\n")
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
            LOGGER.info("Error: " + str(e))"""

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.reportDrivers()
        else:
            self.query()
            LOGGER.debug('longPoll (node)')
        
        # commands here
    
    def goNow(self, command):
        #LOGGER.debug("Query sensor {}".format(self.address))
        asyncio.run(self.getInformed())
        #self.reportDrivers()
        
    def goSet(self, command):
        asyncio.run(self.setTemp(command))
    
    def query(self,command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': 'Online'},
        {'driver': 'GV1', 'value': 0, 'uom': 17, 'name': 'Setpoint'},
        {'driver': 'GV2', 'value': 0, 'uom': 25, 'name': 'Mode'},
        {'driver': 'GV3', 'value': 0, 'uom': 56, 'name': 'Serial'},
        {'driver': 'GV4', 'value': 0, 'uom': 25, 'name': 'Modes'},
        {'driver': 'GV5', 'value': 0, 'uom': 56, 'name': 'ID'},
        {'driver': 'GV6', 'value': True, 'uom': 2, 'name': 'Enabled?'},
        {'driver': 'GV7', 'value': 0, 'uom': 17, 'name': 'Setpoint CMD'},
        ]

    id = 'rheemnode'

    commands = {
                    'GONOW': goNow,
                    'SETPT': goSet,
                    'QUERY': query,
                    
                }
