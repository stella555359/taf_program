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
        addr="10.57.177.45", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="ims"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb1.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb.nokia.com")
]

_realcore = RealCore(
    four_g=None, five_g=None, mcc="001", mnc="01", pdns=_pdns,
)
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.150",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53387",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port="53387",
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.206.52", username="spark", password="spark"
)
_ue_host_ssh1 = SshServiceDetails(
    addr="10.0.176.184", username="mn5gran", password="nokia123@"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.0.176.183", username="mn5gran", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/usr/bin/iperf",
    port=53387,
)
_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.71.207.150", username="vrf4_sg3", password="Haz4_vrf_sg3"
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port=54387,
)
_appserver = AppServer(_iperf_details_on_appserver)
# spark license
_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011579",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="5c67ef2f",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011574",
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e66f249c",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011572",
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e92637f1",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011576",
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9974f381",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011578",
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8a4b1984",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011577",
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8ab3185f",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011575",
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="48d6b638",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011575",
)

_sigspark9 = Android(
    ssh_connection_details=_ue_host_ssh1,
    serial_number="48d6b638",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100011576",
)

# _mtk_pdu = FACOM(addr="10.57.151.19", port_numbers=[2]).pdu_ports[5]
_elt_path = "C:\tool\ELT_exe_v3.2416.0_customer_x64"

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/TOOl/mtk/MDDB_MT6990_S00_NR16_R2_MD800_MP_W24_25_P5.EDB",
    log_filter='2.Gen98_Default_Standard',
    imei="0123456789ABCDEF",
    imsi="001013100011544",
    apn_url="dxdata2",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["mtk", "huawei"],
    serial_number="0123456789ABCDEF",
)

# _mtk_ue_box.pdu = _mtk_pdu
_mtk_ue_box.elt_path = _elt_path

# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53387",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.241", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220227002526",
    imsi="460028001006302",
    sec_key="18001006302",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---01181451\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.241", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS5T19C09008603",
    imsi="001013100001043",
    sec_key="13100001043",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---01181451\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.240", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR10CV12Z",
    imsi="460028001006394",
    sec_key="18001006394",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---01181451\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.183", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="dd7afc79",
    imsi="460023100010156",
    sec_key="18000010156",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python39/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    pdn=["dxdata1", "mdrb.nokia.com", "mdrb1.nokia.com"],
)

# #RealEnb
_capacity_unit2 = CapacityUnit(addr="192.168.253.33")

_real_enb_pdu0 = FACOM(addr="10.71.196.246", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.108", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=_capacity_unit2,
    pdu_port=_real_enb_pdu0.pdu_ports[2],
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=38721)

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="310", mnc="260", pdns=None)

# #attenuator
_hbte_params = {
    "ip_addr": "10.71.206.36",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params1 = {
    "ip_addr": "10.71.206.23",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator1 = HBTE(**_hbte_params1)


_ru1_pdu = FACOM(addr="10.71.196.242", port_numbers=[1])
_ru2_pdu = FACOM(addr="10.71.196.242", port_numbers=[2])
_ru3_pdu = FACOM(addr="10.71.196.240", port_numbers=[3])
_ru4_pdu = FACOM(addr="10.71.196.248", port_numbers=[2])
_ru5_pdu = FACOM(addr="10.71.196.247", port_numbers=[1])
_ru6_pdu = FACOM(addr="10.71.196.247", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFIB,
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
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQO,
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
        addr="172.22.50.6", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.50.6", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFIB,
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
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
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
        addr="172.22.1.6", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.1.6", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
)

_ru7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)
_ru8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)
_ru9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.71.214.110", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.196.246", port_numbers=[2])

_gnb_pdu1 = FACOM(addr="10.71.196.246", port_numbers=[1])

_gnb_pdu2 = FACOM(addr="10.71.197.4", port_numbers=[5])

_gnb_pdu3 = FACOM(addr="10.71.197.4", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.71.214.110",
    f1_c_ip_addr="10.71.214.110",
    f1_u_ip_addr="10.71.214.110",
)

_lmp_connection1 = SshServiceDetails(
    addr="10.71.214.131", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection2 = SshServiceDetails(
    addr="10.71.214.109", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection3 = SshServiceDetails(
    addr="10.71.214.132", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="10.57.223.107")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[1],
)

_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu2.pdu_ports[5],
)

_common_unit_3 = CommonUnit(
    lmp_connection=_lmp_connection3,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu3.pdu_ports[6],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_airscale2 = Airscale(common_units=[_common_unit_2])

_airscale3 = Airscale(common_units=[_common_unit_3])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru5, _ru6],
    f1_m_ip_addr="10.71.214.131",
    f1_c_ip_addr="10.71.214.131",
    f1_u_ip_addr="10.71.214.131",
)

_du2 = DU(
    airscale=_airscale2,
    rus=[_ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.214.109",
    f1_c_ip_addr="10.71.214.109",
    f1_u_ip_addr="10.71.214.109",
)

_du3 = DU(
    airscale=_airscale3,
    rus=[_ru7, _ru8, _ru9],
    f1_m_ip_addr="10.71.214.132",
    f1_c_ip_addr="10.71.214.132",
    f1_u_ip_addr="10.71.214.132",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.214.110",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.110", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.110", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.71.214.131",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.131", username="Nemuadmin", password="nemuuser"
    ),
)

_cu2 = CU(
    backhaul_site_oam_ip="10.71.214.109",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.109", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.109", username="Nemuadmin", password="nemuuser"
    ),
)

_cu3 = CU(
    backhaul_site_oam_ip="10.71.214.132",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.132", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.132", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=38711, global_bts_id=3871199999)

_classical_bts2 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=38713, global_bts_id=38713)

_classical_bts1 = ClassicalBts(dus=[_du2], cu=_cu2, instance_id=38712, global_bts_id=3871299999)

_classical_bts3 = ClassicalBts(dus=[_du3], cu=_cu3, instance_id=38714, global_bts_id=38714)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[
        _classical_bts0,
        _classical_bts1,
        _classical_bts2,
        _classical_bts3,
    ],
    core=_realcore,
    enbs=[_lte_real_enb0],
    ues=[
        _sigspark1,
        _sigspark2,
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark6,
        _sigspark7,
        _sigspark8,
        _sigspark9,
        _mtk_ue_box,
        _android,
        _android_1,
        _android_2,
        _android_3
    ],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator1],
    tl_cloud_topology=_tl_cloud_topology,
)
