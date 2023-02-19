from csv_extractor import CSVExtractor
from NOS_mass_and_volume import NOSMassAndVolume
from NOS_vapour_CG import NOSVapourCG
from NOS_liquid_CG import NOSLiquidCG
from engine_CG import EngineCG
from engine_XML import EngineXML
from constants import ConstantsManager
from scaling_and_experimentation import timestrech_thurst_curve, get_burn_impulse

import yaml

DEBUG_MODE = False

def execute_calculation(data_file_path, target_path, modification_parameters=None,
                        constants_file_path=None, suppress_printout=False):
    '''
    Execute all calculations and save the results to an output file.

    Parameters
    ----------
    data_file_path: str
        This is the path pointing to the file where the DAQ data.
    target_path: str
        This is the path where the output is to be saved to.
    modifcation_parameters: dict
        Parameters for modying the given DAQ data (for when the calculation is being executed
        as part of a parameter sweep).
    constants_file_path: str
        The path to the constants yaml file. Defaults to none, in which case a default one will
        be used.
    suppress_printout: bool
        Whether the 'calculation successful' printout needs to be supressed or not. Default to 
        false, which means it will print. 
    '''

    constants = None
    if constants_file_path:
        constants = ConstantsManager(constants_file_path)

    extractor = CSVExtractor()
    DAQ_data = extractor.extract_data_to_raw_DAQ(data_file_path)

    if modification_parameters:
        DAQ_data = timestrech_thurst_curve(DAQ_data, modification_parameters['timestretch_factor'])
    
    if DEBUG_MODE:
        print('Burn impulse after time-stretch is ' + str(get_burn_impulse(DAQ_data)))

    NOS_mass_volume = NOSMassAndVolume(DAQ_data, i_constants=constants)
    NOS_liquid_CG = NOSLiquidCG(NOS_mass_volume, i_constants=constants)
    NOS_vapour_CG = NOSVapourCG(
        NOS_mass_volume, NOS_liquid_CG, i_constants=constants)
    engine_CG = EngineCG(DAQ_data, NOS_vapour_CG,
                         NOS_liquid_CG, i_constants=constants)
    engine_XML = EngineXML(DAQ_data, engine_CG, i_constants=constants)

    with open(target_path, 'w') as file:
        for tag in engine_XML.XML_tags:
            file.write(tag)
            file.write('\n')

    if not suppress_printout:
        if modification_parameters:
            print('Modification parameters: ', end='')
            print(modification_parameters, end=' ')
            
        print(' [Calculation successful]')
        
        
def default_mode():
    '''
    Runs the calculator in default mode (i.e.) processes a single DAQ file into a single RSE file.
    '''
    # In case someone wants to hard-code a value into this in the future
    DAQ_PATH = None
    TARGET_PATH = None

    print('-- Calculator launched in default mode --\n')
    if DAQ_PATH is None:
        print('Please enter the filepath of the raw DAQ data to be used')
        daq_path = input()
    else:
        daq_path = DAQ_PATH

    if TARGET_PATH is None:
        print('Please enter the filepath to which the xml will be saved')
        target_path = input()
        if target_path == '':
            target_path = 'outputxml.txt'
    else:
        target_path = TARGET_PATH

    execute_calculation(daq_path, target_path)
    

def parameter_sweep_mode(config):
    '''
    Runs the calculator in parameter sweep mode, where a single base set of DAQ data is taken,
    and then a set of RSE files based on the specified requirements is provided.
    
    Parameters
    ----------
    config: dict
        The configuration of the parameter sweep, based on the contents of the loaded YAML file
    '''
    
    # In case someone wants to hard-code a value into this in the future
    DAQ_PATH = None
    TARGET_FOLDER_PATH = None
    
    print('-- Calculator launched in parameter sweep mode --\n')
    if DAQ_PATH is None:
        print('Please enter the filepath of the raw DAQ data to be used')
        daq_path = input()
    else:
        daq_path = DAQ_PATH
        
    if TARGET_FOLDER_PATH is None:
        print('Please enter the name (or path) of the folder that will contain' +\
              ' the simulation outputs (file names will be assigned programatically based' +\
              ' on the paramters used in creating it).')
        target_folder_path = input()
        if target_folder_path == '':
            target_folder_path = 'simulation_results'
    else:
        target_folder_path = TARGET_FOLDER_PATH

    import os

    if not os.path.isdir(target_folder_path):
        os.mkdir(target_folder_path)

    for itm in config['factors_to_simulate']:
        target_path = os.path.join(target_folder_path, f'timestretch_factor_{itm}.txt')
        target_parameters = {'timestretch_factor' : itm}
        execute_calculation(daq_path, target_path, modification_parameters = target_parameters)

def run_calculator():
    '''
    Runs the calculator, either as a single run or as part of a parameter sweep.
    '''
    
    with open('experimental_config.yaml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    
    if data['execute_experimental_simulation']:
        parameter_sweep_mode(data)
    else:
        default_mode()
    
