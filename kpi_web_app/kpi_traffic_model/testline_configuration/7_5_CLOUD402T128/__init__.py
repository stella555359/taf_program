__maintainer__ = "Yang, Le (NSB - CN/Hangzhou)"
__team__ = (
    "I_MN_SRAN_TRUNK_ENGINE_SG_HZ1_GMS <I_MN_SRAN_TRUNK_ENGINE_SG_HZ1@internal.nsn.com>"
)
__email__ = "ke.3.li@nokia-sbell.com"

import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, APC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.enb import (
    Enb,
    RealEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RadioModule
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.core import EPCSim

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.184.177", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)

# #5GRU for classicalBTS

# attenuator
_attenuator = HBTE(
    ip_addr="10.106.211.141",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.106.211.182", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru1_pdu = FACOM(addr="10.106.211.207", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
# _ru2_pdu = FACOM(addr='10.57.243.7', port_numbers=[1])
# _ru3_pdu = FACOM(addr='10.57.242.53', port_numbers=[5])

_ru0 = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    radio_type="AHFIB",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
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
    pdu_port=_5g_ru_pdu.pdu_ports[1],
    radio_type="AHLOA",
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.106.211.227",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.211.227", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.211.227", username="Nemuadmin", password="nemuuser"
    ),
)

#########DU##########
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_pdu = FACOM(addr="10.106.211.182", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu.pdu_ports[8],
    hardware_type="ASIB",
    hardware_version="A.102",
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru0, _ru1], f1_m_ip_addr="10.106.211.227")

#########ClassicalBts##########
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

#########4G RU##########
_4g_ru_pdu = FACOM(addr="10.106.211.182", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[5],
)

#########RealEnb##########
_real_enb_pdu = FACOM(addr="10.106.211.182", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.211.186", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
    hardware_type="ASIA",
    hardware_version="A.203",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])

#########EPCSim##########

#########UE##########
_qualcomm_pdu = FACOM(addr="10.68.183.77", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.108.184.177", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    network_interface_address="10.108.184.177",
    iperf_path="/usr/bin/iperf",
)

_askey = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.211.188", username="QT-tester", password="Nokia123!"
    ),
    serial_number="c24bb1b9",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["askey"],
)

_askey.ue_type = "askey"

#########app server#########
_appserver_ssh = SshServiceDetails(
    addr="10.108.184.177", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.184.177",
    iperf_path="iperf",
    port=5023,
)

_appserver = AppServer(_iperf_details_on_appserver)

#########TestLine##########
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    # core=_epc_sim,
    ues=[_askey],
    tl_cloud_topology="hgz-tl128",
    attenuator=_attenuator,
    appserver=_appserver,
)

# tl = TestlineWrapper(tl)

__all__ = ["tl"]
