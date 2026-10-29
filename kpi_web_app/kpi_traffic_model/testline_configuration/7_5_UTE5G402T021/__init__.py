import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "yin.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.164", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.57.240.220", username="root", password="lphtcxyz"
)

_ue_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_ue_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="iperf",
    port=51024,
)

_appserver = AppServer(_iperf_details_on_appserver)


# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e41bc73f",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996543",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="1feba6d",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996544",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="a64503d9",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996545",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="3d4a8e8d",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996546",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="5020a338",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996547",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="91c599bd",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996545",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="6bd7782f",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996545",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="55a003c9",
    server_dir="D:/Pilot Pioneer10.4.9.106/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996545",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)


# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.240.252", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.240.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb)

# #5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.57.240.205", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.18.33", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.18.33", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQG,
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.131.57", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.240.253", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.57.131.57")

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.131.57",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.57", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.57", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id="21", instance_id="21")

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_sigspark_1, _sigspark_2, _sigspark_3, _sigspark_4, _sigspark_5],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)

# compatibility workaround
tl = TestlineWrapper(tl)
