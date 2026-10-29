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
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import TafUeIphone
from taf.config.testline.connection_details import (SshServiceDetails, OpenStackConnectionDetails, BmcConnectionDetails,
                                                    HttpConnectionDetails)

__maintainer__ = "Jack Zeng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jack.zeng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPC(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.126", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.162", username="vrf_sg3", password="vrf@sg3", port="53600"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.162",
    iperf_path="/usr/bin/iperf",
    port="53600",
)

_appserver = AppServer(_iperf_details_on_appserver)


_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.162",
    iperf_path="/cygdrive/c/iperf",
    port="53800",
)

_app_server_iphone = TafUeAppServer(app_server_name="APP_1",
                                    address="10.71.207.162",
                                    user="vrf_sg3",
                                    password="vrf@sg3",
                                    bind_interface_ip="10.71.207.162",
                                    expected_prompt="vrf_sg3@appserver")

_data_transfer_iperf_iphone = TafUeDataTransferProtocol(protocol_name='iperf',
                                                        app_server=_app_server_iphone,
                                                        server_close_delay=50,
                                                        # binary_path='some/path',
                                                        # interface_name='some_interface_name',
                                                        # bind_ue_ip='1.1.1.1',
                                                        version=3,
                                                        interval=1)

_data_transfer_ping_iphone = TafUeDataTransferProtocol(protocol_name='ping',
                                                       app_server=_app_server_iphone,
                                                       interval=1)

_data_transfer_ftp_iphone = TafUeDataTransferProtocol(protocol_name='ftp',
                                                      app_server=_app_server_iphone,
                                                      interval=1)

# _pdn1 = PDNAndroidDetails(entryName='wustatic',
#                           apnName='wustatic',
#                           apnType=['NONE'])
# CI_Detail_UE_Type='Qualcomm'
_android0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CR60WF62E",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.94",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR106J04V",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.92",
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CR40YXCJT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.95",
)

_android3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN2190D7E",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.103",
)

_android4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CR5085RCA",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.101",
)

_android5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CR50B3Q3B",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.96",
)

_android6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR316X2NM",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.93",
)

_android7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR10LXHTX",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.97",
)

_android8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CNC0B7D2Z",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.102",
)

_android9 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40JEH7P",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.100",
)

_android10 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CY62GDJCP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.118",
)

_android11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CXC3185SE",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.112",
)

_android12 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR103WRMT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.105",
)

_android13 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR20E705V",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.119",
)

_android14 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCXC10H1QN",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.113",
)


_android15 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCY1092KCV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.67.252",
)

_android16 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX60FWXPM",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.109",
)


_android17 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT610FE9M",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.117",
)


_android18 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW3299ALF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.110",
)


_android19 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW11NY79E",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.116",
)


_android20 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CY548JLQF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.115",
)

_android21 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW216G04F",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.126",
)

_android22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CRC2XD3RH",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.57",
)


_android23 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCRA03B2KT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.108",
)


_android24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CT32TS7TL",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.120",
)

_android25 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCXC137ZPW",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.111",
)

_android26 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40KQEAM",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.66.253",
)


_android27 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW218FJYR",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.48.126",
)

_android28 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40MH1CE",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.124",
)

_android29 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW20YTT9A",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.123",
)

_android30 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX10JPDWT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.75",
)

_android31 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40LH14Y",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.76",
)

_android32 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CY20PS4QZ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.77",
)

_android33 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW32AYL0W",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.78",
)

_android34 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW11NZKTV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.79",
)

_android35 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW314PJGP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.226",
)

_android36 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CW10X29EJ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.230",
)

_android37 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN1037CHB",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.48.137",
)

_android38 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW20HK02H",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.233",
)

_android39 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCXC13LVQP",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.218",
)

_android40 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40KNF6E",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.254",
)

_android41 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CW10X27PN",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.65.122",
)

_android42 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR10NE6VX",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.48.123",
)

_android43 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR403T99J",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.48.124",
)

_android44 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CT34DPQMF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.48.149",
)

_android45 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="4b60ef26",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.235",
)

_android46 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["mtk", "REAL_ANDROID_UE", "mtk"],
    mobile_network_text="172.249.48.168",
)

_android47 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.250.160.244",
)

_iphone48 = TafUeIphone(serial_number='G6TDKTCA0D80',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.250.160.250",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_12"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024036',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='356681111893993',
                        imsi='310260100024036',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_android49 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="7H99DQAYIJAULJKA",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="222.222.222.221",
)

