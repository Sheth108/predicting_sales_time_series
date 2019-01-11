import pickle
import pandas as pd
import numpy as np
from get_forecast import *


# create a function to take in user-entered amounts and apply the model
def forecast(amounts):
    
    forecast, summary = getForecast(amounts[0], amounts[1], amounts[2])
    return forecast, summary

    # if amounts[4] == True:
    # 	forecast, summary = getForecast(amounts[0], amounts[1], amounts[2],
    # 									amounts[3], amounts[4], amounts[5])
    # 	return forecast, summary
    # else:
    # 	forecast = getForecast(amounts[0], amounts[1], amounts[2],
    # 							amounts[3], amounts[4], amounts[5])
    # 	return forecast, ''