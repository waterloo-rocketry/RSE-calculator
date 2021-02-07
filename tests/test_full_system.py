import xml.etree.ElementTree as ET

from calculator_main import execute_calculation


def test_full_system():
    xml_from_string = ET.fromstring

    execute_calculation(
        'test_csv.csv', 'output_testcase_xml.txt', suppress_printout=True)

    correct_file = open('data\\correct_xml.txt')
    new_file = open('output_testcase_xml.txt')

    for line in correct_file:
        other_line = new_file.readline()

        correct_line_dict = xml_from_string(line).attrib
        other_line_dict = xml_from_string(other_line).attrib

        for key in correct_line_dict.keys():
            assert abs(float(correct_line_dict[key]) - float(other_line_dict[key])) <= \
                abs(float(correct_line_dict[key]))/100
