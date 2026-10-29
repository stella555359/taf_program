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
from taf.config.testline.testpc import TestPc, Connection
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
from taf.config.testline.pdu import FPFH
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline import RealEnb
from taf.config.testline.pdu import Gude
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
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
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
from taf.config.testline.optical_switch import Leoni, Calient
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes


__maintainer__ = "Hao Xiaoxia"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xiaoxia.haonokia-sbell.com"


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.240", username="vrf4_sg6", password="Nokia@1234567", port="56815"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.240",
    iperf_path="/opt/app/iperf",
    port="56915",
)
_ue_pdu = pdu_TopYoung(addr="1.1.1.1", port_numbers=[1])

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.144", username="mn5gran", password="nokia123@"
    ),
    serial_number="c6566410",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
    pdu_port=_ue_pdu.pdu_ports[1],
)

# attenuator
_attenuator_0 = HBTE(
    ip_addr="10.101.53.53",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# #5GRU for classicalBTS
_gnb_pdu = pdu_HBTE(addr="10.68.87.71", port_numbers=[4])
_ru1_pdu = pdu_TopYoung(addr="10.68.87.75", port_numbers=[4])
_ru2_pdu = pdu_HBTE(addr="10.68.87.88", port_numbers=[2])
_ru3_pdu = pdu_HBTE(addr="10.68.87.178", port_numbers=[3])
_ru4_pdu = FPFH(addr="10.68.87.68", port_numbers=[3])
_real_enb_pdu = pdu_TopYoung(addr="10.101.46.14", port_numbers=[4])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[14],
        _attenuator_0.attenuator_ports[15],
        _attenuator_0.attenuator_ports[16],
    ],
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFIB,
)


# #DU for classicalBTS
_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# _lmp_connection_2 = SshServiceDetails(
#    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
# )

_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.77", username="toor4nsn", password="oZPS0POrRieRtu"
)

# _capacity_unit = CapacityUnit(addr="10.68.88.182")

_gnb_airscale_cu_capacity_unit_1 = CapacityUnit(
    addr="10.68.88.182",
    hardware_type="ABIP",
)
_gnb_airscale_cu_capacity_unit_2 = CapacityUnit(
    addr="10.68.88.182",
    hardware_type="ABIP",
)
_gnb_airscale_cu_capacity_unit_3 = CapacityUnit(
    addr="10.68.88.182",
    hardware_type="ABIO",
)
_enb_airscale_cu_capacity = CapacityUnit(
    addr="10.71.213.77",
    hardware_type="ABIA",
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_gnb_airscale_cu_capacity_unit_1, _gnb_airscale_cu_capacity_unit_2, _gnb_airscale_cu_capacity_unit_3],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASIM",
)

# _common_unit_2 = CommonUnit(
#    lmp_connection=_lmp_connection_2,
#    capacity_units=[_gnb_airscale_cu_capacity_unit_right],
#    hardware_type="ASIB",
#    pdu_port=_gnb_pdu_right.pdu_ports[6],
# )

# #RealEnb

_common_unit_enb = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[_enb_airscale_cu_capacity],
    pdu_port=_real_enb_pdu.pdu_ports[4],
    hardware_type="ASIA",
)

_airscale_1 = Airscale(common_units=[_common_unit_1])
# _airscale_2 = Airscale(common_units=[_common_unit_2])
_airscale_enb = Airscale(common_units=[_common_unit_enb])
_lte_real_enb = RealEnb(
    airscale=_airscale_enb, rms=None, oam_ip=NetworkAddress("10.101.52.17")
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="192.168.255.129",
)

# _du_2 = DU(airscale=_airscale_2, rus=[_ru3, _ru4])

# _du_enb = DU(
# airscale=_airscale_enb, rus=[_ru1, _ru2], f1_m_ip_addr="192.168.255.129"
# )

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
    backhaul_site_oam_ip="10.68.88.182",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.182", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.182", username="Nemuadmin", password="nemuuser"
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

_cu_enb = CU(
    backhaul_site_oam_ip="10.101.52.17",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.17", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.17", username="Nemuadmin", password="nemuuser"
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


_fct = CommonUnit(
    SshServiceDetails(
        addr="10.71.213.77", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_enb_airscale_cu_capacity],
    pdu_port=_real_enb_pdu.pdu_ports[4],
    hardware_type="ASIA",
    # hardware_version="A.203",
    # serial_number="L1172804242",
)

_smod_enb = Airscale(common_units=[_fct])


# classicalbts
_classical_bts_1 = ClassicalBts(dus=[_du_1], cu=_cu, instance_id=10857, global_bts_id=10857)
# _classical_bts_2 = ClassicalBts(
#    dus=[_du_2], cu=_cu, instance_id=811, global_bts_id=811, master=_classical_bts_1
# )
# _classical_bts_1.slave = _classical_bts_2
_classical_bts_enb = RealEnb(airscale=_smod_enb, instance_id=814)

# #host
_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.87", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts_1.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIM_ABIOB1_ABIPB2B3_3xAEHC"

tl = TestLine(
    test_pc=_test_pc_1,
    #    test_pcs=[_test_pc_1, _test_pc_2, _test_pc_enb],
    #    gnbs=[_classical_bts_1, _classical_bts_2],
    test_pcs=[_test_pc_1],
    gnbs=[_classical_bts_1],
    tl_cloud_topology=_tl_cloud_topology,
#    enbs=[_classical_bts_enb],
    ues=[_android],
    attenuators=[_attenuator_0],
)

# common
__all__ = ["tl"]

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
