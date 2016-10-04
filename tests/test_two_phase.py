# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from __future__ import division
from fluids import *
import numpy as np
from numpy.testing import assert_allclose
import pytest


def test_Friedel():
    dP = Friedel(m=10, x=0.9, rhol=950., rhog=1.4, mul=1E-3, mug=1E-5, sigma=0.02, D=0.3, roughness=0, L=1)
    assert_allclose(dP, 274.21322116878406)
    
    # Example 4 in [6]_:
    dP = Friedel(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, sigma=0.0487, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 738.6500525002241)
    # 730 is the result in [1]_; they use the Blassius equation instead for friction
    # the multiplier was calculated to be 38.871 vs 38.64 in [6]_


def test_Gronnerud():
    dP = Gronnerud(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 384.125411444741)
    
    dP = Gronnerud(m=5, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 26650.676132410194)

def test_Chisholm():
    # Gamma < 28, G< 600
    dP = Chisholm(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 1084.1489922923736)
    
    # Gamma < 28, G > 600
    dP = Chisholm(m=2, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 7081.89630764668)
    
    # Gamma <= 9.5, G_tp <= 500
    dP = Chisholm(m=.6, x=0.1, rhol=915., rhog=30, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 222.36274920522493)
    
    # Gamma <= 9.5, G_tp < 1900:
    dP = Chisholm(m=2, x=0.1, rhol=915., rhog=30, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 1107.9944943816388)
    
    # Gamma <= 9.5, G_tp > 1900:
    dP = Chisholm(m=5, x=0.1, rhol=915., rhog=30, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 3414.1123536958203)
    
    dP = Chisholm(m=1, x=0.1, rhol=915., rhog=0.1, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 8743.742915625126)
    
    # Roughness correction
    dP = Chisholm(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=1E-4, L=1, rough_correction=True)
    assert_allclose(dP, 846.6778299960783)

    
def test_Baroczy_Chisholm():
    # Gamma < 28, G< 600
    dP = Baroczy_Chisholm(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 1084.1489922923736)
        
    # Gamma <= 9.5, G_tp > 1900:
    dP = Baroczy_Chisholm(m=5, x=0.1, rhol=915., rhog=30, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 3414.1123536958203)
    
    dP = Baroczy_Chisholm(m=1, x=0.1, rhol=915., rhog=0.1, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 8743.742915625126)

    
def test_Muller_Steinhagen_Heck():
    dP = Muller_Steinhagen_Heck(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 793.4465457435081)


def test_Lombardi_Pedrocchi():
    dP = Lombardi_Pedrocchi(m=0.6, x=0.1, rhol=915., rhog=2.67, sigma=0.045, D=0.05, L=1)
    assert_allclose(dP, 1567.328374498781)


def test_Theissing():
    dP = Theissing(m=0.6, x=.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 497.6156370699528)
    
    # Test x=1, x=0
    dP = Theissing(m=0.6, x=1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 4012.248776469056)
    
    dP = Theissing(m=0.6, x=0, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 19.00276790390895)

    
def test_Jung_Radermacher():
    dP = Jung_Radermacher(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 552.068612372557)

    
def test_Tran():
    dP = Tran(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, sigma=0.0487, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 423.2563312951231)

    
def test_Chen_Friedel():
    dP = Chen_Friedel(m=.0005, x=0.9, rhol=950., rhog=1.4, mul=1E-3, mug=1E-5, sigma=0.02, D=0.003, roughness=0, L=1)
    assert_allclose(dP, 6249.247540588871)
    
    dP = Chen_Friedel(m=.05, x=0.9, rhol=950., rhog=1.4, mul=1E-3, mug=1E-5, sigma=0.02, D=0.03, roughness=0, L=1)
    assert_allclose(dP, 690.8541527904271)

    
def test_Zhang_Webb():
    dP = Zhang_Webb(m=0.6, x=0.1, rhol=915., mul=180E-6, P=2E5, Pc=4055000, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 712.0999804205619)

    
def test_Bankoff():
    dP = Bankoff(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 4746.059442453398)


def test_Xu_Fang():
    dP = Xu_Fang(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, sigma=0.0487, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 604.0595632116267)

def test_Yu_France():
    dP = Yu_France(m=0.6, x=.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 1146.983322553957)
    

def test_Wang_Chiang_Lu():
    dP = Wang_Chiang_Lu(m=0.6, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 448.29981978639154)
    
    dP = Wang_Chiang_Lu(m=0.1, x=0.1, rhol=915., rhog=2.67, mul=180E-6, mug=14E-6, D=0.05, roughness=0, L=1)
    assert_allclose(dP, 3.3087255464765417)