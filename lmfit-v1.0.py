#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#This code is showing read out data from a fits file.
#Then use the prepared model(initial params and bounds are already settled) to fit the data (include error)
#Finally, plot the raw data, fit data, and print the chisqr and the separation


from astropy.io import fits
from lmfit.model import ModelResult, save_model, load_model

#import fits file from the local directory
#Then save the specific range of the data into variables
#And normalized data
spec68 = fits.open('../1Ds_LAEs_forYuzheng/1D_spectrum_MUSEID_68.fits')
x68 = spec68[1].data['delta_v_Lya'][1956:1996]
y68 = spec68[1].data['flux'][1956:1996]
e68 = spec68[1].data['flux_err'][1956:1996]
Ne68 = e68/y68.max()

#Load preset model
FW2 = load_model('FW2SG.sav')

#plot the graph
result = FW2.fit(Ny68, params_FW, x=x68, weights = Ne68)
pyplot.step(x68, Ny68, '-', where='mid')
pyplot.plot(x68, result.best_fit, '--')
pyplot.title('2 Skewed gaussian using FWHM as parameters')
pyplot.show()

#print out the result
sep_result = result.params['x0_2'] - result.params['x0_1']
print('The chi square is {:.10f}'.format(result.chisqr))
print('The separation is {:.2f}'.format(sep_result))
#print(result.fit_report())
result.params
