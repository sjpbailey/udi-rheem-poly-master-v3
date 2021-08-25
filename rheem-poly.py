#!/usr/bin/env python3
"""
Polyglot v3 node server Example 1
Copyright (C) 2021 Robert Paauwe

MIT License
"""
import udi_interface
import sys
import time
import asyncio
import logging

import requests
from requests.auth import HTTPBasicAuth #HTTP

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom
polyglot = None
Parameters = None
n_queue = []
count = 0

'''
TestNode is the device class.  Our simple counter device
holds two values, the count and the count multiplied by a user defined
multiplier. These get updated at every shortPoll interval
'''
class TestNode(udi_interface.Node):
    id = 'test'
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'GV0', 'value': 0, 'uom': 56},
            {'driver': 'GV1', 'value': 0, 'uom': 56},
            ]

def noop(self):
        LOGGER.info('Discover not implemented')

def query(self):
        #LOGGER.debug("Query sensor {}".format(self.address))
        asyncio.run(self.querynodes())
        #self.reportDrivers()        

        commands = {
        'DISCOVER': noop,
        'QUERY':  query
        }

'''
node_queue() and wait_for_node_event() create a simple way to wait
for a node to be created.  The nodeAdd() API call is asynchronous and
will return before the node is fully created. Using this, we can wait
until it is fully created before we try to use it.
'''
def node_queue(data):
    n_queue.append(data['address'])

def wait_for_node_event():
    while len(n_queue) == 0:
        time.sleep(0.1)
    n_queue.pop()

'''
Read the user entered custom parameters. In this case, it is just
the 'multiplier' value.  Save the parameters in the global 'Parameters'
'''
def parameterHandler(params):
    global Parameters

    Parameters.load(params)


'''
This is where the real work happens.  When we get a shortPoll, increment the
count, report the current count in GV0 and the current count multiplied by
the user defined value in GV1. Then display a notice on the dashboard.
'''

async def main():
    
    email = "sjpbailey@comcast.net" #input("Enter your email: ").strip()
    password = "NatiqueRheem61" #getpass.getpass(prompt='Enter your password: ')  
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


def poll(polltype):
    global count
    global Parameters

    if 'shortPoll' in polltype:
        if Parameters['multiplier'] is not None:
            mult = int(Parameters['multiplier'])
        else:
            mult = 1

        node = polyglot.getNode('my_address')
        if node is not None:
            count += 1

            node.setDriver('GV0', count, True, True)
            node.setDriver('GV1', (count * mult), True, True)

            # be fancy and display a notice on the polyglot dashboard
            polyglot.Notices['count'] = 'Current count is {}'.format(count)


def stop():
    nodes = polyglot.getNodes()
    for n in nodes:
        nodes[n].setDriver('ST', 0, True, True)
    polyglot.stop()

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        Parameters = Custom(polyglot, 'customparams')

        # subscribe to the events we want
        polyglot.subscribe(polyglot.CUSTOMPARAMS, parameterHandler)
        polyglot.subscribe(polyglot.ADDNODEDONE, node_queue)
        polyglot.subscribe(polyglot.STOP, stop)
        polyglot.subscribe(polyglot.POLL, poll)

        # Start running
        polyglot.ready()
        polyglot.setCustomParamsDoc()
        polyglot.updateProfile()


    except Exception as e:
        LOGGER.info("Error: " + str(e))
        node = TestNode(polyglot, 'my_address', 'my_address', 'Rheem Water Heater')
        polyglot.addNode(node)
        wait_for_node_event()

        # Just sit and wait for events
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

