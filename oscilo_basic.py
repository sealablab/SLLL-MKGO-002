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
import math
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
        
        ## Manually set trigger on input Channel 1, rising edge, 0.01V 
        i.set_trigger(type='Edge', source='Input1', level=0.01)
        ## View +-5usec, i.e. trigger in the centre
        i.set_timebase(-5e-6, 5e-6)

        return i
    except Exception as e:
        logger.error(f'Exception occurred connecting to scope: {e}')

def process_data(data: dict):
    """process_data: illustrates how to walk the simplistic data structure returned by a single call to scope.get_data"""
    ## The `data` is arranged in a series of parallel arrays.
    ## taking the length of one of these will return the number of samples
    n_samples = len(data['time']) 
    
    ## it seems like a hack, but afaict the best way to deduce the number of channels present in the current data dict
    ## is by subtracting one from the overall length of the returned dict 🤔
    n_channels= len(data) - 1
    ## By taking the fabs delta between the first and last sample returned, we can deduce the duration in seconds
    t_span = math.fabs(data['time'][-1] - data['time'][0])
    ## And finally, since we know the window that we requested was 'centered' (see the call to`set_timebase` above)
    ## we just assume that t0 was right in the middle of the data. (This is a very bad assumption)
    mid_x = int(n_samples / 2) # close enough!
    ## Before we actually iterate through any of this, lets print a sumary
    logger.info(f"##process_data( n_chan:{n_channels},t_span:{t_span}, n_samples:{n_samples}")

    logger.debug(f"## First: {data['time'][0]}|  {data['ch1'][0]}")
    logger.debug(f"##   Mid: {data['time'][mid_x]}|{data['ch1'][mid_x]}")
    logger.debug(f"##  Last: {data['time'][-1]}|{data['ch1'][-1]}")
    
    return


       
if __name__ == "__main__":
    i = setup_scope(G['ip'], G['force_connect'])
    logger.info("Scope setup complete:")
    logger.info(i)
    data = i.get_data()
    process_data(data)
    ## SLLL-MKGO-Q1: What is the return type of our 'data' variable
    ## SLLL-MKGO-Q1.1: What is the overall structure inside? (See process_data for example)
    
    ## When we are all done playing we put our toys back in the toybox (cleanup resources..)
    i.relinquish_ownership()

