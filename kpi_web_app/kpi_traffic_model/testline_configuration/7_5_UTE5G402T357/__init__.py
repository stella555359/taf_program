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
        addr="10.57.155.143", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245", username="vrf4_sg3", password="Haz4_vrf_sg3", port="53357"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/usr/bin/iperf",
    port="53357",
)

_appserver = AppServer(_iperf_details_on_appserver)


_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53457",
)

# CI_Detail_UE_Type='Qualcomm'
# _android0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.130.138", username="MN5GRAN", password="nokia123@"
#     ),
#     serial_number="e44b79d9",
#     server_dir="/cygdrive/c/pyro_server/",
#     python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python38/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["qct_dx50"],
# )

_ue_host_ssh = SshServiceDetails(
    addr="10.57.239.140", username="spark", password="spark"
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100001025",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100010207",
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100001046",
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100008771",
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100001020",
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100008768",
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260032997010",
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.5.0.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100008786",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.60", username="mn5gran", password="nokia123@"
    ),
    serial_number="2c13636f",
    sec_key="+6688",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python3/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "qct_dx50"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.193", username="mn5gran", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    sec_key="+6688",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python3/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "qct_dx50"],
)

_android3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.18", username="mn5gran", password="nokia123@"
    ),
    serial_number="adf1dfe8",
    sec_key="+6688",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python3/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "qct_dx50"],
)

_hbte_params = {
    "ip_addr": "10.57.239.135",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator = HBTE(**_hbte_params)

_hbte_params1 = {
    "ip_addr": "10.57.239.130",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator1 = HBTE(**_hbte_params1)

_hbte_params2 = {
    "ip_addr": "10.57.239.142",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator2 = HBTE(**_hbte_params2)

# 5GRU for classicalBTS
_ru_pdu1 = FACOM(addr="10.57.176.70", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.255", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru_pdu2 = FACOM(addr="10.57.176.70", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.131", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu3 = FACOM(addr="10.57.241.203", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu3.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu4 = FACOM(addr="10.57.176.70", port_numbers=[2])
_ru4 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu4.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_ru_pdu5 = FACOM(addr="10.57.176.71", port_numbers=[4])
_ru5 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu5.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu6 = FACOM(addr="10.57.176.71", port_numbers=[5])
_ru6 = RU(
    ru_hw_group="AHFB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.100", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu6.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

# classical gNB LMP
_lmp_connection = SshServiceDetails(
    addr="10.57.225.242", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection1 = SshServiceDetails(
    addr="10.57.226.139", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal IP
_capacity_unit = CapacityUnit(addr="192.168.253.20")

# gNB PB
_gnb_pdu = FACOM(addr="10.57.176.71", port_numbers=[3])
_gnb_pdu1 = FACOM(addr="10.57.176.71", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu1.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.57.225.242",
    f1_c_ip_addr="10.57.225.242",
    f1_u_ip_addr="10.57.225.242",
)

# gNB MPlane IP
_cu1 = CU(
    backhaul_site_oam_ip="10.57.225.242",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.242", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.242", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb1
_lmp_connection_enb1 = SshServiceDetails(
    addr="10.57.226.142", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_pdu = FACOM(addr="10.57.176.71", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb1,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)

_real_enb1 = Airscale(common_units=[_common_unit_1])

_lte_real_enb1 = RealEnb(
    airscale=_real_enb1, rms=None, instance_id=357, global_bts_id=357
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# switch port to EIF1
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.161", port="1/37", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# instance_id=MRBTS_ID
_classical_bts1 = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=357, global_bts_id=3571199999
)

_classical_bts2 = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=357, global_bts_id=3571299999
)

# realcore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.110.133.68", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)


_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=310, mnc=260)

# Netact IP
_netact = Netact("10.106.161.25")

tl = TestLine(
    test_pc=_host,
    core=_core,
    gnbs=[_classical_bts1,_classical_bts2],
    enbs=[_lte_real_enb1],
    ues=[_sigspark1, _sigspark2, _sigspark3, _sigspark4, _sigspark5, _sigspark6, _sigspark7, _sigspark8,
         _android1, _android2, _android3],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch],
    attenuator=[_attenuator, _attenuator1, _attenuator2],
    nms=_netact,
)
