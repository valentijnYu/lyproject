#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.special import erf

def ga1_sk(x, amp1,cen1,asym1,sigma1):
    norm = amp1*(1/(sigma1*(numpy.sqrt(2*numpy.pi))))*(numpy.exp(-((x-cen1)**2)/((2*sigma1)**2)))
    cdf = 0.5*(1+erf(asym1*(x-cen1)/(sigma1*2**0.5)))
    return norm*cdf

def ga2_sk(x,amp1,cen1,asym1,sigma1,amp2,cen2,asym2,sigma2):
    g1 = ga1_sk(x,amp1,cen1,asym1,sigma1)
    g2 = ga1_sk(x,amp2,cen2,asym2,sigma2)
    return g1+g2

G2lm = Model(ga2_sk)
print('parameter names: {}'.format(G2lm.param_names))
print('independent variables: {}'.format(G2lm.independent_vars))

G1lm = Model(ga1_sk)
print('parameter names: {}'.format(G1lm.param_names))
print('independent variables: {}'.format(G1lm.independent_vars))

#set initial values and boundaries
params_new = G2lm.make_params(amp1=20, cen1=-250, asym1=0.25, sigma1 = 25, amp2=20, cen2=250, asym2=0.25,sigma2 = 25)

G2lm.set_param_hint('amp1', min = 0, max = 100)
G2lm.set_param_hint('cen1', min = -500, max = 0)
G2lm.set_param_hint('asym1', min = -10, max = 10)
G2lm.set_param_hint('sigma1', min = 5, max = 80)
G2lm.set_param_hint('amp2', min = 0, max = 100)
G2lm.set_param_hint('cen2', min = 0, max = 500)
G2lm.set_param_hint('asym2', min = -10, max = 10)
G2lm.set_param_hint('sigma2', min = 5, max = 80)

result_new = G2lm.fit(muse_y, params_new, x=muse_x, method = 'leastsq')
print(result_new.fit_report())

pyplot.step(muse_x, muse_y, '-')
pyplot.plot(muse_x, result_new.best_fit, '--')

pyplot.show()
