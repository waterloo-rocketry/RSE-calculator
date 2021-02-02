from constants import ConstantsManager as CM
from engine_XML import EngineXML as EXML

ERROR_TOLERANCE = 0.001

def test_recalculate_propellant_CG_mm():
    cm = CM('data\\test_constants.yaml')

    assert abs(EXML.recalculate_propellant_CG_mm(0, cm) - 1651.0) < 1651.0*ERROR_TOLERANCE
    assert abs(EXML.recalculate_propellant_CG_mm(0.5, cm) - 1638.3) < 1638.3*ERROR_TOLERANCE
    assert abs(EXML.recalculate_propellant_CG_mm(30, cm) - 889.0) < 889.0*ERROR_TOLERANCE

def test_prepare_XML_tag_for_data_point():

    t1_correct ='<eng-data t="0.00" f="0.74" m="8125.563" cg="846.349"/>'
    assert EXML.prepare_XML_tag_for_data_point(0, 0.739, 8125.5631, 846.34928) == t1_correct

    t2_correct ='<eng-data t="0.00" f="0.10" m="1000.000" cg="100.000"/>'
    assert EXML.prepare_XML_tag_for_data_point(0, 0.1, 1000, 100) == t2_correct

    t3_correct ='<eng-data t="0.00" f="0.10" m="1000.000" cg="100.000"/>'
    assert EXML.prepare_XML_tag_for_data_point(0, 0.0999, 999.9999, 99.9999) == t3_correct
