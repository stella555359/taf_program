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
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
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
    LicenseKeeper,
)
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeMtk
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Chen Tong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "tong.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_appserver_ssh_mtk = SshServiceDetails(
    addr="10.71.207.143", username="vrf4_sg2", password="Vrf4@sg2_123456", port="52672"
)

_iperf_mtk = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.171", username="mn5gran", password="nokia123@"
    ),
    network_interface_address="10.71.217.171",
    iperf_path="/data/local/tmp/iperf",
    port="52726",
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxdata2"),
]

# for MediaTek
_mtk_appserver_taf = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.143",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.71.207.143",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=["52672", "52153"],
)
_mtk1_appserver_taf = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.143",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.71.207.143",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=["52673", "52152"],
)

_mtk_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_mtk_appserver_taf,
    interval=1,
    #binary_path="/data/iperf",
    version=2,
)

_mtk1_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_mtk1_appserver_taf,
    interval=1,
    #binary_path="/data/iperf",
    version=2,
)

_mtk = TafUeMtk(
    serial_number="MTK_26203",
    ue_pc_address="10.71.217.171",
    ue_pc_port=80,
    pdns=_pdns,
    data_transfer=[_mtk_data_transfer_iperf],
    com_port="auto",
    edb_file_path="C:/MTK/M90//MDDB_MT6986D_S00_NR17_R2_MP_W25_33_P1.EDB",
    log_filter="2.Gen97_Default_Standard",
    imei="123123123123244",
    imsi="262038001006322",
    default_pdn_name="dxdata2",
    capabilities=["REAL_MTK_UE", "mtk_ue"],
)

_pdn1 = PDNTafUeAndroidDetails(entryName='default',
                           apnName='apn1',
                           apnType=['DEFAULT']
)

_android_5G_mtk1 = TafUeAndroid(
    serial_number="MTK_26203",
    capabilities=["REAL_MTK_UE", "mtk_ue"],
    ue_pc_address="10.71.217.171",
    data_transfer=[_mtk_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="_mtk_data_transfer_iperf", username="mn5gran", password="nokia123@"
    ),
    ueproxy_force_release=False,
    ue_pc_port=80,
    imei="123123123123244",
    imsi="460023100024140",
    pdns=[_pdn1],
    qualcomm_prototype=False,
    voice_call_dialing_timeout="30",
    network_mode_switch_method="adb",
    airplane_mode_switcher_text="Airplane mode",
)

_android_5G_mtk2 = TafUeAndroid(
    serial_number="0123456789ABCDEF",
    capabilities=["REAL_MTK_UE", "mtk_ue"],
    ue_pc_address="10.0.176.180",
    data_transfer=[_mtk1_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="_mtk_data_transfer_iperf", username="mn5gran", password="nokia123@"
    ),
    ueproxy_force_release=False,
    ue_pc_port=80,
    imei="123123123123244",
    imsi="262038001006322",
    pdns=[_pdn1],
    qualcomm_prototype=False,
    voice_call_dialing_timeout="30",
    network_mode_switch_method="adb",
    airplane_mode_switcher_text="Airplane mode",
)
# SAMSUNG
_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.36", username="MN5GRAN", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.191.244", username="vrf4_sg2", password="Vrf4@sg2_123456"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.244",
    iperf_path="iperf",
    port=52771,
)

# CI_Detail_UE_Type='samsung_sigspark'
_sigspark_samsung = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="RFCW211XACR",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004087",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)


# 5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.71.197.15", port_numbers=[1])

_ru_0 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M242100017",
)

_ru_1_pdu = HBTE(addr="10.71.197.15", port_numbers=[2])

_ru_1 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
    serial_number="1M250305330",
)

_ru_2_pdu = HBTE(addr="10.71.197.15", port_numbers=[3])

_ru_2 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AVQC,
    serial_number="1M250305331",
)

_ru_3_pdu = HBTE(addr="10.71.197.15", port_numbers=[4])

_ru_3 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQC,
    serial_number="1M250305326",
)

_ru_4_pdu = HBTE(addr="10.71.197.75", port_numbers=[1])

_ru_4 = RU(
    #'AHEGB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHEGB,
    serial_number="DH241131447",
)

_ru_5_pdu = HBTE(addr="10.71.197.75", port_numbers=[3])

_ru_5 = RU(
    #'AHEGB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHEGB,
    serial_number="K9184605243",
)

_ru_6_pdu = HBTE(addr="10.71.197.75", port_numbers=[2])

_ru_6 = RU(
    #'AHEGB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_6_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHEGB,
    serial_number="EA204150627",
)

_ru_7_pdu = HBTE(addr="10.71.197.80", port_numbers=[2])

_ru_7 = RU(
    #'FXED'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_7_pdu.pdu_ports[2],
    radio_type=RadioTypes.ARHA,
    serial_number="1M242009638",
)

_ru_8_pdu = HBTE(addr="10.71.197.80", port_numbers=[3])

_ru_8 = RU(
    #'FXED'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_8_pdu.pdu_ports[3],
    radio_type=RadioTypes.FXED,
    serial_number="1M183029363",
)

_ru_9_pdu = HBTE(addr="10.71.197.80", port_numbers=[2])

_ru_9 = RU(
    #'FXED'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_9_pdu.pdu_ports[2],
    radio_type=RadioTypes.FXED,
    serial_number="1M184443506",
)

_ru_10_pdu = HBTE(addr="10.71.197.80", port_numbers=[3])

_ru_10 = RU(
    #'FXED'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_10_pdu.pdu_ports[3],
    radio_type=RadioTypes.FXED,
    serial_number="F7172416471",
)

_ru_11_pdu = HBTE(addr="10.71.197.80", port_numbers=[3])

_ru_11 = RU(
    #'FXED'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_11_pdu.pdu_ports[3],
    radio_type=RadioTypes.FXED,
    serial_number="1M192415520",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.215.216", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.71.197.87", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
         airscale=_airscale,
         rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9, _ru_10, _ru_11],
         f1_m_ip_addr="10.71.215.216"
)

_cu = CU(
    backhaul_site_oam_ip="10.71.215.216",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.216", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.216", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=20775, global_bts_id=20775)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.26", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_android_5G_mtk1, _sigspark_samsung,_android_5G_mtk2],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
)
