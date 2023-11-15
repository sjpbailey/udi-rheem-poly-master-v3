#!/usr/bin/env python
"""
This is a NodeServer template for Polyglot v2 written in Python2/3
by Einstein.42 (James Milne) milne.james@gmail.com
"""
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import requests
from requests.auth import HTTPBasicAuth #HTTP
import xml.etree.ElementTree as ET
import re

import asyncio
import aiohttp
import logging

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType #pyeconet.equipment
from pyeconet.equipment.water_heater import WaterHeater


LOGGER = polyinterface.LOGGER
"""
polyinterface has a LOGGER that is created by default and logs to:
logs/debug.log
You can use LOGGER.info, LOGGER.warning, LOGGER.debug, LOGGER.error levels as needed.
"""

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        """
        Optional.
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.
        """
        super(Controller, self).__init__(polyglot)
        self.name = 'Rheem'
        self.poly.onConfig(self.process_config)
        self.debug_enable = 'False'

    def start(self):
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
        # This grabs the server.json data and checks profile_version is up to date
        serverdata = self.poly.get_server_data()
        LOGGER.info('Started Water Heater NodeServer {}'.format(serverdata['version']))
        self.check_params()
        self.discover()
        self.poly.add_custom_config_docs("<b>And this is some custom config data</b>")

    def shortPoll(self):
        
        pass

    def longPoll(self):
        
        pass

    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    """async def get_request(self, url):
        email = self.email
        password = self.password
        api = await EcoNetApiInterface.login(email, password=password)
        all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        all_equipment = ([EquipmentType.WATER_HEATER])
        #api.subscribe()
        #await asyncio.sleep(5)"""
        

    async def get_request(self, url):
        try:
            r = requests.get(url, auth=aiohttp.BasicAuth(api = await EcoNetApiInterface.login(self.email, self.password)))
            if r.status_code == requests.codes.ok:
                if self.debug_enable == 'True' or self.debug_enable == 'true':
                    print(r.content)

                return r.content
            else:
                LOGGER.error("ISY-Inventory.get_request:  " + r.content)
                return None

        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))

    def discover(self, *args, **kwargs):
        if self.email is not None:
            pass
            #api = await EcoNetApiInterface.login(email, password=password)
            #all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER]) #, EquipmentType.THERMOSTAT
            #api.subscribe()
            #await asyncio.sleep(5)
            """all_equipment = ({"EquipmentType.WATER_HEATER"})
            for equip_list in all_equipment():
                    for equipment in equip_list:
                        LOGGER.info(f"\nName: {equipment.device_name}\n")
                        LOGGER.info(f"\nStatus: {'@STATUS'}\n")
                        LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                #LOGGER.info(f"\nSupports modes: {equipment._supports_modes()}\n")
                #LOGGER.info(f"\nOperation modes: {equipment.modes}\n")
                #LOGGER.info(f"\nOperation mode: {equipment.mode}\n")
                #LOGGER.info(f"\nOperation mode: {WaterHeaterOperationMode}\n")
                #LOGGER.info(f"\nDevice id: {equipment.device_id}\n")
                #LOGGER.info(f"\nSerial #: {equipment.serial_number}\n")
                #LOGGER.info(f"\nDevice Mode: {equipment.mode}\n")
                #LOGGER.info(f"\All Values:{all_equipment.values}\n")
                #await equipment._get_energy_usage()
                #"{equipment.set_point == 20}"
                #equipment.set_mode(OperationMode.GAS)
                #await asyncio.sleep(300000)
                #api.unsubscribe()
        
                    status = "equipment.set_point"
                    self.setdriver('GV1', status)"""

        """
        Example
        Do discovery here. Does not have to be called discovery. Called from example
        controller start method and from DISCOVER command recieved from ISY as an exmaple.
        """
        #self.addNode(WaterHeater(self, self.address, 'waterheatid', 'Tankless Water Heater'))

    def delete(self):
        """
        Example
        This is sent by Polyglot upon deletion of the NodeServer. If the process is
        co-resident and controlled by Polyglot, it will be terminiated within 5 seconds
        of receiving this message.
        """
        LOGGER.info('Oh God I\'m being deleted. Nooooooooooooooooooooooooooooooooooooooooo.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def check_params(self):
        st = True
        self.remove_notices_all()
        default_email = "YourEMail"
        default_password = "YourPassword"
        

        if 'email' in self.polyConfig['customParams']:
            self.email = self.polyConfig['customParams']['email']
        else:
            self.email = default_email
            LOGGER.error('check_params: email not defined in customParams, please add it.  Using {}'.format(self.email))
            st = False

        if 'password' in self.polyConfig['customParams']:
            self.password = self.polyConfig['customParams']['password']
        else:
            self.password = default_password
            LOGGER.error(
                'check_params: password not defined in customParams, please add it.  Using {}'.format(self.password))
            st = False

        
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']

        # Make sure they are in the params
        self.addCustomParam({'password': self.password, 'email': self.email,
                            'debug_enable': self.debug_enable})

        # Add a notice if they need to change the email/password from the default.
        if self.email == default_email or self.password == default_password:
            self.addNotice('Please set proper email, password and ISY IP '
                        'in configuration page, and restart this nodeserver')
            st = False

        if st:
            return True
        else:
            return False

    def remove_notices_all(self):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self, command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    """
    Optional.
    Since the controller is the parent node in ISY, it will actual show up as a node.
    So it needs to know the drivers and what id it will use. The drivers are
    the defaults in the parent Class, so you don't need them unless you want to add to
    them. The ST and GV1 variables are for reporting status through Polyglot to ISY,
    DO NOT remove them. UOM 2 is boolean.
    The id must match the nodeDef id="controller"
    In the nodedefs.xml
    """
    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        #'REMOVE_NOTICE_TEST': remove_notice_test
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 17}
        ]



