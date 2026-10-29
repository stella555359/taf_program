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
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "zhang qingqing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "qingqing.zhang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.22", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.150",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53386",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port="53386",
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.206.53", username="spark", password="spark"
)

_ue_host_ssh1 = SshServiceDetails(
    addr="10.71.217.249", username="mn5gran", password="nokia123@"
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.71.207.150", username="vrf4_sg3", password="Haz4_vrf_sg3"
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port=54386,
)

# CI_Detail_UE_Type='MTK'
_mtk_host_ssh = SshServiceDetails(
    addr="10.0.176.105", username="mn5gran", password="nokia123@"
)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata1"),
    PDN(pdp_type=PDPTypes.IP.value, apn="ims")
]

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="10.0.176.105",
    iperf_path="/usr/bin/iperf",
    port=54386,
)

_appserver = AppServer(_iperf_details_on_appserver)

# spark license
_licensekeeper = LicenseKeeper(username="HAZ4_SG3", password="HAZ4_SG3")

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100008766",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="5c67ef2f",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100009203",
    licensekeeper=_licensekeeper,
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e66f249c",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260032994029",
    licensekeeper=_licensekeeper,
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e92637f1",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100001023",
    licensekeeper=_licensekeeper,
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh1,
    serial_number="e92637f1",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100001023",
    licensekeeper=_licensekeeper,
)

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    # edb_file_path="auto",
    edb_file_path="c:/Users/mn5gran/Desktop/tool/mtk/MDDB_MT6990_S00_NR16_R2_MD800_MP_W24_42_P3.EDB",
    log_filter='2.Gen98_Default_Standard',
    imei="0123456789ABCDEF",
    imsi="001013100011544",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["mtk", "Huawei"],
    serial_number="0123456789ABCDEF",
)

# #RealEnb
_capacity_unit2 = CapacityUnit(addr="10.71.214.114")

_real_enb_pdu0 = FACOM(addr="10.71.196.246", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.114", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=_capacity_unit2,
    pdu_port=_real_enb_pdu0.pdu_ports[1],
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=38621)

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="310", mnc="260", pdns=_pdns)

# #attenuator
_hbte_params = {
    "ip_addr": "10.71.206.21",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params1 = {
    "ip_addr": "10.71.206.25",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator1 = HBTE(**_hbte_params1)


_ru1_pdu = FACOM(addr="10.71.196.248", port_numbers=[5])
_ru2_pdu = FACOM(addr="10.71.196.248", port_numbers=[6])
_ru3_pdu = FACOM(addr="10.71.196.248", port_numbers=[4])
_ru4_pdu = FACOM(addr="10.71.196.247", port_numbers=[3])
_ru5_pdu = FACOM(addr="10.71.196.247", port_numbers=[4])
_ru6_pdu = FACOM(addr="10.71.196.247", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[3],
    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQO,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.49.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.49.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)


_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQU,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHFIG,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
)

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.166", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.57.166", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFIG,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.71.214.105", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.196.245", port_numbers=[5])

_gnb_pdu1 = FACOM(addr="10.71.196.245", port_numbers=[7])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.71.214.105",
    f1_c_ip_addr="10.71.214.105",
    f1_u_ip_addr="10.71.214.105",
)

_lmp_connection1 = SshServiceDetails(
    addr="10.71.214.106", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="10.57.223.107")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[7],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru3, _ru4, _ru5],
    f1_m_ip_addr="10.71.214.106",
    f1_c_ip_addr="10.71.214.106",
    f1_u_ip_addr="10.71.214.106",
)

_lmp_connection2 = SshServiceDetails(
    addr="10.71.214.111", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[7],
)

_airscale2 = Airscale(common_units=[_common_unit_2])

_du2 = DU(
    airscale=_airscale2,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.71.214.111",
    f1_c_ip_addr="10.71.214.111",
    f1_u_ip_addr="10.71.214.111",
)

_lmp_connection3 = SshServiceDetails(
    addr="10.71.214.106", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_3 = CommonUnit(
    lmp_connection=_lmp_connection3,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[7],
)

_airscale3 = Airscale(common_units=[_common_unit_3])

_du3 = DU(
    airscale=_airscale3,
    rus=[_ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.214.106",
    f1_c_ip_addr="10.71.214.106",
    f1_u_ip_addr="10.71.214.106",
)
# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.214.105",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.105", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.105", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.71.214.106",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.106", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.106", username="Nemuadmin", password="nemuuser"
    ),
)

_cu2 = CU(
    backhaul_site_oam_ip="10.71.214.111",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.111", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.111", username="Nemuadmin", password="nemuuser"
    ),
)

_cu3 = CU(
    backhaul_site_oam_ip="10.71.214.106",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.106", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.106", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=38611, global_bts_id=3861199999)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=38612, global_bts_id=3861299999)

_classical_bts2 = ClassicalBts(dus=[_du2], cu=_cu2, instance_id=38613, global_bts_id=3861399999)

_classical_bts3 = ClassicalBts(dus=[_du3], cu=_cu3, instance_id=38614, global_bts_id=3861499999)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1, _classical_bts2, _classical_bts3],
    core=_realcore,
    enbs=[_lte_real_enb0],
    ues=[_sigspark1, _sigspark2, _sigspark3, _sigspark4, _sigspark5, _mtk_ue_box],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator1],
    tl_cloud_topology=_tl_cloud_topology,
)
