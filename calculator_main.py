from csv_extractor import CSVExtractor
from NOS_mass_and_volume import NOSMassAndVolume
from NOS_vapour_CG import NOSVapourCG
from NOS_liquid_CG import NOSLiquidCG
from engine_CG import EngineCG
from engine_XML import EngineXML
from constants import ConstantsManager


def execute_calculation(data_file_path, target_path,
                        constants_file_path=None, suppress_printout=False):
    '''
    Execute all calculations and save the results to an output file.

    Parameters
    ----------
    data_file_path: str
        This is the path pointing to the file where the DAQ data.
    target_path: str
        This is the path where the output is to be saved to.
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
        print('calculation successful')
