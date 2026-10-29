__maintainer__ = "Yang, Le (NSB - CN/Hangzhou)"
__team__ = (
    "I_MN_SRAN_TRUNK_ENGINE_SG_HZ1_GMS <I_MN_SRAN_TRUNK_ENGINE_SG_HZ1@internal.nsn.com>"
)
__email__ = "le.yang@nokia-sbell.com"

import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RadioModule

from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.184.177", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
# _ru1_pdu = FACOM(addr='10.57.243.7', port_numbers=[2])
# _ru2_pdu = FACOM(addr='10.57.243.7', port_numbers=[1])
# _ru3_pdu = FACOM(addr='10.57.242.53', port_numbers=[5])

_ru0 = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[4],
    radio_type="AHCA",
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
    radio_type="AHCA",
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
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
    pdu_port=_5g_ru_pdu.pdu_ports[2],
    radio_type="AHCA",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.108.233.97",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.108.233.97", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.108.233.97", username="Nemuadmin", password="nemuuser"
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
    hardware_type="ASIK",
    hardware_version="A.101",
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru0, _ru1, _ru2], f1_m_ip_addr="10.108.233.97")

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
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
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
        addr="10.108.184.177", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10300,
    egate_port=20000,
    dir_path="/home/nokia/WTS_614186",
    cfg_filename=None,
)

#########UE##########
_qualcomm_pdu = FACOM(addr="10.68.183.77", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.108.184.177", username="root", password="nokia123"
    ),
    network_interface_address="10.108.184.177",
    iperf_path="/usr/bin/iperf",
)

_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.211.188", username="QT-tester", password="Nokia123!"
    ),
    serial_number="5c8e459f",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["REAL_ANDROID_UE"],
)

_qualcomm.ue_type = "qualcomm"

#########app server#########
_appserver_ssh = SshServiceDetails(
    addr="10.108.184.177", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    core=_epc_sim,
    ues=[_qualcomm],
    tl_cloud_topology="hgz-tl105",
    attenuator=_attenuator,
    appserver=_appserver,
)

# tl = TestlineWrapper(tl)

__all__ = ["tl"]
