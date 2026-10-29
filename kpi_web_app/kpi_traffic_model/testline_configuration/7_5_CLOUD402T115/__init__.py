__maintainer__ = "Zheng Min"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "min.zheng@nokia-sbell.com"


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
from taf.config.testline.enb import RealEnb, Enb
from taf.config.testline.core import EPCSim, RealCore, AMF, MME
from taf.config.testline.ue import Airphone, Prisma, TM500, Android
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdu import FACOM, PduPort
from taf.config.testline.attenuator import AttenuationPort, HBTE

# from taf.compatibility.configuration import TestlineWrapper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.106.164.47", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)


#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.108.233.123",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.108.233.123", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.108.233.123", username="Nemuadmin", password="nemuuser"
    ),
)

#########DU##########

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)


_common_unit_pdu = FACOM(addr="10.106.211.208", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu.pdu_ports[6],
    hardware_type="ASIB",
    hardware_version="A.102",
)


_airscale = Airscale(common_units=[_common_unit])

# attenuator
_attenuator = HBTE(
    ip_addr="10.106.211.191",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.106.211.214", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru0 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=None,
    ru_hw_group="",
    radio_type="AHFIB",
)

_ru1 = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[2],
    radio_type="AHOLA",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[13],
    ],
)

#########DU##########
_du = DU(
    airscale=_airscale,
    rus=[_ru0, _ru1],
    f1_m_ip_addr="10.108.233.123",
    f1_c_ip_addr="10.108.233.123",
    f1_u_ip_addr="10.108.233.123",
)

#########ClassicalBts##########
_classicalbts = ClassicalBts(cu=_cu, dus=[_du])

#########4G RU##########
_4g_ru_pdu = FACOM(addr="10.106.211.214", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[4],
)

#########RealEnb##########
_real_enb_pdu = FACOM(addr="10.106.211.214", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.211.212", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
    hardware_type="ASIA",
    hardware_version="A.202",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])
#########EPCSim##########
_epc_sim = EPCSim(
    mme_ip=None,
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.106.164.47", username="root", password="nokia123"
    ),
    mcc=None,
    mnc=None,
    dir_path=None,
    cfg_filename=None,
)
#########UE##########
_appserver_ssh = SshServiceDetails(
    addr="10.106.164.47", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.164.47",
    iperf_path="iperf",
    port=5024,
)

_appserver = AppServer(_iperf_details_on_appserver)

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.164.47", username="root", password="nokia123"
    ),
    network_interface_address="10.106.164.47",
    iperf_path="/usr/bin/iperf",
)

_askey = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.211.213", username="qt-tester", password="Nokia123!"
    ),
    serial_number="8a25ad9c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["askey"],
)

_askey.ue_type = "askey"

#########TestLine##########
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classicalbts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_askey],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology="hgz-tl115",
)

# tl = TestlineWrapper(tl)

__all__ = ["tl"]