_iphone49 = TafUeIphone(serial_number='MV6DNHXDH4',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.250.160.252",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024038',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='355033652070691',
                        imsi='310260100024038',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone50 = TafUeIphone(serial_number='NKQRYW9J4T',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.250.160.251",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_14"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024042',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='357684399048297',
                        imsi='310260100024042',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone51 = TafUeIphone(serial_number='J12J0Q023J',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.249.48.172",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_15"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024026',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='353850628248370',
                        imsi='310260100024026',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone52 = TafUeIphone(serial_number='LMWX67Q4NP',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.250.160.253",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_15"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024039',  # OPTIONAL (however MANDA.TORY for Voice Calls to work properly)
                        imei='356054498820130',
                        imsi='310260100024039',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone53 = TafUeIphone(serial_number='LR70NQH2F5',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.249.48.197",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_15"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024079',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='358684520341818',
                        imsi='310260100024079',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone54 = TafUeIphone(serial_number='L43C70D40D',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.249.48.195",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_15"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024077',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='356506178898348',
                        imsi='310260100024077',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone55 = TafUeIphone(serial_number='MTYXKKF72K',
                        ue_pc_address='10.57.130.78',
                        proxy_mngr_artifactory="172.249.48.196",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_15"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024078',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='351878590966127',
                        imsi='310260100024078',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_android56 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="WKPZ95EAK76THUEM",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.164",
)

_android57 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="ZY22LNG4W2",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.190",
)

_android58 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="3B159K00CBG00000",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.193",
)

_android59 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="AIMZWGFE797H4D7T",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.192",
)

_android60 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.134", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="AMCASCZXQ4AENRRK",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.189",
)

_android61 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="3B159K00CB300000",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.194",
)

_android62 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.166", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="5DGMZP6DSGJVORWS",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    mobile_network_text="172.249.48.198",
)

