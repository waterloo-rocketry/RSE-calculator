

def timestrech_thurst_curve(data, strech_factor):
    '''
    Streches a thrust curve while maintaining total burn impulse.


    NOTE: Since the end_of_burn is saved as an index when the DAQ is instantiated 
    it does not need to be modified here 

    Parameters
    ----------
    data: RSE-calculator.DAQRaw
        The data structure containing all of the DAQ data to be modified.

    Returns
    -------
    RSE-calculator.DAQRaw:
        The modified DAQ file.

    '''

    if strech_factor == 1:
        return data

    for idx in range(len(data.time_s)):
        data.time_s[idx] = data.time_s[idx]*strech_factor
        data.thrust_lb[idx] = data.thrust_lb[idx]/strech_factor

    return data


def get_burn_impulse(data, end_of_burn_idx=0):
    '''
    Calculate the impulse of a burn specified within a DAQRaw object

    Parameters
    ----------
    data: RSE-calculator.DAQRaw
        The data structure containing all of the DAQ data for which the impulse
        is to be calculated.
    end_of_burn_idx:
        The index at which the end of the burn occurs. The default value is zero, 
        in which case it will use the length of the whole daq file. 
    Returns
    -------
    float:
        The impulse of the specified burn
    '''
    impulse = 0

    if end_of_burn_idx == 0:
        end_of_burn_idx = len(data.time_s)

    for idx in range(1, end_of_burn_idx):
        dt = data.time_s[idx] - data.time_s[idx - 1]
        impulse += dt*0.5*(data.thrust_lb[idx] + data.thrust_lb[idx - 1])

    return impulse
