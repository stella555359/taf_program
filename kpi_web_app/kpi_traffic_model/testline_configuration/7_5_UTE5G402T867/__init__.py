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
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)

__maintainer__ = "fred li"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "fred.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.124", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = HBTE(
    ip_addr="10.71.204.210",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

# 5GRU for classicalBTS
_ru_1_pdu = FACOM(addr="10.71.196.38", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[12],
    ],
)
_ru_2_pdu = FACOM(addr="10.71.196.38", port_numbers=[3])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[13],
    ],
)
_ru_3_pdu = FACOM(addr="10.71.196.38", port_numbers=[4])
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[14],
    ],
)
_ru_4_pdu = FACOM(addr="10.71.196.38", port_numbers=[5])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[5],
)
_ru_5_pdu = FACOM(addr="10.71.196.38", port_numbers=[6])

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_5_pdu.pdu_ports[6],
)
_ru_6_pdu = FACOM(addr="10.71.196.36", port_numbers=[1])

_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_6_pdu.pdu_ports[1],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")


_gnb_pdu = FACOM(addr="10.71.196.37", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6],
    f1_m_ip_addr="10.71.211.166",
)

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.166", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.166", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB1"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=867, instance_id=867)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.204.211", username="spark", password="spark"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57867,
)


# CI_Detail_UE_Type='Huawei honor 30s'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.186", username="mn5gran", password="nokia123@"
    ),
    # serial_number="afbf869b",
    serial_number="d49041fa",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "XIAOMI"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.186", username="mn5gran", password="nokia123@"
    ),
    serial_number="1827ef3b",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "XIAOMI"],
)

_sigspark0 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7f92be76",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008822",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="26fcb02f",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008823",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4661bf95",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008824",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="3274a15e",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008825",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7bd08eaf",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008826",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e2e67217",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008827",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9dbcdc36",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008828",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="64abfe6a",
    server_dir="C:/Program Files (x86)/Spark1.1.2000.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="001013100008829",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[
        _sigspark0,
        _sigspark1,
        _sigspark2,
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark6,
        _sigspark7,
        _android_0,
        _android_1,
    ],
    attenuator=[_attenuator],
)
