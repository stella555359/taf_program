__maintainer__ = "Le Yang"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "le.yang@nokia-sbell.com"


import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import DU
from taf.config.testline.radio import RU, RadioModule
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.ue import TM500
from taf.config.testline.pdu import FACOM, PduPort

# from taf.compatibility.configuration import TestlineWrapper
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.56", username="root", password="nokia123"
    )
)

#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.57.227.131",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.131", username="Nemuadmin", password="nemuuser"
    ),
)

#########DU##########
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_pdu = FACOM(addr="10.57.241.143", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[],
    pdu_port=_common_unit_pdu.pdu_ports[3],
    hardware_type="ASIK",
    hardware_version="A.101",
)

_airscale = Airscale(common_units=[_common_unit])

#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.57.246.238", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="mmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[1],
    radio_type="AEUA",
)

#########DU##########
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.57.227.131",
    f1_c_ip_addr="10.57.227.131",
    f1_u_ip_addr="10.57.227.131",
)

#########ClassicalBts##########
_classicalbts = ClassicalBts(cu=_cu, dus=[_du])

#########4G RU##########
_4g_ru_pdu = FACOM(addr="10.57.246.235", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[2],
)

#########RealEnb##########
_real_enb_pdu = FACOM(addr="10.57.241.143", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.235.135", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
    hardware_type="ASIA",
    hardware_version="A.103",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])

#########EPCSim##########
_epc_sim = EPCSim(
    mme_ip=None,
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.56", username="nokia", password="nokia"
    ),
    mcc=None,
    mnc=None,
    dir_path=None,
    cfg_filename=None,
)

#########UE##########
_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.246.248", username="tester", password="nokia123"
    ),
    tma_command_port=5003,
    tma_path=(
        r"C:\\Program Files (x86)\\Aeroflex\\TM500\\5G NR - NLA 4.14.0"
        r"\\Test Mobile Application\\TmaApplication.exe"
    ),
)

#########TestLine##########
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classicalbts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_cobham],
    tl_cloud_topology="hgz-tl111",
)

# tl = TestlineWrapper(tl)

__all__ = ["tl"]
