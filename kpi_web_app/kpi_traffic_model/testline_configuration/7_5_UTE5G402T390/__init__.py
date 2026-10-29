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
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import TafUeIphone

__maintainer__ = "Jin Yanyan"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "cindy.1.jin@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPC(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.21", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245", username="vrf4_sg3", password="Haz4_vrf_sg3", port="53390"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/usr/bin/iperf",
    port="53390",
)

_appserver = AppServer(_iperf_details_on_appserver)

_app_server_iphone = TafUeAppServer(app_server_name="APP_1",
                             address="10.57.191.245",
                             user="vrf4_sg3",
                             password="Haz4_vrf_sg3",
                             bind_interface_ip="10.57.191.245",
                             expected_prompt="vrf4_sg3@appserver ~")

_data_transfer_iperf_iphone = TafUeDataTransferProtocol(protocol_name='iperf',
                                                 app_server=_app_server_iphone,
                                                 interval=1)

_data_transfer_ping_iphone = TafUeDataTransferProtocol(protocol_name='ping',
                                                app_server=_app_server_iphone,
                                                interval=1)


_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53900",
)

_mtk_host_ssh_9 = SshServiceDetails(
    addr="10.57.150.61", username="mn5gran", password="nokia123@"
)

_mtk_host_ssh_10 = SshServiceDetails(
    addr="10.57.150.96", username="mn5gran", password="nokia123@"
)

_iperf_details_on_mtk_9 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_9,
    network_interface_address="10.57.191.245",
    iperf_interval=1,
    iperf_version=29,
    iperf_path="/usr/bin/iperf",
    port=53390,
)
_iperf_details_on_mtk_10 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_10,
    network_interface_address="10.57.191.245",
    iperf_interval=1,
    iperf_version=29,
    iperf_path="/usr/bin/iperf",
    port=53490,
)

# CI_Detail_UE_Type='Qualcomm'
_android0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCRA03BLVV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.171.81",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR30TXMMT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.171.85",
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40LFV6T",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.171.89",
)

_android3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CN202F60K",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.171.93",
)

_android4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCX20AGDKA",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.76.107 ",
)

_android5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["MediaTek"],
    mobile_network_text="172.250.171.77",
)

_android6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CR411TGDM",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.163",
)

_android7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CY21PCT1H",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.76.138",
)

_android8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR10X4W5A",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.135",
)

_android9 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.61", username="mn5gran", password="nokia123@"
    ),
    sec_key="172.250.167.3",
    server_dir="c:/pyro_server",
    server_port=8080,
    # edb_file_path="auto",
    edb_file_path="C:/tool/mtk/MDDB_MT6990_S00_NR16_R2_MD800_MP_W24_25_P5.EDB",
    log_filter='2.Gen98_Default_Standard',
    imei="0123456789ABCDEF",
    imsi="310260031398421",
    apn_url="fwa",
    iperf_details=_iperf_details_on_mtk_9,
    capabilities=["mtk", "Huawei"],
    serial_number="0123456789ABCDEF",
)

_android10 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.96", username="MN5GRAN", password="nokia123@"
    ),
    sec_key="172.250.171.70",
    server_dir="c:/pyro_server",
    server_port=8080,
    # edb_file_path="172.250.171.74",
    edb_file_path="C:/Tool/mtk/MDDB_MT6990_S00_NR16_R2_MD800_MP_W24_25_P5.EDB",
    log_filter='2.Gen98_Default_Standard',
    imei="0123456789ABCDEF",
    imsi="310260001006301",
    apn_url="weistatic",
    iperf_details=_iperf_details_on_mtk_10,
    capabilities=["mtk", "Huawei"],
    serial_number="0123456789ABCDEF",
)

_android11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCRA0FKNHJ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.76.112",
)

_android12 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCRA1GWA9N",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.160",
)

_android13 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCRA1HYDHV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.147",
)

_android14 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT50S88JZ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.159",
)

_android15 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW2107WLZ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.156",
)

_android16 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCY70R4B7A",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.252.76.108",
)

_android17 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CN604NHSZ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.144",
)

_android18 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCRA03BN8M",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.250.164.164",
)

_android19 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW20HNPSF",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.3",
)

_android20 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CX80CMAHK",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.4",
)

_android21 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CX22N5HTM",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.5",
)

_android22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="ZY22LR55LJ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.6",
)

# _android9= Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.150.61", username="nokia5g", password="noki@123"
#     ),
#     serial_number="0123456789ABCDEF",
#     server_dir="/cygdrive/c/pyro_server/",
#     python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python37/python.exe",
#     iperf_details=_iperf,
#     capabilities=["mtk"],
#     mobile_network_text="172.250.171.70",
# )
#
# _android10= Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.150.96", username="MN5GRAN", password="nokia123@"
#     ),
#     serial_number="0123456789ABCDEF",
#     server_dir="/cygdrive/c/pyro_server/",
#     python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python313/python.exe",
#     iperf_details=_iperf,
#     capabilities=["MediaTek"],
#     mobile_network_text="172.250.171.74",
# )
_android23 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.70", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="TDC00002FUM6",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
    mobile_network_text="172.249.72.26",
)
_android24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="PC24100073_AB76",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["MediaTek"],
    mobile_network_text="172.249.72.20",
)
_android25 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CT310C58T",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.16",
)
_android26 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CX148A5JW",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.12",
)
_android27 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CX508V5EV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.15",
)
_android28 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR110RSRT",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.10",
)
_android29 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40JH5LW",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.14",
)
_android30 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR40NZG0V",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.38",
)
_android31 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.212", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CX508V5EV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    mobile_network_text="172.249.72.28",
)

