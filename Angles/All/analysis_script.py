#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.offsetbox import AnchoredText
get_ipython().run_line_magic('matplotlib', 'inline')

#Scatter function
def scatter_flux(dfile):
    '''
    Inputs
        dfile, type: string, name of flux file we want to plot
    Output:
        Scatter plot of flux (events/m^2/min) vs. time (UTC)
        Returns flux and error data
    '''

    #open flux csv file and read in data 
    file = open(dfile)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
            rows.append(row)

    #get flux from file
    flux = []
    for r in rows:
        flux.append(float(r[2]))    

    #get dates and times from  file
    date_time = []
    for d in rows:
        date_time.append(d[0] + ' ' + d[1])
    good_times = pd.to_datetime(date_time, format='%y/%m/%d %H:%M:%S')

    #get error in flux from file
    err = []
    for e in rows:
        err.append(float(e[3]))
    
    #flux plot  
    fig, ax = plt.subplots()
    at = AnchoredText("Detector: 6709\n Channel Number:1", prop=dict(size=10), frameon=False, loc='upper right')
    ax.add_artist(at)

    plt.scatter(good_times, flux)
    plt.errorbar(good_times, flux, yerr=err, fmt='o', capsize=4)
    plt.title('Flux Study')
    plt.xlabel('Time (UTC)')
    plt.ylabel('Flux (events/m$^2$/min)')
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45)
    plt.tick_params(bottom=True, top=True, left=True, right=True, direction='in')

    plt.show()
    plt.close

    file.close()
    
    return flux, err

# Outlier function
def remove_outlier(flux, err):
    q1, q3 = np.percentile(flux, [25,75])
    iqr = q3 - q1
    
    lower_bound = q1 - (1.5 * iqr) 
    upper_bound = q3 + (1.5 * iqr)
    
    for count, f in enumerate(flux):
        if f < lower_bound or f > upper_bound:
            flux.remove(f)
            err.pop(count)

