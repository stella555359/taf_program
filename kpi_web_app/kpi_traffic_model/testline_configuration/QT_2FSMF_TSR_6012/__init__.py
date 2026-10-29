__maintainer__ = "QT"
__email__ = "I_AM_QT@internal.nsn.com"
__owner_email__ = "I_AM_QT@internal.nsn.com"

from ute_testline_configuration.ute_config import UTE_CONFIG, Host, Pdu, FSMr3, RF

PDU_IP = "10.255.1.52"
PDU_IP2 = "10.255.1.53"
PDU_TYPE = "EPC"

host = [Host(addr="10.5.29.9"), Host(addr="10.5.29.10")]

fsm = [FSMr3(pdu=Pdu(PDU_IP, 9, PDU_TYPE)), FSMr3(pdu=Pdu(PDU_IP, 8, PDU_TYPE))]

rf = [RF(pdu=Pdu(PDU_IP2, 12, PDU_TYPE)), RF(pdu=Pdu(PDU_IP2, 9, PDU_TYPE))]

UEs = []

tl = UTE_CONFIG(host=host, fsm=fsm, rf=rf, ue=UEs)

__all__ = ["tl"]

tl.custom = {
    'BTS_Id': '1',
    'BBMODs': 'FBBC',
    'RATs': ['GSM', 'WCDMA', 'LTE']
}
