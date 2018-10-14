#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 14:38:13 2018

@author: paul
"""
import os
import quandl
quandl.ApiConfig.api_key =  os.environ.get('API_KEY_QUANDL')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import datetime
now = datetime.datetime.now()
#%%

class Stocks:
    def __init__(self):
        """
        init a Stocks object
        """
        self.stock_dict = dict()
   
    def load_names(self,stock_names):
        """
        load the names of the stockes 
        """
        self.stock_names = stock_names
        self.n_stocks = len(stock_names)
        
    
    def get_data(self):
        """
        download the data using quandl if not already downloaded
        """
        for name in self.stock_names:
            if not name in self.stock_dict:
                self._download_data(name)
    
    def _download_data(self,stock_name):
        """
        download data using quandl
        """
        self.stock_dict[stock_name] = quandl.get(stock_name)
        
    def resample(self,key,alternative=None,first='2014-04-01',last=now.strftime("%Y-%m-%d")):
        """
        resample data to a daily period with foreward filling for not exisiting 
        days and nan values
        """
        self.stock_dict_resampled = dict()
        
        for name in self.stock_names:
            try:
                self.stock_dict_resampled[name] = self.stock_dict[name][key]
            except:
                if alternative:
                    try: 
                        self.stock_dict_resampled[name] = self.stock_dict[name][alternative]
                        print "No data found for key '"+key+"' use alternative '"+ alternative + "'"
                    except:
                        raise SystemExit("No data found for key '"+key+"' and alternative '"+ alternative + "'")
           
            first_date_df = stocks.stock_dict_resampled[name].reset_index()['Date'].min()
            last_date_df = stocks.stock_dict_resampled[name].reset_index()['Date'].max()
            
            if pd.Timestamp(first) > first_date_df and pd.Timestamp(last) < last_date_df:
                self.stock_dict_resampled[name] = self.stock_dict_resampled[name].resample('D').ffill().truncate(before=first, after=last)
            else:
                print "No data existent for '" + name + "' for the desired time period. Exclude this data."
                del self.stock_dict_resampled[name]
                continue
                
            self.stock_dict_resampled[name] = self.stock_dict_resampled[name].fillna(method="ffill")
        
        self.stock_df = pd.DataFrame(self.stock_dict_resampled)
        
    def pca(self):
        """
        perform a pca using the pca method from the sklearn module
        """
        x = StandardScaler().fit_transform(self.stock_df)
        self.pcs = PCA().fit(x)
        
        self.plot_pca()
    
    def plot_pca(self,weigted_ev=False):
        """
        plot the components in a matrix with names on the x axis and explained 
        variance on the y-axis
        """
        plt.close("all")
        ind = np.arange(0,len(self.pcs.components_))
        fig, ax = plt.subplots()
        
        if weigted_ev:
            plotdata = self.pcs.components_* self.pcs.explained_variance_ratio_.reshape(8,1)
        else: 
            plotdata = self.pcs.components_
            
        scale = np.max(np.abs(plotdata))
        
        mat = ax.matshow(plotdata,cmap=plt.cm.RdYlGn,vmin = -scale,vmax = scale)
        
        ax.set_xticks(ind)
        ax.set_xticklabels(list(self.stock_df.columns.values))
        
        ax.set_ylabel("explained variance")
        ax.set_yticks(ind)
        ax.set_yticklabels(np.round(self.pcs.explained_variance_ratio_*100,1))
        plt.colorbar(mat)
        
    
#%%
if __name__ == "__main__":
            
    stocks = Stocks()
    
    stocks.load_names(["SSE/VVD","SSE/IFX","SSE/PO0","SSE/FB2A","SSE/AMZ","SSE/FNTN","SSE/BRYN","SSE/RHM","FSE/MUV2_X"])
    stocks.get_data()
    #%%
    
    stocks.resample("Last", alternative="Close",first='2018-09-01',last='2018-10-01')
    
    stocks.pca()
    stocks.plot_pca(weigted_ev=False)