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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
from taf.config.testline.attenuator import HBTE as PA_HBTE
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
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Chen Jun"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jun.8.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))



# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.240", username="vrf4_sg6", password="Nokia@1234567", port="56182",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.240",
    iperf_path="/cygdrive/c",
    port="56082"
)

_appserver = AppServer(_iperf)


# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.203", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="bde0d57c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE0", "qct_dx50"],
    imsi="262033100007808",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)


# #5GRU for classicalBTS
# attenuator
_attenuator = PA_HBTE(
    ip_addr="10.71.212.104",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 16],
    model="PA-16-16-6-127-0.5-B-S",
)


# #5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.71.196.70", port_numbers=[2])
_ru2_pdu = HBTE(addr="10.71.196.72", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQC,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    serial_number="1M222643818",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHHI,
    serial_number="EB2321R0181",
)

# RealEnb
_real_enb_pdu = HBTE(addr="10.71.196.71", port_numbers=[2])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.212.35", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
    hardware_type="ASIA",
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIL",
)

_gnb_pdu = HBTE(addr="10.71.196.71", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.71.212.34")

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
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.212.34",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.212.33", ip_prefix_length=29),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.34", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.212.34",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.212.33", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.71.212.34",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.212.33", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="10.71.212.34",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.212.33", ip_prefix_length=29),
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=36929, global_bts_id=36929)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.30", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_ASIKL_ABILB1_AEQC_ENB"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    ues=[_android],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
)
