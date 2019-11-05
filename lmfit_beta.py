#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scipy.ndimage as snd
from lmfit import Model

#Skewed gaussian functions

def sk_ga1(x,a_1,x0_1,asym_1,d_1):
    return a_1*numpy.exp((-(x-x0_1)**2)/(2*(asym_1*(x-x0_1)+d_1)**2))

def sk_ga2(x,a_1,x0_1,asym_1,d_1,a_2,x0_2,asym_2,d_2):
    g1 = sk_ga1(x,a_1,x0_1,asym_1,d_1)
    g2 = sk_ga1(x,a_2,x0_2,asym_2,d_2)
    return g1+g2

#initiate lmfit


lmG2 = Model(sk_ga2)
print('parameter names: {}'.format(lmG2.param_names))
print('independent variables: {}'.format(lmG2.independent_vars))

lmG1 = Model(sk_ga1)
print('parameter names: {}'.format(lmG1.param_names))
print('independent variables: {}'.format(lmG1.independent_vars))

#set initial values and boundaries
params = lmG2.make_params(a_1=20, x0_1=-250, asym_1=0.25, d_1 = 25,a_2=20, x0_2=250, asym_2=0.25,d_2 = 25)

lmG2.set_param_hint('a_1', min = 0, max = 100)
lmG2.set_param_hint('x0_1', min = -500, max = 0)
lmG2.set_param_hint('asym_1', min = 0, max = 0.4)
lmG2.set_param_hint('d_1', min = 20, max = 100)
lmG2.set_param_hint('a_2', min = 0, max = 100)
lmG2.set_param_hint('x0_2', min = 0, max = 500)
lmG2.set_param_hint('asym_2', min = 0, max = 0.4)
lmG2.set_param_hint('d_2', min = 20, max = 100)




#generate a test data

data = lyman(3.1, 120, 90, 0.3,-0.3, 300, 0.5)
muse_x = data.MuseData()[0]
muse_y = data.MuseData()[1]

result = lmG2.fit(muse_y, params, x=muse_x)
print(result.fit_report())


pyplot.step(muse_x, muse_y, '-', label = "data")
pyplot.plot(muse_x, result.best_fit, '--',label = 'fit')
pyplot.legend()
pyplot.show()
