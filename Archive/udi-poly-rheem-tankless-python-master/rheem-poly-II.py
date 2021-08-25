try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import bascontrol_ns
from bascontrol_ns import Device, Platform


LOGGER = polyinterface.LOGGER
class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'BASpi6u6r'
        self.ipaddress = None 
        self.debug_enable = 'False'
        self.poly.onConfig(self.process_config)
        

    def start(self):
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
        self.heartbeat(0)
        if self.check_params():
            self.discover()

    
    def shortPoll(self):
        self.discover()

    def longPoll(self):
        self.heartbeat()

    def query(self, command=None):
        self.discover()

    def get_request(self, url):
        try:
            r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
            if r.status_code == requests.codes.ok:
                if self.debug_enable == 'True' or self.debug_enable == 'true':
                    print(r.content)

                return r.content
            else:
                LOGGER.error("BASpi.get_request:  " + r.content)
                return None

        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
    
    class bc:
        def __init__(self, sIpAddress):
            self.bc = Device()

     
    def discover(self, *args, **kwargs):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
            
            if self.bc.ePlatform == Platform.BASC_NONE:
                LOGGER.info('Unable to connect')
            if self.bc.ePlatform == Platform.BASC_PI:
                LOGGER.info('connected to BASpi6U6R')
            if self.bc.ePlatform == Platform.BASC_AO:
                LOGGER.info('connected to BASpi6U4R2AO WRONG MODULE Please use correct NodeServer')    

            LOGGER.info('\t' + str(self.bc.uiQty) + ' Universal inputs in this BASpi')
            LOGGER.info('\t' + str(self.bc.boQty) + ' Binary outputs in this BASpi')
            LOGGER.info('\t' + str(self.bc.biQty) + ' Binary inputs in This BASpi')
            LOGGER.info('\t' + str(self.bc.aoQty) + ' Analog outputs In This BASpi')    
        
            
            # Universal Inputs   
            input_one = self.bc.universalInput(1)
            input_two = self.bc.universalInput(2)
            input_tre = self.bc.universalInput(3)
            input_for = self.bc.universalInput(4)
            input_fiv = self.bc.universalInput(5)
            input_six = self.bc.universalInput(6)
            
            # Binary/Digital Outputs
            output_one = (self.bc.binaryOutput(1))
            output_two = (self.bc.binaryOutput(2))
            output_tre = (self.bc.binaryOutput(3))
            output_for = (self.bc.binaryOutput(4))
            output_fiv = (self.bc.binaryOutput(5))
            output_six = (self.bc.binaryOutput(6))   
  
            
            if self.debug_enable == 'True' or self.debug_enable == 'true':
                # Universal Inputs
                LOGGER.info("Temp: " + str(input_one))
                LOGGER.info("Temp: " + str(input_two))
                LOGGER.info("Temp: " + str(input_tre))
                LOGGER.info("Temp: " + str(input_for))
                LOGGER.info("Temp: " + str(input_fiv))
                LOGGER.info("Temp: " + str(input_six))
                # Binary/Digital Outputs 
                LOGGER.info("OnOff: " + str(output_one))
                LOGGER.info("OnOff: " + str(output_two))
                LOGGER.info("OnOff: " + str(output_tre))
                LOGGER.info("OnOff: " + str(output_for))
                LOGGER.info("OnOff: " + str(output_fiv))
                LOGGER.info("OnOff: " + str(output_six))
                
            # Universal Inputs
            self.setDriver('GV1', input_one, force=True)
            self.setDriver('GV2', input_two, force=True)
            self.setDriver('GV3', input_tre, force=True)
            self.setDriver('GV4', input_for, force=True)
            self.setDriver('GV5', input_fiv, force=True)
            self.setDriver('GV6', input_six, force=True)
            # Binary/Digital Outputs
            self.setDriver('GV7', output_one, force=True)
            self.setDriver('GV8', output_two, force=True)
            self.setDriver('GV9', output_tre, force=True)
            self.setDriver('GV10', output_for, force=True)
            self.setDriver('GV11', output_fiv, force=True)
            self.setDriver('GV12', output_six, force=True)
         
        LOGGER.info("BASpi IP IO Points configured")
    
    
    # Output 1
    def setOn(self, command):
        if self.bc.binaryOutput(1) != 1:
            self.bc.binaryOutput(1,1)
            self.setDriver("GV7", 1) 
            LOGGER.info('Output 1 On')
    
    def setOff(self, command):
        if self.bc.binaryOutput(1) != 0:
            self.bc.binaryOutput(1,0)
            self.setDriver("GV7", 0) 
            LOGGER.info('Output 1 Off')
    # Output 2
    def setOn2(self, command):
        if self.bc.binaryOutput(2) != 1:
            self.bc.binaryOutput(2,1)
            self.setDriver("GV8", 1) 
            LOGGER.info('Output 2 On')
    
    def setOff2(self, command):
        if self.bc.binaryOutput(2) != 0:
            self.bc.binaryOutput(2,0)
            self.setDriver("GV8", 0) 
            LOGGER.info('Output 2 Off')         
    # Output 3
    def setOn3(self, command):
        if self.bc.binaryOutput(3) != 1:
            self.bc.binaryOutput(3,1)
            self.setDriver("GV9", 1) 
            LOGGER.info('Output 3 On')
    
    def setOff3(self, command):
        if self.bc.binaryOutput(3) != 0:
            self.bc.binaryOutput(3,0)
            self.setDriver("GV9", 0) 
            LOGGER.info('Output 3 Off')
    # Output 4
    def setOn4(self, command):
        if self.bc.binaryOutput(4) != 1:
            self.bc.binaryOutput(4,1)
            self.setDriver("GV10", 1) 
            LOGGER.info('Output 4 On')
    
    def setOff4(self, command):
        if self.bc.binaryOutput(4) != 0:
            self.bc.binaryOutput(4,0)
            self.setDriver("GV10", 0) 
            LOGGER.info('Output 4 Off')
    # Output 5
    def setOn5(self, command):
        if self.bc.binaryOutput(5) != 1:
            self.bc.binaryOutput(5,1)
            self.setDriver("GV11", 1) 
            LOGGER.info('Output 5 On')
    
    def setOff5(self, command):
        if self.bc.binaryOutput(5) != 0:
            self.bc.binaryOutput(5,0)
            self.setDriver("GV11", 0) 
            LOGGER.info('Output 5 Off')
    # Output 6
    def setOn6(self, command):
        if self.bc.binaryOutput(6) != 1:
            self.bc.binaryOutput(6,1)
            self.setDriver("GV12", 1) 
            LOGGER.info('Output 6 On')
    
    def setOff6(self, command):
        if self.bc.binaryOutput(6) != 0:
            self.bc.binaryOutput(6,0)
            self.setDriver("GV12", 0) 
            LOGGER.info('Output 6 Off')                  

    def delete(self):
        LOGGER.info('Removing BASpi')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def heartbeat(self, init=False):
        # LOGGER.debug('heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        # LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON", 2)
            self.hb = 1
        else:
            self.reportCmd("DOF", 2)
            self.hb = 0

    def check_params(self):
        st = True
        self.remove_notices_all()
        #default_user = "YourUserName"
        #default_password = "YourPassword"
        default_baspi_ip = "127.0.0.1"
        default_name = "BASpi"
        
       
        if 'baspi_ip' in self.polyConfig['customParams']:
            self.ipaddress = self.polyConfig['customParams']['baspi_ip']
        else:
            self.ipaddress = default_baspi_ip
            LOGGER.error(
                'check_params: BASpi IP not defined in customParams, please add it.  Using {}'.format(self.ipaddress))
            st = False
        if 'name' in self.polyConfig['customParams']:
            self.user = self.polyConfig['customParams']['name']
        else:
            self.user = default_name
            LOGGER.error('check_params: Poly Name not defined in customParams, please add it.  Using {}'.format(self.user))
            st = False  


        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']

        # Make sure they are in the params 'password': self.password, 'user': self.user,
        self.addCustomParam({'baspi_ip': self.ipaddress, 'debug_enable': self.debug_enable})

        # Add a notice if they need to change the user/password from the defaultself.user == default_user or self.password == default_password or .
        if self.ipaddress == default_baspi_ip:
            self.addNotice('Please set proper, BASpi IP '
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

    id = 'controller'
    commands = {
        'DON': setOn,
        'DOF': setOff,
        'DON2': setOn2,
        'DOF2': setOff2,
        'DON3': setOn3,
        'DOF3': setOff3,
        'DON4': setOn4,
        'DOF4': setOff4,
        'DON5': setOn5,
        'DOF5': setOff5,
        'DON6': setOn6,
        'DOF6': setOff6,
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
    }
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 25},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 56},
        {'driver': 'GV6', 'value': 1, 'uom': 56},
        {'driver': 'GV7', 'value': 1, 'uom': 56},
        {'driver': 'GV8', 'value': 1, 'uom': 56},
        {'driver': 'GV9', 'value': 1, 'uom': 56},
        {'driver': 'GV10', 'value': 1, 'uom': 56},
        {'driver': 'GV11', 'value': 1, 'uom': 56},
        {'driver': 'GV12', 'value': 1, 'uom': 56},
                
        
    ]



if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('BASpi6u6r')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
        polyglot.stop()
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
    sys.exit(0)

#SJB 07_25_2020
