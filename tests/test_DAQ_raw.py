import numpy as np

from DAQ_raw import DAQRaw
from constants import ConstantsManager as CM
ERROR_TOLERANCE = 0.01


def test_basic_setup():
    test_time_list = [100, 101, 102, 103]
    test_tank_pressure_list = [700, 650, 600, 550]
    test_recorded_masses = [26, 27.5, 27.4, 27.3]
    test_thrust_values = [0, 70, 90, 100]

    test_conditions = CM('tests/test_constants.yaml').test_conditions
    LOCAL_ATM_P = test_conditions['local_atmos_pressure']
    WATER_WEIGHT = test_conditions['water_used_for_heating']

    raw_DAQ_sample = DAQRaw(test_time_list, test_tank_pressure_list,
                            test_recorded_masses, test_thrust_values, test_conditions)

    assert raw_DAQ_sample.time_s is not None
    shared_data_length = len(raw_DAQ_sample.time_s)
    assert shared_data_length == 4

    assert raw_DAQ_sample.tank_pressure_psig is not None
    assert len(raw_DAQ_sample.tank_pressure_psig) == shared_data_length

    assert raw_DAQ_sample.tank_pressure_psia is not None
    assert len(raw_DAQ_sample.tank_pressure_psia) == shared_data_length

    assert raw_DAQ_sample.recorded_mass_lb is not None
    assert len(raw_DAQ_sample.recorded_mass_lb) == shared_data_length

    assert raw_DAQ_sample.adjusted_mass_lb is not None
    assert len(raw_DAQ_sample.adjusted_mass_lb) == shared_data_length

    assert raw_DAQ_sample.thrust_lb is not None
    assert len(raw_DAQ_sample.thrust_lb) == shared_data_length

    for idx in range(shared_data_length):
        assert np.allclose(raw_DAQ_sample.time_s[idx], test_time_list[idx],
                           rtol=ERROR_TOLERANCE)
        assert np.allclose(raw_DAQ_sample.tank_pressure_psig[idx], test_tank_pressure_list[idx],
                           rtol=ERROR_TOLERANCE)
        assert np.allclose(raw_DAQ_sample.recorded_mass_lb[idx], test_recorded_masses[idx],
                           rtol=ERROR_TOLERANCE)
        assert np.allclose(raw_DAQ_sample.thrust_lb[idx], test_thrust_values[idx],
                           rtol=ERROR_TOLERANCE)

        assert np.allclose(raw_DAQ_sample.tank_pressure_psia[idx],
                           (raw_DAQ_sample.tank_pressure_psig[idx] + LOCAL_ATM_P),
                           rtol=ERROR_TOLERANCE)

        assert np.allclose(raw_DAQ_sample.adjusted_mass_lb[idx],
                           (raw_DAQ_sample.recorded_mass_lb[idx] -
                            WATER_WEIGHT),
                           rtol=ERROR_TOLERANCE)
