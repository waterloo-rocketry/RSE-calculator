#!/usr/bin/env/python
from math import pi

#Returns volume of cylinder given radius and length
def find_volume_cylinder(r,l):
    return pi * r * r * l

#Converts diameter to radius (divide it by two)
def diameter_to_radius(d):
    return d/2

#Converts value in inches to metres
def inches_to_metres(inches):
    return inches / 39.37

#Oxidizer tank dimensions (inches and cubic inches)
#Tank can be divided into 5 parts, represented by 5 different diameters and lengths
class TankDimensionsInches:
    diameter = (None, 2.5, 3, 3.625, 3, 2.5)
    length = (None, 0.5, 0.75, 37.125, 0.75, 0.875)
    radius = (None, diameter_to_radius(diameter[1]), diameter_to_radius(diameter[2]), diameter_to_radius(diameter[3]), diameter_to_radius(diameter[4]), diameter_to_radius(diameter[5]))
    volume = (None, find_volume_cylinder(radius[1],length[1]), find_volume_cylinder(radius[2],length[2]),find_volume_cylinder(radius[3],length[3]),find_volume_cylinder(radius[4],length[4]),find_volume_cylinder(radius[5],length[5]))

    total_length = sum(length, 1)
    total_volume = sum(volume, 1)

#Oxidizer tank dimensions (metres and cubic metres)
#Uses values from TankDimensionsInches to calculate metric equivalents
class TankDimensionsMetres:
    diameter = (None, inchesToMetres(TankDimensionsInches.diameter[1]), inchesToMetres(TankDimensionsInches.diameter[2]), inchesToMetres(TankDimensionsInches.diameter[3]), inchesToMetres(TankDimensionsInches.diameter[4]), inchesToMetres(TankDimensionsInches.diameter[5]))
    length = (None, inchesToMetres(TankDimensionsInches.length[1]), inchesToMetres(TankDimensionsInches.length[2]), inchesToMetres(TankDimensionsInches.length[3]), inchesToMetres(TankDimensionsInches.length[4]), inchesToMetres(TankDimensionsInches.length[5]))
    radius = (None, diameter_to_radius(diameter[1]), diameter_to_radius(diameter[2]), diameter_to_radius(diameter[3]), diameter_to_radius(diameter[4]), diameter_to_radius(diameter[5]))
    volume = (None, find_volume_cylinder(radius[1],length[1]), find_volume_cylinder(radius[2],length[2]),find_volume_cylinder(radius[3],length[3]),find_volume_cylinder(radius[4],length[4]),find_volume_cylinder(radius[5],length[5]))

    #sum of lengths and volumes
    total_length = sum(length, 1)
    total_volume = sum(volume, 1)

#Properties of Nitrous Oxide (taken from ESDU 91022)
class NitrousOxideProperties:
    critical_temp = 309.57        #kelvin (k)
    critical_pressure = 7251      #kilopascals (kPa)
    critical_density = 452        #kilograms per metres cubed (kg/m^3)

#Constants for equations 4.1, 4.2, 4.3 (taken from ESDU 91022)
class EquationConstants:
    eqn4_1 = (None,-6.71893, 1.35966, -1.3779, -4.051)
    eqn4_2 = (None, 1.72328, -0.8395, 0.5106, -0.10412)
    eqn4_3 = (None, -1.009, -6.28792, 7.50332, -7.90463, 0.629427)

#Engine Information
class EngineInfo:
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
    local_atmos_pressure = 14.383    #pounds per square inch (psi)
    water_used_for_heating = 15      #pounds (lb)