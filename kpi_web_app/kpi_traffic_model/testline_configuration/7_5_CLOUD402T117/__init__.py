__maintainer__ = "Haifeng Gao"
__team__ = (
    "I_MN_SRAN_TRUNK_ENGINE_SG_HZ1_GMS <I_MN_SRAN_TRUNK_ENGINE_SG_HZ1@internal.nsn.com>"
)
__email__ = "haifeng.gao@nokia-sbell.com"


import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import DU
from taf.config.testline.radio import RU, RadioModule
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.ue import Android
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdu import FACOM, PduPort
from taf.config.testline.attenuator import AttenuationPort, HBTE

# from taf.compatibility.configuration import TestlineWrapper
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.106.164.76", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)

#########appserver##########
_appserver_ssh = SshServiceDetails(
    addr="10.106.164.76", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.164.76",
    iperf_path="iperf",
    port=59998,
)

_appserver = AppServer(_iperf_details_on_appserver)

#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.108.231.148",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.108.231.148", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.108.231.148", username="Nemuadmin", password="nemuuser"
    ),
)

#########DU##########
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_pdu = FACOM(addr="10.68.170.8", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu.pdu_ports[2],
    hardware_type="ASIB",
    hardware_version="A.102",
)

_airscale = Airscale(common_units=[_common_unit])

#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.68.170.22", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[1],
    radio_type="AEHC",
)
# attenuator
_attenuator = HBTE(
    ip_addr="10.106.211.141",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
#########DU##########
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.108.231.148",
    f1_c_ip_addr="10.108.231.148",
    f1_u_ip_addr="10.108.231.148",
)

#########ClassicalBts##########
_classicalbts = ClassicalBts(cu=_cu, dus=[_du])

#########4G RU##########
_4g_ru_pdu = FACOM(addr="10.68.170.8", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[3],
)

#########RealEnb##########
_real_enb_pdu = FACOM(addr="10.68.170.8", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.170.18", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
    hardware_type="ASIA",
    hardware_version="A.203",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])

#########EPCSim##########
_epc_sim = EPCSim(
    mme_ip=None,
    tac=None,
    mcc=None,
    mnc=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.40", username="root", password="nokia123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_614186/",
    cfg_filename="eNB_WMP_TL110.cfg",
)

#########UE##########
_qualcomm_pdu = FACOM(addr="10.57.246.238", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.164.76", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    network_interface_address="10.106.164.76",
    iperf_path="/usr/bin/iperf",
)

_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.170.23", username="qt-tester", password="Nokia123!"
    ),
    serial_number="2KE0220806002383",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["huawei"],
)

_huawei.ue_type = "huawei"

#########TestLine##########
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classicalbts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    appserver=_appserver,
    ues=[_huawei],
    attenuator=_attenuator,
    tl_cloud_topology="hgz-tl117",
)


# tl = TestlineWrapper(tl)

__all__ = ["tl"]