_iphone63 = TafUeIphone(serial_number='H41CVFWQWX',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.204",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_14"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026764',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='357684390059459',
                        imsi='310260100026764',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone64 = TafUeIphone(serial_number='QCWG7G14PQ',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.203",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_14"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026763',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='356150803667263',
                        imsi='310260100026763',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone65 = TafUeIphone(serial_number='FFXDQ3PN0DYF',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.242",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_14"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026673',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='359379492232959',
                        imsi='310260100026673',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone66 = TafUeIphone(serial_number='FTV2TP2KTY',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.226",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026685',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='358000860163821',
                        imsi='310260100026685',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone67 = TafUeIphone(serial_number='GY17CM46RP',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.215",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026680',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='358000860157492',
                        imsi='310260100026680',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone68 = TafUeIphone(serial_number='K6KL23CVNN',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.151",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026684',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='358000860323664',
                        imsi='310260100026684',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone69 = TafUeIphone(serial_number='J6W7Q9C3YR',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.219",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026682',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='358000860113123',
                        imsi='310260100026682',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone70 = TafUeIphone(serial_number='GT6H166KM7',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.230",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026689',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='357594327826229',
                        imsi='310260100026689',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone71 = TafUeIphone(serial_number='CRGVMD9F6T',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.250.160.251",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024037',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='357594327864501',
                        imsi='310260100024037',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone72 = TafUeIphone(serial_number='CT6L69C266',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.166",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024049',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='357594328341186',
                        imsi='310260100024049',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone73 = TafUeIphone(serial_number='J2QY2HL4G6',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.200",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026762',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='357594328437034',
                        imsi='310260100026762',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone74 = TafUeIphone(serial_number='LK3QJWP9GF',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.216",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026681',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='359456334527216',
                        imsi='310260100026681',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone75 = TafUeIphone(serial_number='M7KQ409QR1',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.163",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024046',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='351367437052507',
                        imsi='310260100024046',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone76 = TafUeIphone(serial_number='JWXD00VD41',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.167",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024050',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='352687369791148',
                        imsi='310260100024050',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone77 = TafUeIphone(serial_number='JK649Q7Q91',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.207",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_17"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026765',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='355145125662472',
                        imsi='310260100026765',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone78 = TafUeIphone(serial_number='FFXGT5P80DYL',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.191",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_12"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024092',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='352106837452217',
                        imsi='310260100024092',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone79 = TafUeIphone(serial_number='WN77TGWR09',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.250.160.243",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024073',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='352100130130851',
                        imsi='310260100024073',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone80 = TafUeIphone(serial_number='JWQV34V7GV',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.169",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024052',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='358021945773376',
                        imsi='310260100024052',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone81 = TafUeIphone(serial_number='MRQ6WCNF9L',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.171",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100024025',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='354922762092705',
                        imsi='310260100024025',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone82 = TafUeIphone(serial_number='YP4HXLK9FX',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.246",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026766',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='310260100026766',
                        imsi='355611225694111',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone83 = TafUeIphone(serial_number='YG914RL90G',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.243",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026675',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='351467539958104',
                        imsi='310260100026675',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_iphone84 = TafUeIphone(serial_number='DH76P4HQGM',
                        ue_pc_address='10.57.130.77',
                        proxy_mngr_artifactory="172.249.48.244",
                        capabilities=["REAL_UE", "IPHONE_UE", "IPHONE_13"],
                        data_transfer=[_data_transfer_iperf_iphone, _data_transfer_ping_iphone,
                                       _data_transfer_ftp_iphone],
                        phone_number='+8613100026677',  # OPTIONAL (however MANDATORY for Voice Calls to work properly)
                        imei='353504867054292',
                        imsi='310260100026677',
                        processes_to_kill=['Vysor'],
                        ue_pc_port='80')

_hbte_params = {
    "ip_addr": "10.57.230.67",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params_1 = {
    "ip_addr": "10.57.230.68",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_1 = HBTE(**_hbte_params_1)

_hbte_params_2 = {
    "ip_addr": "10.57.230.8",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                 24, 25, 26, 27, 28, 29, 30, 31, 32],
    "model": "PA-32-32-6-127-0.5-S",
    "version": None,
}
_attenuator_2 = HBTE(**_hbte_params_2)

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
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[9],
    #     _attenuator.attenuator_ports[10],
    #     _attenuator.attenuator_ports[11],
    #     _attenuator.attenuator_ports[12],
    # ],
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
        _attenuator_1.attenuator_ports[9],
        _attenuator_1.attenuator_ports[10],
        _attenuator_1.attenuator_ports[11],
        _attenuator_1.attenuator_ports[12],
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
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
    ],
)

_ru_pdu8 = FACOM(addr="10.57.176.160", port_numbers=[3])
_ru8 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu8.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
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
    pdu_port=_ru_pdu9.pdu_ports[8],
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[9],
    #     _attenuator.attenuator_ports[10],
    #     _attenuator.attenuator_ports[11],
    #     _attenuator.attenuator_ports[12],
    # ],
)

_ru_pdu10 = FACOM(addr="10.57.246.59", port_numbers=[8])
_ru10 = RU(
    ru_hw_group="AWHHJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu10.pdu_ports[8],
    attenuation_ports=[
        _attenuator_1.attenuator_ports[5],
        _attenuator_1.attenuator_ports[6],
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
)

_ru_pdu11 = FACOM(addr="10.57.246.59", port_numbers=[8])
_ru11 = RU(
    ru_hw_group="AWHHJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu11.pdu_ports[8],
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[15],
    #     _attenuator.attenuator_ports[16],
    # ],
)

_ru_pdu12 = FACOM(addr="10.57.176.156", port_numbers=[1])
_ru12 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu12.pdu_ports[1],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[1],
        _attenuator_2.attenuator_ports[2],
        _attenuator_2.attenuator_ports[3],
        _attenuator_2.attenuator_ports[4],
    ],
)

_ru_pdu13 = FACOM(addr="10.57.249.27", port_numbers=[5])
_ru13 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu13.pdu_ports[5],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[5],
        _attenuator_2.attenuator_ports[6],
        _attenuator_2.attenuator_ports[7],
        _attenuator_2.attenuator_ports[8],
    ],
)

_ru_pdu14 = FACOM(addr="10.57.176.156", port_numbers=[4])
_ru14 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu14.pdu_ports[4],
    # attenuation_ports=[
    #     _attenuator_2.attenuator_ports[5],
    #     _attenuator_2.attenuator_ports[6],
    #     _attenuator_2.attenuator_ports[7],
    #     _attenuator_2.attenuator_ports[8],
    # ],
)

_ru_pdu15 = FACOM(addr="10.57.249.27", port_numbers=[1])
_ru15 = RU(
    ru_hw_group="AVQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu15.pdu_ports[1],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[9],
        _attenuator_2.attenuator_ports[10],
        _attenuator_2.attenuator_ports[11],
        _attenuator_2.attenuator_ports[12],
    ],
)

_ru_pdu16 = FACOM(addr="10.57.249.27", port_numbers=[4])
_ru16 = RU(
    ru_hw_group="AVQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu16.pdu_ports[4],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[13],
        _attenuator_2.attenuator_ports[14],
        _attenuator_2.attenuator_ports[15],
        _attenuator_2.attenuator_ports[16],
    ],
)

_ru_pdu17 = FACOM(addr="10.57.176.156", port_numbers=[3])
_ru17 = RU(
    ru_hw_group="AVQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu17.pdu_ports[3],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[17],
        _attenuator_2.attenuator_ports[18],
        _attenuator_2.attenuator_ports[19],
        _attenuator_2.attenuator_ports[20],
    ],
)

_ru_pdu18 = FACOM(addr="10.57.176.156", port_numbers=[2])
_ru18 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu18.pdu_ports[2],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[21],
        _attenuator_2.attenuator_ports[22],
        _attenuator_2.attenuator_ports[23],
        _attenuator_2.attenuator_ports[24],
    ],
)

_ru_pdu19 = FACOM(addr="10.57.176.156", port_numbers=[6])
_ru19 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu19.pdu_ports[6],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[25],
        _attenuator_2.attenuator_ports[26],
        _attenuator_2.attenuator_ports[27],
        _attenuator_2.attenuator_ports[28],
    ],
)

_ru_pdu20 = FACOM(addr="10.57.176.152", port_numbers=[5])
_ru20 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu20.pdu_ports[5],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[29],
        _attenuator_2.attenuator_ports[30],
        _attenuator_2.attenuator_ports[31],
        _attenuator_2.attenuator_ports[32],
    ],
)


# classical gNB LMP
_lmp_connection = SshServiceDetails(
    addr="10.57.227.131", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection1 = SshServiceDetails(
    addr="10.57.227.134", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection2 = SshServiceDetails(
    addr="10.57.227.142", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal IP
_capacity_unit = CapacityUnit(addr="192.168.253.20")

# gNB PB
_gnb_pdu = FACOM(addr="10.57.246.59", port_numbers=[2])
_gnb_pdu1 = FACOM(addr="10.57.246.58", port_numbers=[3])
_gnb_pdu2 = FACOM(addr="10.57.176.154", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu1.pdu_ports[3],
)
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu2.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_airscale1 = Airscale(common_units=[_common_unit_1])
_airscale2 = Airscale(common_units=[_common_unit_2])
_du1 = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9],
    f1_m_ip_addr="10.57.227.131",
    f1_c_ip_addr="10.57.227.131",
    f1_u_ip_addr="10.57.227.131",
)

_du2 = DU(
    airscale=_airscale1,
    rus=[_ru10, _ru11],
    f1_m_ip_addr="10.57.227.134",
    f1_c_ip_addr="10.57.227.134",
    f1_u_ip_addr="10.57.227.134",
)

_du3 = DU(
    airscale=_airscale2,
    rus=[_ru12, _ru13, _ru14, _ru15, _ru16, _ru17, _ru18, _ru19, _ru20],
    f1_m_ip_addr="10.57.227.142",
    f1_c_ip_addr="10.57.227.142",
    f1_u_ip_addr="10.57.227.142",
)

# gNB MPlane IP
_cu1 = CU(
    backhaul_site_oam_ip="10.57.227.131",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.131", username="Nemuadmin", password="nemuuser"
    ),
)

_cu2 = CU(
    backhaul_site_oam_ip="10.57.227.134",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.134", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.134", username="Nemuadmin", password="nemuuser"
    ),
)

_cu3 = CU(
    backhaul_site_oam_ip="10.57.227.142",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.142", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.142", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# switch port to EIF1
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.157", port="1/17", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# instance_id=MRBTS_ID
_classical_bts1 = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=33511, global_bts_id=33511
)
_classical_bts2 = ClassicalBts(
    dus=[_du2], cu=_cu2, instance_id=33512, global_bts_id=33512
)
_classical_bts3 = ClassicalBts(
    dus=[_du3], cu=_cu3, instance_id=33513, global_bts_id=33513
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
    gnbs=[_classical_bts1, _classical_bts2, _classical_bts3],
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
        _android30,
        _android31,
        _android32,
        _android33,
        _android34,
        _android35,
        _android36,
        _android37,
        _android38,
        _android39,
        _android40,
        _android41,
        _android42,
        _android43,
        _android44,
        _android45,
        _android46,
        _android47,
        _iphone48,
        # _android49,
        _iphone49,
        _iphone50,
        _iphone51,
        _iphone52,
        _iphone53,
        _iphone54,
        _iphone55,
        _android56,
        _android57,
        _android58,
        _android59,
        _android60,
        _android61,
        _android62,
        _iphone63,
        _iphone64,
        _iphone65,
        _iphone66,
        _iphone67,
        _iphone68,
        _iphone69,
        _iphone70,
        _iphone71,
        _iphone72,
        _iphone73,
        _iphone74,
        _iphone75,
        _iphone76,
        _iphone77,
        _iphone78,
        _iphone79,
        _iphone80,
        _iphone81,
        _iphone82,
        _iphone83,
        _iphone84,
    ],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch],
    attenuator=[_attenuator, _attenuator_1, _attenuator_2],
    nms=_netact,
)
