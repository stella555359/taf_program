import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import MediaTek, LicenseKeeper
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.pdn import PDNAndroidDetails
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Wang lei"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "lei.24.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.84", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = HBTE(
    ip_addr="10.57.236.3",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

# 5GRU for classicalBTS
_ru_1_pdu = FACOM(addr="10.57.241.142", port_numbers=[6])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[12],
    ],
)
_ru_2_pdu = FACOM(addr="10.57.241.142", port_numbers=[7])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[7],
    attenuation_ports=[
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[13],
    ],
)
_ru_3_pdu = FACOM(addr="10.57.241.142", port_numbers=[8])
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[14],
    ],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# _capacity_unit_1 = CapacityUnit(addr="192.168.253.20")
_capacity_cpue = CapacityUnit(addr="192.168.255.129")
_capacity_loki = CapacityUnit(addr="192.168.253.17")


_gnb_pdu = FACOM(addr="10.57.241.142", port_numbers=[2])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.91", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_cpue, _capacity_loki],
    pdu_port=_gnb_pdu.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3],
    f1_m_ip_addr="10.57.225.66",
)

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.66", username="Nemuadmin", password="nemuuser"
    ),
)


##dcap
_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.40",
        port="443",
        username="utfuser",
        password="utfadmin!",
        # addr="10.101.60.56", port="443", username="utfuser", password="utfadmin!",
    )
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB1"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id=91, instance_id=91, dcap=_dcap_1
)


# CI_Detail_UE_Type='Huawei honor 30s'
# _android_0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.130.158", username="nokia5G", password="noki@123"
#     ),
#     serial_number="XXXX",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_ANDROID_UE", "qct_dx50"],
# )

# MTK
_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port=58091
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    ports=[57091],
    port=57091,
)

_appserver = AppServer(_iperf_details_on_appserver)
_mtk_host_ssh = SshServiceDetails(
    addr="10.57.130.38", username="mn5gran", password="nokia123@"
)

_STU_host_ssh = SshServiceDetails(
    addr="10.57.130.39", username="mn5gran", password="nokia123@", port=57091
)

_iperf_stu = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.130.39",
    iperf_path="/usr/bin/iperf",
    port=57091,
)

_iperf_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    ports=[58091],
    port=58091,
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100009157",
    apn_url="dxdata1",
    iperf_details=_iperf_mtk,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="0123456789ABCDEF",
)

# _sigspark_1 = Android(
#     ssh_connection_details=_STU_host_ssh,
#     serial_number="0420243B2351002",
#     server_dir="C:/tool",
#     python_path="C:/Python27",
#     iperf_directory="C:/Program Files (x86)/Spark1.1.2009.3/Bin",
#     diag_com=25,
#     iperf_details=_iperf_stu,
#     imsi="262033100010765",
#     licensekeeper=LicenseKeeper(username="HAZ4_SG7", password="HAZ4_SG7"),
#     capabilities=["REAL_ANDROID_UE", "atcmd_sigspark"],
# )
# spark license
_licensekeeper = LicenseKeeper(
    username="zhe.1.lin@nokia-sbell.com", password="nokia123"
)


# SA   CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.39", username="MN5GRAN", password="nokia123@", port=25
    ),
    serial_number="346f795d",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100010765",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
    pdn=[
        PDNAndroidDetails(
            entryName="5gsahz",
            apnType=["DEFAULT", "MMS", "IMS", "HIPRI", "SUPL", "FOTA", "CBS", "XCAP"],
            apn="dxdata1",
        )
    ],
)

_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.40",
        username="utfuser",
        password="utfadmin!",
        port=49148,
        # addr="10.101.60.56",username="utfuser",password="utfadmin!",port=49148,
    )
)

_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    test_pcs=[_tce_pc],
    gnbs=[_classical_bts],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[
        _sigspark_1,
    ],
    attenuator=[_attenuator],
    appserver=_appserver,
)
