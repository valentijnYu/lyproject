#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:24:13 2019

@author:Jorryt Yuzheng
"""

import numpy
import scipy.ndimage as snd
from scipy.interpolate import interp1d

class lyman:
    
    numpy.seterr(divide='ignore', invalid='ignore') #ignore zero divider

    def __init__(self, z, lr,lb,ar,ab,psep,rpb):
        #Basic default parameters for simulating a fake line
        self.DX=0.5
        self.fakeflux=8. 
        self.xx=numpy.arange(-1200,1500.,self.DX)
        self.c=299792.458 #speed of light in km/s
        #init parameters 
        self.redshift = z
        self.linewidthRed = lr
        self.linewidthBlue = lb
        self.asymRed = ar
        self.asymBlue = ab
        self.separation = psep
        self.relativePeakfluxBluered = rpb
        self.wavelength =1215.67*(1+self.redshift)*(1+self.xx/self.c)
        self.LSF_wavelength=self.MUSE_LSF((1+self.redshift)*1215.67)
        self.LSF_SIGMA=self.LSF_wavelength*self.c/((1+self.redshift)*1215.67)

        
    def __repr__(self):
        return 'Code for Semester Project'
    

    def half_gaussian(self,x,a,x0,sigma):
        return numpy.nan_to_num(a*numpy.exp(-((numpy.sqrt((x-x0)))**2)**2/(2*sigma**2))) 
    
    
    def skewed_gaussian(self,x,a,x0,asym,d):
        return a*numpy.exp((-(x-x0)**2)/(2*(asym*(x-x0)+d)**2))
    
    def smoothed_skewed_gaussian(self,x,a,x0,asym,d):
        LSF_SIGMA_dx=166./(2.355*75.) #75 is the pixel-scale of MUSE dz (e.g. 1 pixel in the wavelength direction corresponds to 75 km/s for this example, need to be improved)
        return snd.gaussian_filter(a*numpy.exp((-(x-x0)**2)/(2*(asym*(x-x0)+d)**2)),sigma=LSF_SIGMA_dx)
    
    def MUSE_LSF(self,wv): #observed wavelength in angstrom; returns the LSF_sigma width, from Eq  in https://arxiv.org/abs/1710.03002
        return (6.040+(5.866E-8 * wv**2) - (9.187E-4*wv))/2.355
    
    def intrinsic_double(self):
        #Simulate a double peak
        peak1 = self.skewed_gaussian(self.xx,self.fakeflux,0.+self.separation/2.,self.asymRed,self.linewidthRed)
        peak2 = self.skewed_gaussian(self.xx,self.fakeflux*self.relativePeakfluxBluered,0-self.separation/2.,self.asymBlue,self.linewidthBlue)
        return (1+self.redshift)*(peak1+peak2)
    
    def smooth(self):
        return snd.gaussian_filter(self.intrinsic_double(),sigma=self.LSF_SIGMA/self.DX)
    
    def MuseData(self):
        ###HERE I'm going to decrease the pixel-scale to the same as the MUSE data, which is  1.25 Angstrom.
        ff=interp1d(self.wavelength,self.smooth())
        sim_wav=numpy.arange(numpy.min(self.wavelength)+2,numpy.max(self.wavelength)-2.,1.25)
        sim_vel=((sim_wav/(1215.67*(1+self.redshift)))-1.)*self.c #decreased x range in MUSE data
        sim_line=ff(sim_wav) #decreased y range in MUSE data
        return sim_vel,sim_line
    
    def MuseDataN(self,sigma):
        smoothed_line=numpy.random.normal(self.smooth(),sigma)
        if sigma == None:
            sigma = 3
        ffN=interp1d(self.wavelength,smoothed_line)
        sim_wav=numpy.arange(numpy.min(self.wavelength)+2,numpy.max(self.wavelength)-2.,1.25)
        sim_Nvel=((sim_wav/(1215.67*(1+self.redshift)))-1.)*self.c #decreased x range in MUSE Noise data
        sim_Nline=ffN(sim_wav) #decreased y range in MUSE Noise data
        return sim_Nvel,sim_Nline
 
