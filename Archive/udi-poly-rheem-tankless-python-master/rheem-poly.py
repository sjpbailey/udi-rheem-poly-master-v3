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
import asyncio
import aiohttp

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from pyeconet import EcoNetApiInterface, equipment
from pyeconet.equipment import EquipmentType #pyeconet.equipment
#from pyeconet.equipment.water_heater import WaterHeater
from pyeconet.equipment import Equipment

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'Template Controller'
        self.poly.onConfig(self.process_config)

    def start(self):
        """
        Optional.
        Polyglot v2 Interface startup done. Here is where you start your integration.
        This will run, once the NodeServer connects to Polyglot and gets it's config.
        In this example I am calling a discovery method. While this is optional,
        this is where you should start. No need to Super this method, the parent
        version does nothing.
        """
        # This grabs the server.json data and checks profile_version is up to date
        serverdata = self.poly.get_server_data()
        LOGGER.info('Started Template NodeServer {}'.format(serverdata['version']))
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
            

    def discover(self, *args, **kwargs):
        """
        Example
        Do discovery here. Does not have to be called discovery. Called from example
        controller start method and from DISCOVER command recieved from ISY as an exmaple.
        """
        self.addNode(WaterHeaterNode(self, self.address, 'waterheatid', 'Rheem Tankless'))

    def delete(self):
        LOGGER.info('deleted.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def check_params(self):
        self.removeNoticesAll()
        #self.addNotice('Hey there, my IP is {}'.format(self.poly.network_interface['addr']),'hello')
        #self.addNotice('Hello Friends! (without key)')
        default_email = "YourUserName"
        default_password = "YourPassword"
        
        if 'email' in self.polyConfig['customParams']:
            self.email = self.polyConfig['customParams']['email']
        else:
            self.user = default_email
            LOGGER.error('check_params: user not defined in customParams, please add it.  Using {}'.format(self.email))
            st = False

        if 'password' in self.polyConfig['customParams']:
            self.password = self.polyConfig['customParams']['password']
        else:
            self.password = default_password
            LOGGER.error('check_params: password not defined in customParams, please add it.  Using {}'.format(self.password))
            st = False
        # Make sure they are in the params
        self.addCustomParam({'password': self.password, 'email': self.user, 'some_example': '{ "type": "TheType", "host": "host_or_IP", "port": "port_number" }'})

        # Add a notice if they need to change the user/password from the default.
        if self.email == default_email or self.password == default_password:
            # This doesn't pass a key to test the old way.
            self.addNotice('Please set proper email and password in configuration page, and restart this nodeserver')
        # This one passes a key to test the new way.
        self.addNotice('This is a test','test')

    def remove_notice_test(self,command):
        LOGGER.info('remove_notice_test: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNotice('test')

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
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
        'REMOVE_NOTICE_TEST': remove_notice_test
    }
    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2}]



class WaterHeaterNode(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        
        super(WaterHeaterNode, self).__init__(controller, primary, address, name)

    def start(self):
        """
        Optional.
        This method is run once the Node is successfully added to the ISY
        and we get a return result from Polyglot. Only happens once.
        """
        self.setDriver('ST', 1)
        pass

    def setOn(self, command):
        """
        Example command received from ISY.
        Set DON on TemplateNode.
        Sets the ST (status) driver to 1 or 'True'
        """
        self.setDriver('ST', 1)

    def setOff(self, command):
        """
        Example command received from ISY.
        Set DOF on TemplateNode
        Sets the ST (status) driver to 0 or 'False'
        """
        self.setDriver('ST', 0)

    def query(self,command=None):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 2}]
    
    id = 'waterheatid'
    
    commands = {
                    'DON': setOn, 'DOF': setOff
                }

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Template')
        
        polyglot.start()
        """
        Starts MQTT and connects to Polyglot.
        """
        control = Controller(polyglot)
        """
        Creates the Controller Node and passes in the Interface
        """
        control.runForever()
        """
        Sits around and does nothing forever, keeping your program running.
        """
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
