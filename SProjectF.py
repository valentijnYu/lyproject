#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:02:05 2019

@author: yuzheng
"""
import numpy
from scipy.optimize import curve_fit


def _1gaussian(x, *p):
    amp1,cen1,sigma1 = p
    return amp1*(1/(sigma1*(numpy.sqrt(2*numpy.pi))))*(numpy.exp(-((x-cen1)**2)/((2*sigma1)**2)))


def _2gaussian(x, *p):
    amp1,cen1,sigma1, amp2,cen2,sigma2 = p
    return amp1*(1/(sigma1*(numpy.sqrt(2*numpy.pi))))*(numpy.exp(-((x-cen1)**2)/((2*sigma1)**2))) +\
           amp2*(1/(sigma2*(numpy.sqrt(2*numpy.pi))))*(numpy.exp(-((x-cen2)**2)/((2*sigma2)**2)))

class alpha:
    
    numpy.seterr(divide = 'ignore', invalid = 'ignore')
    
    
    def __init__(self, x, y, p0, pds1, pds2):
        
        self.x = x
        self.y = y
        
        self.ini1 = p0[:3]
        self.ini2 = p0
        self.pds1 = pds1
        self.pds2 = pds2
        

    def fit1g(self):
         #one-gaussian
         popt_gauss_1, pcov_gauss_1 = curve_fit(_1gaussian, self.x, self.y, p0=self.ini1, bounds = self.pds1)
         y_fit_1 = _1gaussian(self.x,*popt_gauss_1)
         return y_fit_1
     
    def fit2g(self,adv):
        popt_gauss_2, pcov_gauss_2 = curve_fit(_2gaussian, self.x, self.y,p0=self.ini2,bounds = self.pds2)
        pars_1 = popt_gauss_2[0:3]
        pars_2 = popt_gauss_2[3:6]
        gauss_peak_1 = _1gaussian(self.x,*pars_1)
        gauss_peak_2 = _1gaussian(self.x,*pars_2)
        if adv == None:
            return gauss_peak_1 + gauss_peak_2
        else:
            return gauss_peak_1,gauss_peak_2


#x = numpy.array([1,2,3])
#y = numpy.array([1,2,3])

#p0=(50,-500,250,50,500,250)
#bds_2 = ([1,-1000,1,1,0,1],[100000,0,500,100000,1000,500])
#bds_1 = ([1,-1000,1],[100000,1000,500])

#fit = alpha(x,y,p0,bds_1,bds_2)
#fit.fit1g()