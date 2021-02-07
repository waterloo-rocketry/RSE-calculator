from builtins import round

from constants import ConstantsManager as ConstsM

from vapour_pressure_calculations import VapourPressureCalculations as vpc_class

SAMPLE_FILE_PATH = 'data/downsampled_vapour_pressure_sample_output.csv'


def test_eqn4_1():
    consts = ConstsM('data\\test_constants.yaml')

    vpc_sample = vpc_class()
    result_1 = vpc_sample.eqn4_1(0.6, 0.4, consts)
    assert round(result_1, 3) == 107.917
    result_2 = vpc_sample.eqn4_1(0.9, 0.1, consts)
    assert round(result_2, 3) == 3587.583
    result_3 = vpc_sample.eqn4_1(1, 0, consts)
    assert round(result_3, 3) == 7251.0


def test_basic_setup():
    consts = ConstsM('data\\test_constants.yaml')
    vpc_sample = vpc_class(i_constants=consts)

    # Check for validity of temperature list
    assert vpc_sample.t_deg_c is not None and len(vpc_sample.t_deg_c) != 0

    # Check for length continuity in all lists
    assert len(vpc_sample.t_deg_c) == len(vpc_sample.t_kelvin)
    assert len(vpc_sample.t_deg_c) == len(vpc_sample.t_reduced)
    assert len(vpc_sample.t_deg_c) == len(vpc_sample.one_minus_t_reduced)
    assert len(vpc_sample.t_deg_c) == len(vpc_sample.pressure_kpa)
    assert len(vpc_sample.t_deg_c) == len(vpc_sample.pressure_psi)

    for idx in range(len(vpc_sample.t_deg_c)):
        assert vpc_sample.t_kelvin[idx] == vpc_sample.t_deg_c[idx] + 273.15

    for idx in range(len(vpc_sample.t_reduced)):
        assert vpc_sample.t_kelvin[idx] / consts.nitrous_oxide_properties['critical_temp'] == \
            vpc_sample.t_reduced[idx]


def test_with_sample_file():

    sample_file = open(SAMPLE_FILE_PATH, 'r')
    consts = ConstsM('data\\test_constants.yaml')
    vpc_object = vpc_class(i_constants=consts)
    downsample_factor = 10

    for idx in range(len(vpc_object.t_deg_c)):  # all lists the same length
        if idx % downsample_factor == 0:
            current_line_split = sample_file.readline().split(',')
            assert vpc_object.t_deg_c[idx] == float(current_line_split[0])
            assert vpc_object.t_kelvin[idx] == float(current_line_split[1])
            assert vpc_object.t_reduced[idx] == float(current_line_split[2])
            assert vpc_object.one_minus_t_reduced[idx] == float(
                current_line_split[3])
            assert vpc_object.pressure_kpa[idx] == float(current_line_split[4])
            assert vpc_object.pressure_psi[idx] == float(current_line_split[5])
