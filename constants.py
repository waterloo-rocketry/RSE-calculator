#!/usr/bin/env/python
from math import pi

#Returns volume of cylinder given radius and length
def findVolumeCylinder(r,l):
    return pi * r * r * l

#Converts diameter to radius (divide it by two)
def diameterToRadius(d):
    return d/2

#Converts value in inches to metres
def inchesToMetres(inches):
    return inches / 39.37

#Oxidizer tank dimensions (inches and cubic inches)
#Tank can be divided into 5 parts, represented by 5 different diameters and lengths
class TankDimensionsInches:
    diameter = (None, 2.5, 3, 3.625, 3, 2.5)
    length = (None, 0.5, 0.75, 37.125, 0.75, 0.875)
    radius = (None, diameterToRadius(diameter[1]), diameterToRadius(diameter[2]), diameterToRadius(diameter[3]), diameterToRadius(diameter[4]), diameterToRadius(diameter[5]))
    volume = (None, findVolumeCylinder(radius[1],length[1]), findVolumeCylinder(radius[2],length[2]),findVolumeCylinder(radius[3],length[3]),findVolumeCylinder(radius[4],length[4]),findVolumeCylinder(radius[5],length[5]))

    totalLength = sum(length, 1)
    totalVolume = sum(volume, 1)

#Oxidizer tank dimensions (metres and cubic metres)
#Uses values from TankDimensionsInches to calculate metric equivalents
class TankDimensionsMetres:
    diameter = (None, inchesToMetres(TankDimensionsInches.diameter[1]), inchesToMetres(TankDimensionsInches.diameter[2]), inchesToMetres(TankDimensionsInches.diameter[3]), inchesToMetres(TankDimensionsInches.diameter[4]), inchesToMetres(TankDimensionsInches.diameter[5]))
    length = (None, inchesToMetres(TankDimensionsInches.length[1]), inchesToMetres(TankDimensionsInches.length[2]), inchesToMetres(TankDimensionsInches.length[3]), inchesToMetres(TankDimensionsInches.length[4]), inchesToMetres(TankDimensionsInches.length[5]))
    radius = (None, diameterToRadius(diameter[1]), diameterToRadius(diameter[2]), diameterToRadius(diameter[3]), diameterToRadius(diameter[4]), diameterToRadius(diameter[5]))
    volume = (None, findVolumeCylinder(radius[1],length[1]), findVolumeCylinder(radius[2],length[2]),findVolumeCylinder(radius[3],length[3]),findVolumeCylinder(radius[4],length[4]),findVolumeCylinder(radius[5],length[5]))

    #sum of lengths and volumes
    totalLength = sum(length, 1)
    totalVolume = sum(volume, 1)

#Properties of Nitrous Oxide (taken from ESDU 91022)
class NitrousOxideProperties:
    criticalTemp = 309.57        #kelvin (k)
    criticalPressure = 7251      #kilopascals (kPa)
    criticalDensity = 452        #kilograms per metres cubed (kg/m^3)

#Constants for equations 4.1, 4.2, 4.3 (taken from ESDU 91022)
class EquationConstants:
    Eqn4_1 = (None,-6.71893, 1.35966, -1.3779, -4.051)
    Eqn4_2 = (None, 1.72328, -0.8395, 0.5106, -0.10412)
    Eqn4_3 = (None, -1.009, -6.28792, 7.50332, -7.90463, 0.629427)

#Engine Information
class EngineInfo:
    #Distance from the bottom of the fuel grain to the bottom of the oxidizer tank
    distToTankStart = 25          #inches (in)

    fuelGrainLength = 24          #inches (in)
    fuelGrainInitMass = 6.929129  #pounds (lb)
    fuelGrainFinalMass = 2.69     #pounds (lb)

    #need to update this later but im too lazy to do that now so will get to it when I get to it
    #Used by OpenRocket
    initWt = 0                    #grams (g)
    propWt = 0                    #grams (g)

class TestConditions:
    localAtmosPressure = 14.383   #pounds per square inch (psi)
    waterUsedForHeating = 15      #pounds (lb)