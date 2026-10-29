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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
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
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni

__maintainer__ = "Fu Junjie"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "junjie.1.fu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.131", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="cmw_sg3", password="cmw_sg3"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="192.168.10.70",
    iperf_path="/cygdrive/c/Tools/iperf",
)
# #Cobham
_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.159", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    pdu_port=None,
    tma_path="/cygdrive/c/Cobham/NLA_4_26_0/TM500_NR_5G_EXT-MUE_Release_NLA_4_26_0/Test Mobile Application/TmaApplication.exe",
    iperf_details=_iperf,
)


# #RealEnb
_real_enb_pdu = FACOM(addr="10.1.1.1", port_numbers=[3], model="111", version="1.1.1")

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.236.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=229)


# #5GRU for classicalBTS
# attenuator
_attenuator = TopYoung(
    ip_addr="9.8.8.8",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6],
    model="TAS16T16-51-120-1SDES",
)

# 5G RU


# need modify FA IP if need to use
_ru1_pdu = FACOM(addr="10.1.1.1", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.1.1.1", port_numbers=[4])
_ru3_pdu = FACOM(addr="10.1.1.1", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(
        addr="8.8.8.8", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(
        addr="8.8.8.8", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(
        addr="8.8.8.8", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.228.7", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.241.150", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.228.7",
    f1_c_ip_addr="10.57.228.7",
    f1_u_ip_addr="10.57.228.7",
)

_lmp_connection1 = SshServiceDetails(
    addr="10.57.228.9", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu1 = FACOM(addr="10.57.241.150", port_numbers=[2])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu1.pdu_ports[2],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru3],
    f1_m_ip_addr="10.57.228.9",
    f1_c_ip_addr="10.57.228.9",
    f1_u_ip_addr="10.57.228.9",
)
# #CU

_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.57.228.7",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.7", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.228.9",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.9", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.9", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

# classicalbts
_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=229)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=229)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    enbs=[_lte_real_enb],
    ues=[_tm500],
    tl_cloud_topology=_tl_cloud_topology,
)

# old version keyword under robotws5g/resource compatibility workaround
tl = TestlineWrapper(tl)