_hbte_params = {
    "ip_addr": "10.57.239.215",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params_1 = {
    "ip_addr": "10.57.230.20",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_1 = HBTE(**_hbte_params_1)

_hbte_params_2 = {
    "ip_addr": "10.57.239.211",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_2 = HBTE(**_hbte_params_2)

_hbte_params_3 = {
    "ip_addr": "10.57.239.212",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_3 = HBTE(**_hbte_params_3)

# 5GRU for classicalBTS
_ru_pdu1 = FACOM(addr="10.57.176.77", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.96", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu1.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu2 = FACOM(addr="10.57.176.77", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.23", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu3 = FACOM(addr="10.57.176.70", port_numbers=[4])

_ru3 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.161", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
     attenuation_ports=[
         _attenuator.attenuator_ports[9],
         _attenuator.attenuator_ports[10],
         _attenuator.attenuator_ports[11],
         _attenuator.attenuator_ports[12],
     ],
)

_ru_pdu4 = FACOM(addr="10.57.176.70", port_numbers=[6])
_ru4 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.96", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu4.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu5 = FACOM(addr="10.57.176.70", port_numbers=[1])
_ru5 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.23", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu5.pdu_ports[1],
     attenuation_ports=[
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
     ],
)

_ru_pdu6 = FACOM(addr="10.57.176.77", port_numbers=[2])
_ru6 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.161", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu6.pdu_ports[2],
    attenuation_ports=[
        _attenuator_1.attenuator_ports[5],
        _attenuator_1.attenuator_ports[6],
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
)

_ru_pdu7 = FACOM(addr="10.57.176.77", port_numbers=[4])
_ru7 = RU(
    ru_hw_group="AHVA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu7.pdu_ports[4],
    attenuation_ports=[
        _attenuator_1.attenuator_ports[9],
        _attenuator_1.attenuator_ports[10],
        _attenuator_1.attenuator_ports[11],
        _attenuator_1.attenuator_ports[12],
    ],
)

_ru_pdu8 = FACOM(addr="10.57.176.77", port_numbers=[6])
_ru8 = RU(
    ru_hw_group="AHVA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu8.pdu_ports[6],
    attenuation_ports=[
        _attenuator_1.attenuator_ports[13],
        _attenuator_1.attenuator_ports[14],
        _attenuator_1.attenuator_ports[15],
        _attenuator_1.attenuator_ports[16],
    ],
)

_ru_pdu9 = FACOM(addr="10.57.176.77", port_numbers=[5])
_ru9 = RU(
    ru_hw_group="AHVA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu9.pdu_ports[5],
    attenuation_ports=[
         _attenuator_2.attenuator_ports[13],
         _attenuator_2.attenuator_ports[14],
         _attenuator_2.attenuator_ports[15],
         _attenuator_2.attenuator_ports[16],
     ],
)

_ru_pdu10 = FACOM(addr="10.57.176.77", port_numbers=[3])
_ru10 = RU(
    ru_hw_group="AHLOA1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu10.pdu_ports[3],
    attenuation_ports=[
        _attenuator_3.attenuator_ports[5],
        _attenuator_3.attenuator_ports[6],
        _attenuator_3.attenuator_ports[7],
        _attenuator_3.attenuator_ports[8],
    ],
)

_ru_pdu11 = FACOM(addr="10.57.176.70", port_numbers=[6])
_ru11 = RU(
    ru_hw_group="AHFIB1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu11.pdu_ports[6],
    attenuation_ports=[
        _attenuator_3.attenuator_ports[9],
        _attenuator_3.attenuator_ports[10],
        _attenuator_3.attenuator_ports[11],
        _attenuator_3.attenuator_ports[12],
     ],
)
_ru_pdu12 = FACOM(addr="10.57.176.77", port_numbers=[4])
_ru12 = RU(
    ru_hw_group="AHVA1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu12.pdu_ports[4],
    attenuation_ports=[
        _attenuator_3.attenuator_ports[1],
        _attenuator_3.attenuator_ports[2],
        _attenuator_3.attenuator_ports[3],
        _attenuator_3.attenuator_ports[4],
     ],
)

# classical gNB LMP
_lmp_connection = SshServiceDetails(
    addr="10.57.226.141", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

# gNB PB
_gnb_pdu = FACOM(addr="10.57.176.71", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
   capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])
_du1 = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9, _ru10, _ru11, _ru12],
    f1_m_ip_addr="10.57.226.141",
    f1_c_ip_addr="10.57.226.141",
    f1_u_ip_addr="10.57.226.141",
)


# gNB MPlane IP
_cu1 = CU(
    backhaul_site_oam_ip="10.57.226.141",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.141", username="Nemuadmin", password="nemuuser"
    ),
)


# RealEnb2
_lmp_connection_enb2 = SshServiceDetails(
    addr="10.57.226.142", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.176.71", port_numbers=[3])
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_enb2,
  capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[3],
)
_real_enb2 = Airscale(common_units=[_common_unit_2])
_lte_real_enb2 = RealEnb(
    airscale=_real_enb2, rms=None, instance_id=39011, global_bts_id=3901155555
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
    dus=[_du1], cu=_cu1, instance_id=39011, global_bts_id=3901155555
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
    enbs=[_lte_real_enb2],
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
    ],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch],
    attenuator=[_attenuator, _attenuator_1, _attenuator_2, _attenuator_3],
    nms=_netact,
)
