import numpy as np

from NOS_mass_and_volume import NOSMassAndVolume as NMV
from constants import ConstantsManager as CM
from csv_extractor import CSVExtractor

ERROR_TOLERANCE = 0.001
SAMPLE_FILE_PATH = 'tests/sample_files/downsampled_NOS_mass_and_volume_sample_output.csv'


def test_calculate_liquid_volume():

    # Basic calculation cases
    assert np.allclose(NMV.calculate_liquid_volume(5, 150, 800, 0.0065), 0.006192,
                       rtol=ERROR_TOLERANCE)

    assert np.allclose(NMV.calculate_liquid_volume(1, 50, 1000, 0.0065), 0.0007105,
                       rtol=ERROR_TOLERANCE)

    # Zero return case
    assert np.allclose(NMV.calculate_liquid_volume(150*0.0065, 150, 800, 0.0065), 0.0,
                       rtol=ERROR_TOLERANCE)

    # Error Handling
    assert NMV.calculate_liquid_volume(5, 100, 100, 0.0065) == 0.0065


def test_with_sample_file():
    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(
        'tests/sample_files/downsampled_sample_DAQ_file.csv')

    consts = CM('tests/test_constants.yaml')
    nmv = NMV(raw_dat, i_constants=consts)

    with open(SAMPLE_FILE_PATH, 'r') as sample_file:
        for idx in range(len(raw_dat.time_s)):  # all lists the same length
            current_line_split = sample_file.readline().split(',')
            assert np.allclose(raw_dat.time_s[idx],
                               float(current_line_split[0]), rtol=ERROR_TOLERANCE)
            assert np.allclose(raw_dat.adjusted_mass_lb[idx],
                               float(current_line_split[1]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.NOS_mass_kg[idx], float(current_line_split[2]),
                               rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.DAQ_pressure_to_density_data.density_liquid_kg_m3[idx],
                               float(current_line_split[3]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.DAQ_pressure_to_density_data.gas_density_kg_m3[idx],
                               float(current_line_split[4]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.liquid_volume_m3[idx], float(current_line_split[5]),
                               rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.vapour_volume_m3[idx], float(current_line_split[6]),
                               rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.liquid_mass_kg[idx],
                               float(current_line_split[7]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.vapour_mass_kg[idx],
                               float(current_line_split[8]), rtol=ERROR_TOLERANCE)
