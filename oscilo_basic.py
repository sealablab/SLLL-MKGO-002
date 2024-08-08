#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## SLLL-MKGO-002: Basic Oscilloscope
## SLLL-MKGO-002: demonstrates how to use the Oscilloscope instrument
### Pre-requisites: Connectivity verified to moku device per SLLL-MKGO-001
## Configuration settings current all live in `GlobalOptArgs`, aka: 'G'
GlobalOptArgs={}
GlobalOptArgs['ip'] = '192.168.127.40'
GlobalOptArgs['force_connect'] = True
G=GlobalOptArgs

## A note about imports:
## We are just going to take the following for granted:  
## luguru, numpy, ...
import sys
from loguru import logger
from moku.instruments import Oscilloscope
## End imports
## A note about logging:
## We are going to want to utilize the moku library's logging ability.
## But for now, consider that a #TODO
def setup_logging():
    global G
    logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
    logger.info("Logging configured")
    logger.info(G)

logger.info(GlobalOptArgs)
G = GlobalOptArgs



def setup_scope(ip, force) -> Oscilloscope:
    global G
    ## Connect to your Moku by its ip address
    ## (force_connect will take control from any other user)
    try:
        i = Oscilloscope(G['ip'], force_connect=G['force_connect'])
        ## Manually set our input sources:
        i.set_source(1, 'Input1') #(Can i select DIO here if i try hard enough?)
        i.set_source(2, 'Input2') #Set the data source of Channel 2 to Input 2 
        
        # Manually set trigger on input Channel 1, rising edge, 0.01V 
        i.set_trigger(type='Edge', source='Input1', level=0.01)
        return i
    except Exception as e:
        logger.error(f'Exception occurred connecting to scope: {e}')

def main_data_loop(o: Oscilloscope):
    logger.debug("main_data_loop")
    o       
if __name__ == "__main__":
    i = setup_scope(G['ip'], G['force_connect'])
    logger.info("Scope setup complete:")
    logger.info(i)
    data = i.get_data()
    logger.info("Data fetch complete. Now what?")
    print(data)

    ## When we are all done playing we put our toys back in the toybox (cleanup resources..)
    i.relinquish_ownership()

