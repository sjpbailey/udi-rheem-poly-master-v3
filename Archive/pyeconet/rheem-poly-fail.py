

"""
Get the polyinterface objects we need.  Currently Polyglot Cloud uses
a different Python module which doesn't have the new LOG_HANDLER functionality
"""
try:
    import polyinterface
    from polyinterface import Controller,LOG_HANDLER,LOGGER
import logging
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

from pyeconet import EcoNetApiInterface, equipment
from pyeconet.equipment import EquipmentType #pyeconet.equipment
#from pyeconet.equipment.water_heater import WaterHeater
from pyeconet.equipment import Equipment


# IF you want a different log format than the current default
LOG_HANDLER.set_log_format('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')
class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        """
        Optional.
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.
        """
        super(Controller, self).__init__(polyglot)
        self.name = 'Rheem'
        self.hb = 0
        

    def start(self):
        serverdata = self.poly.get_server_data(check_profile=True)
        #serverdata['version'] = "testing"
        LOGGER.info('Started Water Heater NodeServer {}'.format(serverdata['version']))
        # Show values on startup if desired.
        #all_equipment = None
        LOGGER.debug('ST=%s',self.getDriver('ST'))
        self.setDriver('ST', 1)
        self.heartbeat(0)
        self.check_params()
        self.set_debug_level(self.getDriver('GV1'))
        self.discover()
        self.poly.add_custom_config_docs("<b>This is some custom config docs data</b>")
        

    def shortPoll(self):
        self.discover()
        LOGGER.debug('shortPoll')
        for node in self.nodes:
            if node != self.address:
                self.nodes[node].shortPoll()

    def longPoll(self):
        LOGGER.debug('longPoll')
        self.heartbeat()

    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    async def get_request(self, url):
        api = await EcoNetApiInterface.login(self.email, self.password)
        all_equipment = await api.get_equipment_by_type([EquipmentType.WATER_HEATER])
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        api = await EcoNetApiInterface.login(self.email, self.password)
                        
                    ) as _response:
                        if _response.status != 204:
                            await _response.read()
                        else:
                            return _response
        except (Exception, TimeoutError):
            self.logger.exception("Failed to communicate with server.")
            #raise BadfishException
        return _response 
            
    def discover(self, *args, **kwargs,):
        if self.password is not None:
            all_equipment = [EquipmentType.WATER_HEATER]

        
        
            LOGGER.info("{}" .format(equipment))
            self.setDriver('GV2',"{}" .format(equipment))
        
        #self.addNode(TemplateNode(self, self.address, 'templateaddr', 'Template Node Name'))

    def delete(self):
        LOGGER.info('deleted Rheem Econet.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config))
        LOGGER.info("process_config: Exit")

    def heartbeat(self,init=False):
        LOGGER.debug('heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def set_module_logs(self,level):
        logging.getLogger('urllib3').setLevel(level)

    def set_debug_level(self,level):
        LOGGER.debug('set_debug_level: {}'.format(level))
        if level is None:
            level = 30
        level = int(level)
        if level == 0:
            level = 30
        LOGGER.info('set_debug_level: Set GV1 to {}'.format(level))
        self.setDriver('GV1', level)
        # 0=All 10=Debug are the same because 0 (NOTSET) doesn't show everything.
        if level <= 10:
            LOGGER.setLevel(logging.DEBUG)
        elif level == 20:
            LOGGER.setLevel(logging.INFO)
        elif level == 30:
            LOGGER.setLevel(logging.WARNING)
        elif level == 40:
            LOGGER.setLevel(logging.ERROR)
        elif level == 50:
            LOGGER.setLevel(logging.CRITICAL)
        else:
            LOGGER.debug("set_debug_level: Unknown level {}".format(level))
        
        if level < 10:
            LOG_HANDLER.set_basic_config(True,logging.DEBUG)
        else:
            # This is the polyinterface default
            LOG_HANDLER.set_basic_config(True,logging.WARNING)

    def check_params(self):
        """
        This is an example if using custom Params for user and password and an example with a Dictionary
        """
        self.removeNoticesAll()
        #self.addNotice('Hey there, my IP is {}'.format(self.poly.network_interface['addr']),'hello')
        #self.addNotice('Hello Friends! (without key)')
        default_email = "YourEMail"
        default_password = "YourPassword"
        

        if 'email' in self.polyConfig['customParams']:
            self.email = self.polyConfig['customParams']['email']
        else:
            self.email = default_email
            LOGGER.error('check_params: email not defined in customParams, please add it.  Using {}'.format(self.email))

        if 'password' in self.polyConfig['customParams']:
            self.password = self.polyConfig['customParams']['password']
        else:
            self.password = default_password
            LOGGER.error(
                'check_params: password not defined in customParams, please add it.  Using {}'.format(self.password))

    # Make sure they are in the params
        self.addCustomParam({'password': self.password, 'user': self.user,
                            'isy_ip': self.isy_ip, 'debug_enable': self.debug_enable})

        # Add a notice if they need to change the user/password from the default.
        if self.user == default_email or self.password == default_password:
            self.addNotice('Please set proper user, password and ISY IP '
                        'in configuration page, and restart this nodeserver')
            st = False        

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def cmd_set_debug_mode(self,command):
        val = int(command.get('value'))
        LOGGER.debug("cmd_set_debug_mode: {}".format(val))
        self.set_debug_level(val)

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'SET_DM': cmd_set_debug_mode,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 10, 'uom': 25},
        {'driver': 'GV2', 'value': 1, 'uom': 56}, # Debug (Log) Mode, default=30=Warning
    ]

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Tankless')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
        

    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
