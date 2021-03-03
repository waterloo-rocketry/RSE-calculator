import xml.etree.ElementTree as ET
import numpy as np

from calculator_main import execute_calculation

ERROR_TOLERANCE = 0.001


def test_full_system():
    xml_from_string = ET.fromstring

    execute_calculation('tests/sample_files/sample_DAQ_file.csv',
                        'tests/output_testcase_xml.txt', suppress_printout=True)

    correct_file = open('tests/sample_files/created_correct_xml.txt')
    new_file = open('tests/output_testcase_xml.txt')

    for line in correct_file:
        other_line = new_file.readline()

        correct_line_dict = xml_from_string(line).attrib
        other_line_dict = xml_from_string(other_line).attrib

        for key in correct_line_dict.keys():
            assert np.allclose(float(correct_line_dict[key]), float(other_line_dict[key]),
                               rtol=ERROR_TOLERANCE)

    correct_file.close()
    new_file.close()
