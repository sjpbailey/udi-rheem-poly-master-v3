

import udi_interface
import sys
import time
import urllib3

import xml.etree.ElementTree as ET
import asyncio
import logging

import requests
from requests.auth import HTTPBasicAuth #HTTP

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER
Custom = udi_interface.Custom
ISY = udi_interface.ISY 

LOG_HANDLER.set_log_format('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')

class RheemController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(RheemController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = 'Rheem Water Heater'  # override what was passed in
        self.hb = 0
        self.Parameters = Custom(polyglot, 'customparams')
        self.Notices = Custom(polyglot, 'notices')
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.poly.ready()
        self.poly.addNode(self)
        # Attributes
        self.email = None
        self.password = None
        self.isy_ip = None

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()    

    def start(self):
        #self.poly.updateProfile()
        self.discover()

    def discover(self, *args, **kwargs):
        pass

    async def goNow(self):
    
    #email = "" #input("Enter your email: ").strip()
    #password = "" #getpass.getpass(prompt='Enter your password: ')  
    
            api = await EcoNetApiInterface.login(email, password)
            all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
            try:
                #r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
                api = await EcoNetApiInterface.login(email, password=password)
                r = all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
                for equip_list in all_equipment.values():
                    for equipment in equip_list:
                        LOGGER.info(f"\nName: {equipment.device_name}\n")
                        LOGGER.info(f"\nSerial #: {equipment.serial_number}\n")
                        LOGGER.info(f"\nOperation mode: {equipment.device_id}\n")
                        LOGGER.info(f"\nSet point: {equipment.set_point}\n")
                        LOGGER.info(f"\nOperation mode: {equipment.mode}\n")
                        LOGGER.info(f"\nOperation modes: {equipment.modes}\n")
                

                    return equip_list
                else:
                    print.error("Rheem Econet Error:  " + equip_list)
                    return None

            except Exception as e:
                LOGGER.info("Error: " + str(e))

    def delete(self):
        LOGGER.info('Deleting AMI NEM, Net Energy Meter')

    def stop(self):
        LOGGER.debug('AMI NEM NodeServer stopped.')

    def set_module_logs(self,level):
        LOGGER.getLogger('urllib3').setLevel(level)

    def check_params(self):
        """
        This is an example if using custom Params for user and password and an example with a Dictionary
        """
        self.Notices.clear()
        #self.Notices['hello'] = 'Hey there, my IP is {}'.format(self.poly.network_interface['addr'])
        #self.Notices['hello2'] = 'Hello Friends!'
        default_email = "Youremail"
        default_password = "YourPassword"

        self.email = self.Parameters.email
        if self.email is None:
            self.email = default_email
            LOGGER.error('check_params: email not defined in customParams, please add it.  Using {}'.format(default_email))
            self.email = default_email

        self.password = self.Parameters.password
        if self.password is None:
            self.password = default_password
            LOGGER.error('check_params: password not defined in customParams, please add it.  Using {}'.format(default_password))
            self.password = default_password

        # Add a notice if they need to change the user/password from the default.
        if self.email == default_email or self.password == default_password:
            self.Notices['auth'] = 'Please set proper user and password in configuration page'
            #self.Notices['test'] = 'This is only a test' 

    def goNow(self):
        #LOGGER.debug("Query sensor {}".format(self.address))
        asyncio.run(self.querynodes())
        #self.reportDrivers() 
    
    def query(self, command=None):
        nodes = self.poly.getNodes()
        for node in nodes:
            nodes[node].reportDrivers()

    def poll(self, flag):
        nodes = self.poly.getNodes()
        for node in nodes:
            nodes[node].reportDrivers()
            self.discover()
        if 'longPoll' in flag:
            LOGGER.debug('longPoll (controller)')
        else:
            LOGGER.debug('shortPoll (controller)')
            

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.Notices))
        # Remove all existing notices
        self.Notices.clear()

    id = 'controller'
    
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'GONOW': goNow,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        
    ]

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([RheemController])
        polyglot.start()
        control = RheemController(polyglot, 'controller', 'controller', 'RheemContoller')
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
        polyglot.stop()
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
    sys.exit(0)
    