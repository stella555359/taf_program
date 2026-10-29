import os
from taf.config.testline.attenuator import TopYoung, Eubus


ATT_1   = ["TopYoung", "10.42.68.200",  "TAS_24T24_02G6_90_1C_EJS"]
ATT_2   = ["TopYoung", "10.42.61.32",   "TAS_24T24_02G6_90_1C_EJS"]
ATT_3   = ["TopYoung", "10.42.61.129",  "TAS_24T24_04G6_90_1S_EJS"]
ATT_4   = ["TopYoung", "10.42.61.181",  "TAS_24T24_04G6_90_1S_EJS"]
ATT_5   = ["TopYoung", "10.45.185.242", "TAS_24T24_02G6_90_1C_EJS"]
ATT_6   = ["TopYoung", "10.42.61.249",  "TAS_24T24_02G6_90_1S_EJS"]
ATT_7   = ["TopYoung", "10.42.54.39",   "TAS_24T24_02G6_90_1S_EJS"]
ATT_8   = ["TopYoung", "10.42.61.116",  "TAS_24T24_02G6_90_1S_EJS"]
ATT_11  = ["TopYoung", "10.42.221.54",  "TAS_24T24_04G6_90_1S_EJS"]
ATT_12  = ["Eubus", "10.42.170.3"]
ATT_13  = ["Eubus", "10.42.171.28"]
ATT_14  = ["TopYoung", "10.44.160.84",  "TAS_24T24_04G6_90_1S_EJS"]
ATT_15  = ["TopYoung", "10.42.171.52",  "TAS_24T24_04G6_90_1S_EJS"]
ATT_16  = ["TopYoung", "10.42.171.53",  "TAS_24T24_04G6_90_1S_EJS"]


def atten_qt(atten_nr, atten_port_numbers=None, port=None, atten_model=None):
    atten_nr_list = globals()[atten_nr]
    cls = globals()[atten_nr_list[0]]
    if atten_nr_list[0] == "TopYoung":
        if atten_port_numbers == None:
            atten_port_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        if port == None:
            port = 3001
        if atten_model == None:
            try:
                atten_model = atten_nr_list[2]
            except IndexError:
                atten_model = None
    elif atten_nr_list[0] == "Eubus":
        if atten_port_numbers == None:
            atten_port_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        if port == None:
            port = 23
        if atten_model == None:
            try:
                atten_model = atten_nr_list[2]
            except IndexError:
                atten_model = None

    return cls(
        ip_addr=atten_nr_list[1],
        attenuation_port_numbers=atten_port_numbers,
        port=port,
        model=atten_model
    )