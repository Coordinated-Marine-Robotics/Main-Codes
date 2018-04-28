#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 03:01:37 2018

@author: fitri
"""
def testA():
    x = 5
    y = 2
    return x, y

def testB():
    x, y = testA()
    b = x + y
    print(b)
    
    