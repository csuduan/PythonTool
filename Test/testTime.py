#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @created on: 2018/3/21 15:29
# @desc  :


import time

def fun1(a, b):
    print('fun1')
    print(a, b)
    time.sleep(1)

def fun2():
    print('fun2')
    time.sleep(1)

def fun3():
    print('fun3')
    time.sleep(2)

def fun4():
    print('fun4')
    time.sleep(1)

def fun5():
    print('fun5')
    time.sleep(1)
    fun4()


for i in range(1,5):
    fun1('foo', 'bar')
fun2()
fun3()
fun5()