"""class WaterHeater(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        
        #Optional.
        #Super runs all the parent class necessities. You do NOT have
        #to override the __init__ method, but if you do, you MUST call super.

        #:param controller: Reference to the Controller class
        #:param primary: Controller address
        #:param address: This nodes address
        #:param name: This nodes name
        
        super(WaterHeater, self).__init__(controller, primary, address, name)

    def start(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        async def main():
            email = "" #input("Enter your email: ").strip()
            password = "" #getpass.getpass(prompt='Enter your password: ')
            api = EcoNetApiInterface.login(email, password=password)
            all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER]) #, EquipmentType.THERMOSTAT
            api.subscribe()
            await asyncio.sleep(5)
            for equip_list in all_equipment.values():
                for equipment in equip_list:
                    LOGGER.info(f"\nName: {equipment.device_name}\n")
                    LOGGER.info(f"\nStatus: {'@STATUS'}\n")
                    LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                #LOGGER.info(f"\nSupports modes: {equipment._supports_modes()}\n")
                #LOGGER.info(f"\nOperation modes: {equipment.modes}\n")
                #LOGGER.info(f"\nOperation mode: {equipment.mode}\n")
                #LOGGER.info(f"\nOperation mode: {WaterHeaterOperationMode}\n")
                #LOGGER.info(f"\nDevice id: {equipment.device_id}\n")
                #LOGGER.info(f"\nSerial #: {equipment.serial_number}\n")
                #LOGGER.info(f"\nDevice Mode: {equipment.mode}\n")
                #LOGGER.info(f"\All Values:{all_equipment.values}\n")
                #await equipment._get_energy_usage()
                #"{equipment.set_point == 20}"
                #equipment.set_mode(OperationMode.GAS)
                #await asyncio.sleep(300000)
                #api.unsubscribe()
        
        
        #Optional.
        #This method is run once the Node is successfully added to the ISY
        #and we get a return result from Polyglot. Only happens once.
                LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                status = "equipment.set_point"
                self.setdriver('GV1', status)
                self.setDriver('ST', 1)
        

    
        
    
    def setOn(self, command):
        
        #Example command received from ISY.
        #Set DON on TemplateNode.
        #Sets the ST (status) driver to 1 or 'True'
        
        self.setDriver('ST', 1)

    def setOff(self, command):
        
        #Example command received from ISY.
        #Set DOF on TemplateNode
        #Sets the ST (status) driver to 0 or 'False'
        
        self.setDriver('ST', 0)

    def query(self,command=None):
        
        #Called by ISY to report all drivers for this node. This is done in
        #the parent class, so you don't need to override this method unless
        #there is a need.
        
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 17},
        ]
    
    #Optional.
    #This is an array of dictionary items containing the variable names(drivers)
    #values and uoms(units of measure) from ISY. This is how ISY knows what kind
    #of variable to display. Check the UOM's in the WSDK for a complete list.
    #UOM 2 is boolean so the ISY will display 'True/False'
    
    id = 'waterheatid'
    
    #id of the node from the nodedefs.xml that is in the profile.zip. This tells
    #the ISY what fields and commands this node has.
    
    commands = {
                    'DON': setOn, 'DOF': setOff
                }
    
    #This is a dictionary of commands. If ISY sends a command to the NodeServer,
    #this tells it which method to call. DON calls setOn, etc."""
    

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Tankless')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(())
        

    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
