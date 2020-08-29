#!/usr/bin/env/python
from math import pi

def find_volume_cylinder(r,l):
    '''
    Returns the volume of a cylinder.

    Parameters
    ----------
    r: float
        Radius of the cylinder.

    l: float
        Height of the cylinder.
    '''
    return pi * r * r * l

def diameter_to_radius(d):
    '''
    Converts diameter to radius

    Parameters
    ----------
    d: float
        Diameter to be converted to radius.
    '''
    return d/2

def inches_to_metres(inches):
    '''
    Converts value in inches to metres

    Parameters
    ----------
    inches: float
        Value in inches to be converted to metres.
    '''
    return inches / 39.37

def pascals_to_psi(pascals):
    '''
    Converts value in pascals to psi

    Parameters
    ----------
    pascals: float
        Value in pascals to be converted to psi.
    '''
    return pascals * 0.00014503773

def pounds_to_kg(pounds):
    '''
    Converts value in pounds to kg

    Parameters
    ----------
    pounds: float
        Value in pounds to be converted to kilogram
    '''
    return 0.45359237 * pounds

class TankDimensionsInches:
    '''
    Oxidizer tank dimensions given in inches and cubic inches.

    Oxidizer tank can be divided into five parts, represented by 5 different diameters and lengths.
    Refer to documentation for diagram of oxidizer tank. Same dimensions as TankDimensionsMetres
    '''
    #Diameter of each tank segment, d1 = index 1, d2 = index 2, etc...
    diameter = (None, 2.5, 3, 3.625, 3, 2.5)
    #Length of each tank segment, l1 = index 1, l2 = index 2, etc...
    length = (None, 0.5, 0.75, 37.125, 0.75, 0.875)
    #Radius of each tank segment, r1 = index 1, r2 = index 2, etc...
    radius = (None, diameter_to_radius(diameter[1]), diameter_to_radius(diameter[2]),\
       diameter_to_radius(diameter[3]), diameter_to_radius(diameter[4]),\
       diameter_to_radius(diameter[5]))
    #Volume of each tank segment, v1 = index 1, v2 = index 2, etc...
    volume = (None, find_volume_cylinder(radius[1],length[1]),\
       find_volume_cylinder(radius[2],length[2]),find_volume_cylinder(radius[3],length[3]),\
       find_volume_cylinder(radius[4],length[4]),find_volume_cylinder(radius[5],length[5]))

    #sum of lengths and volumes of each segment
    total_length = sum(length[1:])
    total_volume = sum(volume[1:])

#Oxidizer tank dimensions (metres and cubic metres)
#Uses values from TankDimensionsInches to calculate metric equivalents
class TankDimensionsMetres:
    '''
    Oxidizer tank dimensions given in metres and cubic metres.

    Uses values from TankDimensionsInches to calculate metric equivalents of the same dimensions.
    '''
    #Diameter of each tank segment, d1 = index 1, d2 = index 2, etc...
    diameter = (None, inches_to_metres(TankDimensionsInches.diameter[1]),\
       inches_to_metres(TankDimensionsInches.diameter[2]),\
       inches_to_metres(TankDimensionsInches.diameter[3]),\
       inches_to_metres(TankDimensionsInches.diameter[4]),\
       inches_to_metres(TankDimensionsInches.diameter[5]))
    #Length of each tank segment, l1 = index 1, l2 = index 2, etc...
    length = (None, inches_to_metres(TankDimensionsInches.length[1]),\
       inches_to_metres(TankDimensionsInches.length[2]),\
       inches_to_metres(TankDimensionsInches.length[3]),\
       inches_to_metres(TankDimensionsInches.length[4]),\
       inches_to_metres(TankDimensionsInches.length[5]))
    #Radius of each tank segment, r1 = index 1, r2 = index 2, etc...
    radius = (None, diameter_to_radius(diameter[1]), diameter_to_radius(diameter[2]),\
       diameter_to_radius(diameter[3]), diameter_to_radius(diameter[4]),\
       diameter_to_radius(diameter[5]))
    #Volume of each tank segment, v1 = index 1, v2 = index 2, etc...
    volume = (None, find_volume_cylinder(radius[1],length[1]),\
       find_volume_cylinder(radius[2],length[2]),find_volume_cylinder(radius[3],length[3]),\
       find_volume_cylinder(radius[4],length[4]),find_volume_cylinder(radius[5],length[5]))

    #sum of lengths and volumes of each segment
    total_length = sum(length[1:])
    total_volume = sum(volume[1:])

class NitrousOxideProperties:
    '''
    Properties of Nitrous Oxide (taken from ESDU 91022).
    '''
    critical_temp = 309.57          #kelvin (k)
    critical_pressure = 7251.0      #kilopascals (kPa)
    critical_density = 452.0        #kilograms per metres cubed (kg/m^3)

class EquationConstants:
    '''
    Constants for equations 4.1, 4.2, 4.3 (taken from ESDU 91022).
    '''
    eqn4_1 = (None,-6.71893, 1.35966, -1.3779, -4.051)
    eqn4_2 = (None, 1.72328, -0.8395, 0.5106, -0.10412)
    eqn4_3 = (None, -1.009, -6.28792, 7.50332, -7.90463, 0.629427)

class EngineInfo:
    '''
    Engine information.
    '''
    #Distance from the bottom of the fuel grain to the bottom of the oxidizer tank
    dist_to_tank_start = 25          #inches (in)

    fuel_grain_length = 24           #inches (in)
    fuel_grain_init_mass = 6.929129  #pounds (lb)
    fuel_grain_final_mass = 2.69     #pounds (lb)

    #need to update this later but im too lazy to do that now so will get to it when I get to it
    #Used by OpenRocket
    initWt = 0                       #grams (g)
    propWt = 0                       #grams (g)

class TestConditions:
    '''
    Conditions for testing
    '''
    local_atmos_pressure = 14.383    #pounds per square inch (psi)
    water_used_for_heating = 15      #pounds (lb)