
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
                    
                    LOGGER.info(f"\nDevice Id: {equipment.device_id}\n")
                    self.setDriver('GV5', str(f"{equipment.device_id}"))

                    LOGGER.info(f"\nEnabled: {equipment.enabled}\n")
                    if equipment.enabled == True:
                        self.setDriver('GV6', 1)
                    if equipment.enabled == False:
                        self.setDriver('GV6', 0)
                        
    # Stop Power Down Heater
    async def offHeat(self, command):
            api = await EcoNetApiInterface.login(self.email, self.password)
            all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            api.subscribe()
            await asyncio.sleep(5)
        
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    equipment.set_mode(1)
                    if equipment.enabled == False:
                        self.setDriver('GV6', 0)
                    
    # Stop Power Down Heater
    async def onHeat(self, command):
            api = await EcoNetApiInterface.login(self.email, self.password)
            all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            api.subscribe()
            await asyncio.sleep(5)
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    equipment.set_mode(6)
                    if equipment.enabled == True:
                        self.setDriver('GV6', 1)
        

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.reportDrivers()
        else:
            self.query()
            LOGGER.debug('longPoll (node)')
        
        # commands here
    
    def goNow(self, command):
        asyncio.run(self.getInformed())

    def goSet(self, command):
        asyncio.run(self.setTemp(command))
        time.sleep(5)
        asyncio.run(self.setTemp(command))
        
    def stop(self,command):
        asyncio.run(self.offHeat(command))
        
    def start(self,command):
        asyncio.run(self.onHeat(command))
    
    def query(self,command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': 'Online'},
        {'driver': 'GV1', 'value': 0, 'uom': 17, 'name': 'Setpoint'},
        {'driver': 'GV2', 'value': 0, 'uom': 25, 'name': 'Mode'},
        #{'driver': 'GV3', 'value': 0, 'uom': 56, 'name': 'Serial'},
        {'driver': 'GV4', 'value': 0, 'uom': 25, 'name': 'Modes'},
        #{'driver': 'GV5', 'value': 0, 'uom': 56, 'name': 'ID'},
        {'driver': 'GV6', 'value': 0, 'uom': 2, 'name': 'Enabled?'},
        {'driver': 'GV7', 'value': 0, 'uom': 17, 'name': 'Setpoint CMD'},
        ]

    id = 'rheemnode'

    commands = {
                    'GONOW': goNow,
                    'SETPT': goSet,
                    'QUERY': query,
                    'STOP': stop,
                    'START': start,
                    
                }
