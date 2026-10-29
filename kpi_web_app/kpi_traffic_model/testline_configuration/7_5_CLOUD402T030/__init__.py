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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress
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
from taf.config.testline.appserver import AppServer

__maintainer__ = "shi Ming"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "ming.shi@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.27", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_epc_sim = EPCSim(
    mme_ip="192.168.129.211",
    mcc="450",
    mnc="05",
    tac="4442",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.27", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_7577/",
    cfg_filename="1927_Samsung_MDRB.cfg",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.167.27", username="ute", password="iW_K#8.ute%A10h0m0ra"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.167.27",
    iperf_path="/cygdrive/c/iperf",
    port="5501",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.167.27",
    iperf_path="iperf",
    port="5502",
)
_appserver = AppServer(_iperf_details_on_appserver2)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.165", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CM40CMAGT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.44", username="tester", password="tester123"
    ),
    serial_number="R3CM70ALPHF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

_real_enb_pdu = FACOM(
    addr="10.57.242.8", port_numbers=[3], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.113", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=30)

_attenuator = TopYoung(
    ip_addr="10.57.234.92",
    port=3000,
    attenuation_port_numbers=[1, 2, 11, 12, 9, 10],
    model="TAS16T16-51-120-1SDES",
)

_ru1_pdu = FACOM(addr="10.57.249.32", port_numbers=[2])
_ru2_pdu = FACOM(addr="10.57.242.53", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQD,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.57.236.184", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit1 = CapacityUnit(addr="192.168.253.24")

_gnb_pdu = FACOM(addr="10.57.241.161", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit1],
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.236.184",
    f1_c_ip_addr="10.57.236.184",
    f1_u_ip_addr="10.57.236.184",
)


_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.57.236.184",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.236.184", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.236.184", username="Nemuadmin", password="nemuuser"
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
    backhaul_site_oam_ip="10.57.223.98",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.98", username="Nemuadmin", password="nemuuser"
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

_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=30)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_android_0, _android_1],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
