#!/usr/bin/env python
"""
This is a NodeServer template for Polyglot v3 written in Python3
v2 version by Einstein.42 (James Milne) milne.james@gmail.com
v3 version by (Bob Paauwe) bpaauwe@yahoo.com
"""
import udi_interface
import sys

LOGGER = udi_interface.LOGGER

""" Grab My Controller Node (optional) """
from nodes import RheemController

if __name__ == "__main__":
    try:
        
        polyglot = udi_interface.Interface([RheemController])
        
        polyglot.start()

        control = RheemController(polyglot, 'controller', 'controller', 'PythonTemplate')

        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
    
        polyglot.stop()
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
    sys.exit(0)
