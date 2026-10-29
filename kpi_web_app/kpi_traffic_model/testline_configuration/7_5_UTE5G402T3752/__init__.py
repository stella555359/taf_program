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
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
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
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import (
    NetworkAddress,
    RoutingInformation,
)  # add in taf.meta 5.4
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

__maintainer__ = "ming shi"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "ming.shi@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPC(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.145", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.12", username="cmw_sg3", password="cm@3", port="53700"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.12",
    iperf_path="/usr/bin/iperf",
    port="53700",
)

_appserver = AppServer(_iperf_details_on_appserver)


_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.12",
    iperf_path="/cygdrive/c/iperf",
    port="53730",
)

# CI_Detail_UE_Type='Qualcomm'
_android0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CNC08A9NX",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX4101WBY",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN1037CHB",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN202F60K",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN207PH4Z",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN208KEDY",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN20MWE9K",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN20Q9JSN",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCWC0XKVBP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android9 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN211JNJN",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android10 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN212Z7SE",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN2190D7E",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android12 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN30RGP5M",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S20"],
)

_android13 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CR411TB3K",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android14 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CR60N219V",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)
_android15 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX10VQ9SX",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android16 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR111ZVJP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android17 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX219DXPA",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android18 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT31L51ED",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android19 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.144", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT51636LN",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)
_android20 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX11CE8XP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android21 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW11REXEF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW2021WJD",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android23 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW20HPAXW",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW20YTESR",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)
_android25 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW318YK0Y",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android26 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW329A7DR",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android27 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW32AYKJJ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android28 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW32AZ8FP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)

_android29 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.175", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX114Q4VF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21"],
)


_hbte_params = {
    "ip_addr": "10.57.249.98",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params_1 = {
    "ip_addr": "10.57.249.100",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_1 = HBTE(**_hbte_params_1)

# 5GRU for classicalBTS
_ru_pdu1 = FACOM(addr="10.57.246.204", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.255", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu1.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu2 = FACOM(addr="10.57.246.204", port_numbers=[7])

_ru2 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.131", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu2.pdu_ports[7],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu3 = FACOM(addr="10.57.246.54", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu3.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu4 = FACOM(addr="10.57.246.54", port_numbers=[4])
_ru4 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu4.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu5 = FACOM(addr="10.57.246.55", port_numbers=[1])
_ru5 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu5.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu6 = FACOM(addr="10.57.246.204", port_numbers=[5])
_ru6 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu6.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu7 = FACOM(addr="10.57.246.58", port_numbers=[6])
_ru7 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu7.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu8 = FACOM(addr="10.57.246.59", port_numbers=[8])
_ru8 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu8.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu9 = FACOM(addr="10.57.246.59", port_numbers=[8])
_ru9 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu8.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu10 = FACOM(addr="10.57.246.59", port_numbers=[8])
_ru10 = RU(
    ru_hw_group="AHFB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu8.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

_ru_pdu11 = FACOM(addr="10.57.246.59", port_numbers=[8])
_ru11 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu8.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

# classical gNB LMP
_lmp_connection = SshServiceDetails(
    addr="10.57.131.117", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal IP
_capacity_unit = CapacityUnit(addr="192.168.253.20")

# gNB PB
_gnb_pdu = FACOM(addr="10.57.246.197", port_numbers=[2])
_gnb_pdu1 = FACOM(addr="10.57.246.197", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du1 = DU(
    airscale=_airscale,
    rus=[_ru10, _ru11],
    f1_m_ip_addr="10.57.131.117",
    f1_c_ip_addr="10.57.131.117",
    f1_u_ip_addr="10.57.131.117",
)

# gNB MPlane IP
_cu1 = CU(
    backhaul_site_oam_ip="10.57.131.117",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.117", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.117", username="Nemuadmin", password="nemuuser"
    ),
)


# RealEnb1
_lmp_connection_enb1 = SshServiceDetails(
    addr="10.57.248.157", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.246.197", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb1,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb1 = Airscale(common_units=[_common_unit_1])
_lte_real_enb1 = RealEnb(
    airscale=_real_enb1, rms=None, instance_id=37521, global_bts_id=37521
)


# RealEnb2
_lmp_connection_enb2 = SshServiceDetails(
    addr="10.57.248.156", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.246.197", port_numbers=[1])
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_enb2,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb2 = Airscale(common_units=[_common_unit_2])
_lte_real_enb2 = RealEnb(
    airscale=_real_enb2, rms=None, instance_id=37522, global_bts_id=37522
)
# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

## switch port to EIF1
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.161", port="1/37", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# instance_id=MRBTS_ID
_classical_bts1 = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=37512, global_bts_id=37512
)

# realcore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.107.180.5", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)


_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=310, mnc=260)

# Netact IP
_netact = Netact("10.106.161.25")

tl = TestLine(
    test_pc=_host,
    core=_core,
    gnbs=[_classical_bts1],
    enbs=[_lte_real_enb1, _lte_real_enb2],
    ues=[
        _android0,
        _android1,
        _android2,
        _android3,
        _android4,
        _android5,
        _android6,
        _android7,
        _android8,
        _android9,
        _android10,
        _android11,
        _android12,
        _android13,
        _android14,
        _android15,
        _android16,
        _android17,
        _android18,
        _android19,
        _android20,
        _android21,
        _android22,
        _android23,
        _android24,
        _android25,
        _android26,
        _android27,
        _android28,
        _android29,
    ],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch],
    attenuator=[_attenuator, _attenuator_1],
    nms=_netact,
)
