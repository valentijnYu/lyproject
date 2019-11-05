#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 12:35:33 2019

@author: yuzheng
"""
import numpy

class asd:
    def __init__(self,x):
        self.x = x
    def ga(self,*p):
        a,b,c = p
        return a+self.x
    
test = asd(3)
d = ([1,2,3])

test.ga(d)