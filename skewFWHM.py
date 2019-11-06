#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def sk1F(x,a_1,x0_1,asym_1,FWHM_1):
    d_1 = FWHM_1*(1-1.38629*asym_1**2)/2.35482 #write sigma in terms of FWHM
    return a_1*numpy.exp((-(x-x0_1)**2)/(2*(asym_1*(x-x0_1)+d_1)**2))

def sk2F(x,a_1,x0_1,asym_1,FWHM_1,a_2,x0_2,asym_2,FWHM_2):
    g1 = sk_ga1(x,a_1,x0_1,asym_1,FWHM_1)
    g2 = sk_ga1(x,a_2,x0_2,asym_2,FWHM_2)
    return g1+g2

FW1 = Model(sk1F)
print('parameter names: {}'.format(FW1.param_names))
print('independent variables: {}'.format(FW1.independent_vars))

FW2 = Model(sk2F)
print('parameter names: {}'.format(FW2.param_names))
print('independent variables: {}'.format(FW2.independent_vars))

#set initial values and boundaries

FW2.set_param_hint('a_1', min = 0)
FW2.set_param_hint('x0_1', min = -500, max = 0)
FW2.set_param_hint('asym_1', min = 0, max = 0.2)
FW2.set_param_hint('FWHM_1', max = 500)
FW2.set_param_hint('a_2', min = 0)
FW2.set_param_hint('x0_2', min = 0, max = 500)
FW2.set_param_hint('asym_2', min = -0.2, max = 10)
FW2.set_param_hint('FWHM_2', max = 500)

params_FW = FW2.make_params(a_1=20, x0_1=-250, asym_1=0.1, FWHM_1 = 100, a_2=20, x0_2=250, asym_2=-0.1,FWHM_2 = 100)

result = FW2.fit(muse_y, params_FW, x=muse_x)
print(result.fit_report())

pyplot.step(muse_x, muse_y, '-')
pyplot.plot(muse_x, result.best_fit, '--')

pyplot.show()
