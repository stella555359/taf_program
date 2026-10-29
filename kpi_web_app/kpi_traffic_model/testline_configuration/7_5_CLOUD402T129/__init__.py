__maintainer__ = "lisa yang"
__team__ = (
    "I_MN_SRAN_TRUNK_ENGINE_SG_HZ1_GMS <I_MN_SRAN_TRUNK_ENGINE_SG_HZ1@internal.nsn.com>"
)
__email__ = "lisa.yang@nokia-sbell.com"


import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM
from taf.config.testline.attenuator import HBTE
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Android
from taf.config.testline.enb import RealEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU
from taf.config.testline.appserver import AppServer

# from taf.compatibility.configuration import TestlineWrapper
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.183.60", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)

#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.108.233.102",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.108.233.102", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.108.233.102", username="Nemuadmin", password="nemuuser"
    ),
)

#########DU##########
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_pdu = FACOM(addr="10.57.241.143", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu.pdu_ports[2],
    hardware_type="ASIK",
    hardware_version="A.101",
)

_airscale = Airscale(common_units=[_common_unit])

# attenuator
_attenuator = HBTE(
    ip_addr="10.106.211.185",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.106.211.218", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru0 = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[2],
    radio_type="AHPB",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[5],
    ],
)

_ru1 = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.85", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[3],
    radio_type="AHPB",
    attenuation_ports=[
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[6],
    ],
)

_ru2 = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[4],
    radio_type="AHPB",
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[7],
    ],
)

#########DU##########
_du = DU(
    airscale=_airscale,
    rus=[_ru0, _ru1, _ru2],
    f1_m_ip_addr="10.108.233.102",
    f1_c_ip_addr="10.108.233.102",
    f1_u_ip_addr="10.108.233.102",
)

#########ClassicalBts##########
_classicalbts = ClassicalBts(cu=_cu, dus=[_du])

#########EPCSim##########
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.149.10", username="hztester", password="Nokia_1234"
    ),
    mcc=None,
    mnc=None,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# ########enb##########
# _real_enb_pdu = FACOM(addr='10.57.241.151', port_numbers=[2], model='111', version='1.1.1')
#
# _common_unit_2 = CommonUnit(
#     lmp_connection=SshServiceDetails(addr='10.57.236.9', username='toor4nsn', password='oZPS0POrRieRtu'),
#     capacity_units=[],
#     pdu_port=_real_enb_pdu.pdu_ports[2])
#
# _real_enb = Airscale(common_units=[_common_unit_2])
#
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=235)


#########UE##########
_appserver_ssh = SshServiceDetails(
    addr="10.108.183.60", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.183.60",
    iperf_path="iperf",
    port=59995,
    ports=[59995],
)

_appserver = AppServer(_iperf_details_on_appserver)

_ue_host_ssh = SshServiceDetails(
    addr="10.106.211.200", username="QT-tester", password="Nokia123!"
)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="wap1.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="wap2.nokia.com"),
]
_core = RealCore(pdns=_pdns)
_core.default_ssh_connection_details = SshServiceDetails(
    addr="",
    username="",
    password="",
)

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.108.183.60", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    network_interface_address="10.108.183.60",
    iperf_path="/usr/bin/iperf",
    port=59995,
)

_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.211.200", username="qt-tester", password="Nokia123!"
    ),
    serial_number="9YS0220721001042",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["huawei"],
    imsi="huawei",
)

_huawei.ue_type = "huawei"

#########TestLine##########
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classicalbts],
    # enbs=[_lte_real_enb],
    # core=_epc_sim,
    core=_core,
    ues=[_huawei],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology="hgz-tl129",
)


# tl = TestlineWrapper(tl)

__all__ = ["tl"]
