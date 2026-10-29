import os
from taf.config.testline.pdu import PduPort, Gude, ATEN, APC


PDU_1  = ["Gude", "10.44.205.225"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_2  = ["Gude", "10.44.205.9"]                #[PDU type, PDU ip address, optional:PDU version]
PDU_3  = ["Gude", "10.44.206.27"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_4  = ["Gude", "10.44.177.92"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_5  = ["Gude", "10.44.177.91"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_6  = ["ATEN", "10.44.206.125"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_7  = ["Gude", "10.44.177.21"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_8  = ["ATEN", "10.42.61.175"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_9  = ["Gude", "10.44.177.94"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_10 = ["Gude", "10.44.206.238", "8220-1"]    #[PDU type, PDU ip address, optional:PDU version]
PDU_11 = ["Gude", "10.44.206.11"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_12 = ["Gude", "10.44.206.144", "8220-1"]    #[PDU type, PDU ip address, optional:PDU version]
PDU_13 = ["ATEN", "10.44.206.123"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_14 = ["ATEN", "10.42.61.176"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_15 = ["Gude", "10.44.177.84"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_16 = ["Gude", "10.44.177.20"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_17 = ["Gude", "10.45.172.132"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_18 = ["Gude", "10.45.172.157"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_19 = ["ATEN", "10.42.61.173"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_20 = ["ATEN", "10.44.206.41"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_21 = ["ATEN", "10.44.206.145"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_22 = ["Gude", "10.44.177.97"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_23 = ["Gude", "10.44.177.236"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_24 = ["Gude", "10.44.177.136"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_25 = ["Gude", "10.44.177.93"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_26 = ["Gude", "10.45.172.148"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_27 = ["Gude", "10.45.172.156"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_28 = ["Gude", "10.44.177.189"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_29 = ["Gude", "10.44.177.26"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_30 = ["Gude", "10.44.177.234"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_31 = ["Gude", "10.44.177.228"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_32 = ["Gude", "10.44.177.98"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_33 = ["ATEN", "10.44.205.7"]                #[PDU type, PDU ip address, optional:PDU version]
PDU_34 = ["ATEN", "10.44.206.42"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_35 = ["ATEN", "10.44.206.122"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_36 = ["ATEN", "10.42.61.174"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_37 = ["Gude", "10.44.206.213"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_38 = ["ATEN", "10.44.206.146"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_39 = ["Gude", "10.45.172.134"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_40 = ["Gude", "10.45.172.156"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_41 = ["APC", "10.42.168.214"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_42 = ["Gude", "10.44.177.212"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_43 = ["ATEN", "10.42.168.250"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_44 = ["ATEN", "10.42.168.169"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_45 = ["Gude", "10.44.71.8", "8220-1"]       #[PDU type, PDU ip address, optional:PDU version]
PDU_46 = ["Gude", "10.44.71.9", "8220-1"]       #[PDU type, PDU ip address, optional:PDU version]
PDU_47 = ["Gude", "10.44.177.237"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_48 = ["Gude", "10.42.168.192", "8220-1"]    #[PDU type, PDU ip address, optional:PDU version]
PDU_49 = ["Gude", "10.42.168.55", "8220-1"]     #[PDU type, PDU ip address, optional:PDU version]
PDU_50 = ["ATEN", "10.42.168.20"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_51 = ["ATEN", "10.42.168.19"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_52 = ["ATEN", "10.44.71.5"]                 #[PDU type, PDU ip address, optional:PDU version]
PDU_53 = ["ATEN", "10.44.71.4"]                 #[PDU type, PDU ip address, optional:PDU version]
PDU_54 = ["Gude", "10.42.168.189", "8220-1"]    #[PDU type, PDU ip address, optional:PDU version]
PDU_55 = ["Gude", "10.45.172.158"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_56 = ["APC", "10.44.71.6"]                  #[PDU type, PDU ip address, optional:PDU version]
PDU_57 = ["Gude", "10.42.168.56", "8220-1"]     #[PDU type, PDU ip address, optional:PDU version]
PDU_58 = ["Gude", "10.42.168.72", "8220-1"]     #[PDU type, PDU ip address, optional:PDU version]
PDU_59 = ["APC", "10.44.71.7"]                  #[PDU type, PDU ip address, optional:PDU version]
PDU_60 = ["APC", "10.42.168.210"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_61 = ["APC", "10.42.168.211"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_62 = ["ATEN", "10.42.170.97"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_63 = ["APC", "10.42.168.172"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_64 = ["ATEN", "10.42.169.15"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_65 = ["APC", "10.42.168.216"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_66 = ["APC", "10.42.168.215"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_67 = ["ATEN", "10.42.51.211"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_68 = ["ATEN", "10.42.169.27"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_69 = ["APC", "10.42.168.171"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_70 = ["APC", "10.42.168.175"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_71 = ["ATEN", "10.42.169.26"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_72 = ["APC", "10.42.168.208"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_73 = ["APC", "10.42.168.207"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_74 = ["Gude", "10.44.205.163"]              #[PDU type, PDU ip address, optional:PDU version]
PDU_75 = ["APC", "10.42.168.212"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_76 = ["ATEN", "10.42.51.212"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_77 = ["APC", "10.42.168.213"]               #[PDU type, PDU ip address, optional:PDU version]
PDU_78 = ["Gude", "10.42.168.193", "8220-1"]    #[PDU type, PDU ip address, optional:PDU version]
PDU_79 = ["Gude", "10.44.71.11", "8220-1"]      #[PDU type, PDU ip address, optional:PDU version]


def pdu_qt(pdu_nr, pdu_model=None, pdu_version=None):
    pdu_nr_list = globals()[pdu_nr]
    cls = globals()[pdu_nr_list[0]]
    if pdu_nr_list[0] == "Gude":
        pdu_port_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        pdu_model = "EPC"
        try:
            pdu_version = pdu_nr_list[2]
        except IndexError:
            pdu_version = "8221-1"

    elif pdu_nr_list[0] == "ATEN" or pdu_nr_list[0] == "APC":
        pdu_port_numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    return cls(
        addr=pdu_nr_list[1],
        port_numbers=pdu_port_numbers,
        model=pdu_model,
        version=pdu_version,
    )
