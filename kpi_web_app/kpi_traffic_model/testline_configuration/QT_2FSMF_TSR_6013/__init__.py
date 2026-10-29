__maintainer__ = "QT"
__email__ = "I_AM_QT@internal.nsn.com"
__owner_email__ = "I_AM_QT@internal.nsn.com"

from ute_testline_configuration.ute_config import UTE_CONFIG, Host, Pdu, FSMr3, RF

PDU_IP = "10.255.1.55"
PDU_IP2 = "10.255.1.54"
PDU_TYPE = "EPC"

host = [Host(addr="10.5.53.71"), Host(addr="10.5.53.72")]

fsm = [FSMr3(pdu=Pdu(PDU_IP, 1, PDU_TYPE)), FSMr3(pdu=Pdu(PDU_IP, 2, PDU_TYPE))]

rf = [RF(pdu=Pdu(PDU_IP2, 9, PDU_TYPE)), RF(pdu=Pdu(PDU_IP2, 10, PDU_TYPE))]

UEs = []

tl = UTE_CONFIG(host=host, fsm=fsm, rf=rf, ue=UEs)

__all__ = ["tl"]

tl.custom = {
    'BTS_Id': '1',
    'BBMODs': 'FBBC',
    'RATs': ['GSM', 'WCDMA', 'LTE']
}