from csv_extractor import CSVExtractor
from NOS_mass_and_volume import NOSMassAndVolume
from NOS_vapour_CG import NOSVapourCG
from NOS_liquid_CG import NOSLiquidCG
from engine_CG import EngineCG
from engine_XML import EngineXML


if __name__ == '__main__':
    print('Please enter the filepath of the raw DAQ date to be used')
    file_path = input()
    extractor = CSVExtractor()
    DAQ_data =  extractor.extract_data_to_raw_DAQ(file_path)
    NOS_mass_volume = NOSMassAndVolume(DAQ_data)
    NOS_liquid_CG = NOSLiquidCG(NOS_mass_volume)
    NOS_vapour_CG = NOSVapourCG(NOS_mass_volume, NOS_liquid_CG)
    engine_CG = EngineCG(DAQ_data, NOS_vapour_CG, NOS_liquid_CG)
    engine_XML = EngineXML(DAQ_data, engine_CG)
    
    file = open('poopyxml.txt', 'w')
    for tag in engine_XML.XML_tags:
        file.write(tag)
        file.write('\n')
        
    file.close()