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
import matplotlib.pyplot as plt

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
        i = Oscilloscope(ip=ip, force_connect=force)
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

def parameterize_data(data: dict):
    """ Returns a handy dict with the relevant capture details filled in.."""
    ret = {}
    ## The `data` is arranged in a series of parallel arrays.
    ## taking the length of one of these will return the number of samples
    ret['n_samples']  = len(data['time']) 
    ## it seems like a hack, but afaict the best way to deduce the number of channels present in the current data dict
    ## is by subtracting one from the overall length of the returned dict 🤔
    ret['n_channels'] = len(data) - 1
    ## These boundaries are handy for setting the x-axes limits
    ret['t_start']= data['time'][0]
    ret['t_end']  = data['time'][-1]
    
    return ret

def process_data(params, data):
    """process_data: illustrates how to walk the simplistic data structure returned by a single call to scope.get_data"""
    logger.info(f"##process_data(params:{params}")
    mid_x = int(params['n_samples'] / 2) #close enough!

    logger.debug(f"## First: {data['time'][0]}|  {data['ch1'][0]}")
    logger.debug(f"##   Mid: {data['time'][mid_x]}|{data['ch1'][mid_x]}")
    logger.debug(f"##  Last: {data['time'][-1]}|{data['ch1'][-1]}")
    
    return

def do_plotly_stuff_here(i: Oscilloscope, params):
    """#TODO: stuff here"""
    logger.info(f"About to start doing plotly stuff with params:{params}")

    try:
        data = i.get_data()
    
        #PLotly stuff
        plt.ion()
        plt.show()
        plt.grid(visible=True)
        plt.ylim([-1, 1])
        plt.xlim( [params['t_start'], params['t_end']])
    
        ## Lines
        line1, = plt.plot([])
        line2, = plt.plot([])

        ## axes
        ax = plt.gca()
        
        print(f"##  Begin infinite loop over get_data")
        while True:
            ## pull in new data
            data = i.get_data()

            ## update the plots
            line1.set_ydata(data['ch1'])
            line2.set_ydata(data['ch2'])
            line1.set_xdata(data['time'])
            line2.set_xdata(data['time'])
            plt.pause(0.001)
    except Exception as e:
        print(f'Exception occured looping over data: {e}')
        logger.error(f'Exception occured looping over data: {e}')

    finally:
        i.relinquish_ownership()
        sys.exit(-1)


    return None
       
if __name__ == "__main__":
    setup_logging()
    i = setup_scope(G['ip'], G['force_connect'])
    logger.info("Scope setup complete:")
    logger.info(i)
    data = i.get_data()
    data_params = parameterize_data(data)

    do_plotly_stuff_here(i, data_params)
    #process_data(data_params, data)
    
