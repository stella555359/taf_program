import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.mcs import HBTE
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
# from taf.config.testline import HBTE
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
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
    TafUeAndroid,
    TafUeAt,
    TafUeFastmile,

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
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Wang Ming"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "ming.5.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.176", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# mcs
_hbte = HBTE(
    ip_addr="10.57.156.130",
    port="5000",
    mcs_port_numbers=[1],
    model="PPSAM-64X16-2.3-3.8-90-0.5-360-1-A",
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.90.130",
    mcc="262",
    mnc="03",
    tac="200",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.90.130", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.57.242.45", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.124", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=1, global_bts_id=15)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.242.53", port_numbers=[5])

_ru = RU(
    #'AEHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.229", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.254.33")

_gnb_pdu = FACOM(addr="10.57.242.45", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.223.229")

_cu = CU(
    backhaul_site_oam_ip="10.57.223.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.229", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="15")

_appserver_ssh = SshServiceDetails(
    # addr="10.57.162.12", username="cmw_sg2", password="cm@2"
    addr="10.57.163.35",
    username="cmw_sg2",
    password="12345678",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/usr/bin/iperf",
    port=52015,
)

# _ue_host_ssh = SshServiceDetails(
#    addr="10.57.240.212", username="root", password="Dinglicom"

_appserver = AppServer(_iperf)

_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.35",
    user="cmw_sg2",
    password="12345678",
    bind_interface_ip="10.57.163.35",
    expected_prompt="[cmw_sg2@cmw_sg2 ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52926, 52015],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile = TafUeFastmile(
    com_port="12",
    ue_pc_address="10.57.130.153",
    root_password="4eba95a2b662",
    ue_manage_ip="192.168.1.1",
    serial_number="aaf3c86e",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.1",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)


_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="f49aa628",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004124",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="7c616fb5",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004120",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="dc1fcb83",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    python_path="C:/Python27/python.exe",
    # diag_cfg_path='C:/pyro_server/DIAG.cfg',
    iperf_details=_iperf,
    imsi="262033100004126",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="77cac0a5",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004125",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="46c766e7",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262038001006322",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="a8b1aabb",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100004119",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="2ca15992",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100004123",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="spark", password="spark"
    ),
    serial_number="8aacd3b2",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100004122",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)



_sigspark_11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="a64503d9",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996921",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_12 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="91c599bd",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996543",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_13 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="55a003c9",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996545",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_14 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="5020a338",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006437",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_15 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="e41bc73f",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996546",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_16 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="6bd7782f",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996544",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_17 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="3d4a8e8d",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996547",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_18 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.135", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="D:\spark\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996919",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_21 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006084",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006090",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_23 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006324",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032995918",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_25 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006431",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_26 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032995930",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_27 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006247",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_28 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.134", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.4\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006418",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_31 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006422",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_32 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006438",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_33 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996942",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_34 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032995955",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_35 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996939",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_36 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996941",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_37 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006419",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_38 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="spark", password="spark"
    ),
    serial_number="1feba6d",
    server_dir="C:\\spark\\Spark1.1.2008.60\\Bin\\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006420",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    core=_epc_sim,
    ues=[
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
        _sigspark_11,
        _fastmile,
        _sigspark_13,
        _sigspark_14,
        _sigspark_15,
        _sigspark_16,
        _sigspark_17,
        _sigspark_18,
        _sigspark_21,
        _sigspark_22,
        _sigspark_23,
        _sigspark_24,
        _sigspark_25,
        _sigspark_26,
        _sigspark_27,
        _sigspark_28,
        _sigspark_31,
        _sigspark_32,
        _sigspark_33,
        _sigspark_34,
        _sigspark_35,
        _sigspark_36,
        _sigspark_37,
        _sigspark_38,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    mcses=_hbte,
)
