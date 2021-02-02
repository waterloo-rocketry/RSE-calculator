#!/usr/bin/env/python
from math import pi
import copy
import yaml


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
    return inches / 39.37007874

def metres_to_inches(metres):
    '''
    Converts value in metres to inches

    Parameters
    ----------
    metres: float
        Value in metres to be converted to inches
    '''

    return metres * 39.37007874

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

def kg_to_pounds(kg):
    '''
    Converts value in kg to pounds

    Parameters
    ----------
    kg: float
        Value in kg to be converted to pounds
    '''

    return 2.20462262185 * kg

def pounds_to_N(pounds):
    '''
    Converts value in pounds force to newtons

    Parameters
    ----------
    pounds: float
        Value in pounds to be converted to newtons
    '''
    return 4.44822 * pounds

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

class ConstantsManager:
    '''
    A constants manager class based on configuration file loading
    '''
    DEFAULT_PATH = 'data\\constant_config.yaml' # Default path of the configuration settings

    def __init__(self, path = None):
        self.tank_dimensions_inches = {}
        self.tank_dimensions_meters = {}
        self.nitrous_oxide_properties = {}
        self.engine_info = {}
        self.test_conditions = {}

        if path is None:
            path = self.DEFAULT_PATH

        self.load_config(path)

    def load_config(self, path):
        '''
        Loads the configuration at the target path into local fields

        Parameters
        ----------
        path: str
            The path at which the configuration file is.

        '''

        with open(path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        self.tank_dimensions_inches = self.load_tank_dims_inches(data['TankDimensionsInches'])
        self.tank_dimensions_meters = self.load_tank_dims_meters(self.tank_dimensions_inches)
        self.nitrous_oxide_properties = data['NitrousOxideProperties']
        self.equation_constants = data['EquationConstants']
        self.engine_info = data['EngineInfo']
        self.test_conditions = data['TestConditions']

    @staticmethod
    def load_tank_dims_inches(yaml_data):
        '''
        Process and complete tank dimension data

        Parameters
        ----------
        yaml_data: dict
            The base data from the configuration file

        Returns
        -------

        dict:
            A new dict containing the complete data concerning the tank dimensions
        '''

        diameter = yaml_data['diameter']
        length = yaml_data['length']

        radius = (None, diameter_to_radius(diameter[1]),\
            diameter_to_radius(diameter[2]),\
            diameter_to_radius(diameter[3]), diameter_to_radius(diameter[4]),\
            diameter_to_radius(diameter[5]))
        volume = (None, find_volume_cylinder(radius[1],length[1]),\
            find_volume_cylinder(radius[2],length[2]),find_volume_cylinder(radius[3],length[3]),\
            find_volume_cylinder(radius[4],length[4]),find_volume_cylinder(radius[5],length[5]))

        return_data = copy.deepcopy(yaml_data)
        return_data['radius'] = radius
        return_data['volume'] = volume

        #sum of lengths and volumes of each segment
        return_data['total_length'] = sum(length[1:])
        return_data['total_volume'] = sum(volume[1:])

        return return_data

    @staticmethod
    def load_tank_dims_meters(inches_data):
        '''
        Convert the tank dimensions data dict in inches to a new one in meters.

        Parameters
        ----------
        inches_data: dict
            The data in inches

        Returns
        -------

        dict:
            A new dict containing the complete data concerning the tank dimensions, but in meters.
        '''
        return_data = {}

        #Diameter of each tank segment, d1 = index 1, d2 = index 2, etc...
        diameter = (None, inches_to_metres(inches_data['diameter'][1]),\
           inches_to_metres(inches_data['diameter'][2]),\
           inches_to_metres(inches_data['diameter'][3]),\
           inches_to_metres(inches_data['diameter'][4]),\
           inches_to_metres(inches_data['diameter'][5]))
        #Length of each tank segment, l1 = index 1, l2 = index 2, etc...
        length = (None, inches_to_metres(inches_data['length'][1]),\
           inches_to_metres(inches_data['length'][2]),\
           inches_to_metres(inches_data['length'][3]),\
           inches_to_metres(inches_data['length'][4]),\
           inches_to_metres(inches_data['length'][5]))
        #Radius of each tank segment, r1 = index 1, r2 = index 2, etc...
        radius = (None, diameter_to_radius(diameter[1]), diameter_to_radius(diameter[2]),\
           diameter_to_radius(diameter[3]), diameter_to_radius(diameter[4]),\
           diameter_to_radius(diameter[5]))
        #Volume of each tank segment, v1 = index 1, v2 = index 2, etc...
        volume = (None, find_volume_cylinder(radius[1],length[1]),\
           find_volume_cylinder(radius[2],length[2]),find_volume_cylinder(radius[3],length[3]),\
           find_volume_cylinder(radius[4],length[4]),find_volume_cylinder(radius[5],length[5]))

        return_data['diameter'] = diameter
        return_data['length'] = length
        return_data['radius'] = radius
        return_data['volume'] = volume

        #sum of lengths and volumes of each segment
        return_data['total_length'] = sum(length[1:])
        return_data['total_volume'] = sum(volume[1:])

        return return_data

