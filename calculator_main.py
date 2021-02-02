from csv_extractor import CSVExtractor
from NOS_mass_and_volume import NOSMassAndVolume
from NOS_vapour_CG import NOSVapourCG
from NOS_liquid_CG import NOSLiquidCG
from engine_CG import EngineCG
from engine_XML import EngineXML


def execute_calculation(data_file_path, target_path, \
                        constants_file_path = None, supress_printout = False):

    extractor = CSVExtractor()
    DAQ_data =  extractor.extract_data_to_raw_DAQ(data_file_path)
    NOS_mass_volume = NOSMassAndVolume(DAQ_data)
    NOS_liquid_CG = NOSLiquidCG(NOS_mass_volume)
    NOS_vapour_CG = NOSVapourCG(NOS_mass_volume, NOS_liquid_CG)
    engine_CG = EngineCG(DAQ_data, NOS_vapour_CG, NOS_liquid_CG)
    engine_XML = EngineXML(DAQ_data, engine_CG)

    file = open(target_path, 'w')
    for tag in engine_XML.XML_tags:
        file.write(tag)
        file.write('\n')

    file.close()
    if not supress_printout:
        print('calculation sucessful')
