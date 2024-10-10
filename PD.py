#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  10 14:10:56 2024

@author: denis
"""

import nazca as nd
import nazca.geometries as geom
from nazca.interconnects import Interconnect
import nazca.gds_base as base
import nazca.demofab as demo

import re
import math
import random
from itertools import product 

        
# base.gds_db_unit = 5e-9
# base.gds_db_user = 0.001

wg = 0.6
R = 50
edge_offset = 20
edge_taper_length = 300
die_x = 5210
die_y = 4870
 
 
nd.add_layer(name='x1', layer=(2,0), accuracy=0.005)
nd.add_xsection('xs1')
nd.add_layer2xsection(xsection='xs1', layer='x1')

ic = Interconnect(xs='xs1', width=wg, radius=R)


with nd.Cell('background_cell') as background:
   
    sq1 = geom.box(length=die_x, width=die_y) 
    sq2 = geom.box(length=die_x-20, width=die_y-20)
    nd.Polygon(points=sq1, layer=(100,2)).put()
    nd.Polygon(points=sq2, layer=(100,0)).put(10,0)


def load_grating(filename='gratings.gds'):
    
    with nd.Cell(name='grating') as grating: 
        var = nd.load_gds(
            filename=filename,
            cellname='Grat_400'
            )
        var.put()
        nd.Pin('a0').put(0, 0, 180)
        nd.Pin('b0').put(0, 0, 0)
        # nd.Pin('b0').put(var.bbox[2], var.bbox[3], 0)
        nd.put_stub()
    return grating


def backloop_gen(coupler_cell, pitch=250, lgth = 200):  
    
    with nd.Cell('GC_backloop_' + coupler_cell.__class__.__name__) as bb:             
        coupler_cell.put()
        ic.strt(lgth).put()
        ic.bend(angle=90).put()
        ic.strt(pitch - 2*R).put()
        ic.bend(angle=90).put()
        ic.strt(lgth).put()
        coupler_cell.put(flop=True)           
    return bb


def PD_gen(Ge_length=200, Ge_width=4):  
 
    with nd.Cell('PD_' + str(Ge_length) + "_" + str(Ge_width)) as bb:            
        # define xsection
        xsd = nd.add_xsection(name='XSD_'+ str(random.randint(0,10)))
        xsd.width = wg
        xsd.radius= R
        # create layers in a xsection
        nd.add_layer(name='wg_d', layer=(2,0))
        nd.add_layer(name='ge_clad', layer=(101,1))
        nd.add_layer(name='ge_wrap', layer=(102,1))
        nd.add_layer(name='ge_omic', layer=(103,1))
        nd.add_layer(name='ge_pin', layer=(104,1))

        nd.add_layer2xsection(xsection=xsd, layer='wg_d', accuracy=0.001)
        nd.add_layer2xsection(xsection=xsd, layer='ge_clad', accuracy=0.001, growx=Ge_width)
        nd.add_layer2xsection(xsection=xsd, layer='ge_wrap', accuracy=0.01, growx=Ge_width+6)  
        
        nd.add_layer2xsection(xsection=xsd, layer='ge_omic', accuracy=0.01, leftedge=(5, 6.0), rightedge=(5.0, 3.0))
        nd.add_layer2xsection(xsection=xsd, layer='ge_omic', accuracy=0.01, leftedge=(-5, -3.0), rightedge=(-5.0, -6.0))
        
        nd.add_layer2xsection(xsection=xsd, layer='ge_pin', accuracy=0.01, leftedge=(10, 60.0), rightedge=(5.0, 2.0))
        nd.add_layer2xsection(xsection=xsd, layer='ge_pin', accuracy=0.01, leftedge=(-5, -2.0), rightedge=(-5.0, -60.0))
             
        nd.strt(length=100, width=wg, xs=xsd).put(0)       
    return bb


def GC_PD_gen(grating_cell, PD_cell):
    
    with nd.Cell('GC_PD_' + PD_cell.__class__.__name__) as bb:              
        grating_cell.put()
        ic.strt(700).put()
        ic.sbend(offset=-100).put()
        ic.strt(700).put()
        PD_cell.put()          
    return bb



with nd.Cell('TOP') as top:
    
    pitch = 250  # fiber array pitch distance   
    background.put(0,die_y/2)  
    nd.cp.move(1000,-die_y/2+300)
    
    # Fiber array couplers generation
    # In case of broadband source this cell can be substituted by edge coupler cell if alignment precission allows to do that
    coupler_cell = load_grating()   
    backloop_gen(coupler_cell, pitch=pitch).put()
    
    nd.cp.move(0,2*pitch)   
    Ge_length = [200, 300]
    Ge_width = [4, 5]
    permute = product(Ge_length, Ge_width)
    
    # PD allocation
    for var in permute:
        
        PD_cell = PD_gen(*var)  
        GC_PD_gen(coupler_cell, PD_cell).put()
        
        # Text
        cp = nd.cp.get_xy()
        nd.cp.move(0,-80)
        nd.text(str(var), height=50, layer='x1').put()
        nd.cp.goto(*cp)
        
        nd.cp.move(0,pitch)
    
    # closing backloop allocation  
    backloop_gen(coupler_cell, pitch=pitch).put()
    
    
nd.export_gds(top, filename="PD.gds")





