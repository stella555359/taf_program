import os
import yaml
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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE
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
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "Zhang Xuewen"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ4_05_GMS <I_NSB_MN_RAN_RD_VRF_HAZ4_05@internal.nsn.com>"
)
__email__ = "xuewen.zhang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

ue_config_path = os.path.join(_cfg_dir, "inseego.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(f)
else:
    ue_config = ""

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.62", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247",
    username="vrf4_sg5",
    password="vrf4@sg5",
    port="55257",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/cygdrive/c/iperf",
    port="55257",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="iperf",
    port="55257",
)
_appserver = AppServer(_iperf_details_on_appserver2)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.131", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CNC0DF2SN",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "REAL_ANDROID_UE"],
    imsi="310260001006099",
)


# #RealEnb
_real_enb_pdu0 = FPFH(addr="10.57.176.194", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.244", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu0.pdu_ports[3],
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=358)

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="310", mnc="260", pdns=None)

# #attenuator
_hbte_params = {
    "ip_addr": "10.57.230.20",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_ru1_pdu = FPFH(addr="10.57.176.194", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AENB,
)


_lmp_connection = SshServiceDetails(
    addr="10.57.233.244", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")

_gnb_pdu1 = FPFH(addr="10.57.176.204", port_numbers=[5])

_gnb_pdu2 = FPFH(addr="10.57.176.204", port_numbers=[3])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_pdu1.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.57.233.244",
    f1_c_ip_addr="10.57.233.244",
    f1_u_ip_addr="10.57.233.244",
)

_lmp_connection1 = SshServiceDetails(
    addr="10.57.233.243", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="10.57.233.243")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu2.pdu_ports[3],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru1],
    f1_m_ip_addr="10.57.233.243",
    f1_c_ip_addr="10.57.233.243",
    f1_u_ip_addr="10.57.233.243",
)

# _f1m = NetworkAddress(v6="2a00:8a00:8000:136:10:57:229:40")

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.233.244",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.233.244", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.233.244", username="Nemuadmin", password="nemuuser"
    ),
    #    f1m=_f1m,
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.233.243",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.233.243", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.233.243", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=2157)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=2158)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    core=_realcore,
    enbs=[_lte_real_enb0],
    ues=[_android],
    appserver=_appserver,
    attenuator=[],
    tl_cloud_topology=_tl_cloud_topology,
)
