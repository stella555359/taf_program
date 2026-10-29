import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Prisma, MediaTek
from taf.config.testline.ue import Android
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE

__maintainer__ = "Shi Taotao"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "taotao.shi@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.106", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.221.135", username="haijtest", password="Nokia@12345"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
_ru_enb_pdu = FACOM(addr="10.68.87.41", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[5],
)

##RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.13", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.15", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##GNB1
##5GRU for TL207 classicalBTS
_gnb_1_ru_1_pdu = PBHBTE(addr="10.68.87.42", port_numbers=[3])
_gnb_1_ru_2_pdu = PBHBTE(addr="10.68.87.59", port_numbers=[3])
_gnb_1_ru_3_pdu = PBHBTE(addr="10.68.87.42", port_numbers=[6])

_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[3],
    radio_type="AEQB",
)

_gnb_1_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_2_pdu.pdu_ports[3],
    radio_type="AEQB",
)

_gnb_1_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_3_pdu.pdu_ports[6],
    radio_type="AEQB",
)

_attenuator = HBTE(
    ip_addr="10.68.88.40",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

# #DU for TL207 classicalBTS
_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = PBHBTE(addr="10.68.87.13", port_numbers=[6])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[6],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_gnb_1_du = DU(
    airscale=_gnb_1_airscale,
    rus=[_gnb_1_ru_1, _gnb_1_ru_2, _gnb_1_ru_3],
    f1_m_ip_addr="10.57.251.190",
)

_du = DU(airscale=_gnb_1_airscale, rus=[_gnb_1_ru_1, _gnb_1_ru_2, _gnb_1_ru_3])

##CU for TL207 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.190", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.251.190", username="Nemuadmin", password="nemuuser"
    ),
)

## TL207 classicalBTS
_classical_gnb_1 = ClassicalBts(
    dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="207", global_bts_id="207"
)

# ##GNB20702
#
# _gnb_2_ru_1 = RU(
#     ru_hw_group="hw_group",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.53", username="user", password="pass"
#     ),
#     lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
#     pdu_port=_gnb_2_ru_1_pdu.pdu_ports[6],
#     radio_type="AEQB",
# )
#
# ##DU for TL20702 classicalBTS
# _gnb_2_airscale_cu_lmp = SshServiceDetails(
#     addr="10.68.88.106", username="toor4nsn", password="oZPS0POrRieRtu"
# )
#
# _gnb_2_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")
#
# _gnb_2_pdu = FACOM(addr="10.68.87.44", port_numbers=[4])
#
# _gnb_2_airscale_cu = CommonUnit(
#     lmp_connection=_gnb_2_airscale_cu_lmp,
#     capacity_units=[_gnb_2_airscale_cu_capacity_unit],
#     pdu_port=_gnb_2_pdu.pdu_ports[4],
# )
#
# _gnb_2_airscale = Airscale(common_units=[_gnb_2_airscale_cu])
#
# _gnb_2_du = DU(airscale=_gnb_2_airscale, rus=[_gnb_2_ru_1])
#
# ##CU for TL20702 classicalBTS
# _gnb_2_cu = CU(
#     backhaul_site_oam_ip="10.68.88.106",
#     oam_ssh_connection_details=SshServiceDetails(
#         addr="10.68.88.106", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     oam_http_connection_details=HttpConnectionDetails(
#         addr="10.68.88.106", username="Nemuadmin", password="nemuuser"
#     ),
# )
#
# # TL20702 classicalBTS
# _classical_gnb_2 = ClassicalBts(
#     dus=[_gnb_2_du],
#     cu=_gnb_2_cu,
#     instance_id="MRBTS-20702",
#     global_bts_id="NRBTS-20702",
# .)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.101.47.213", username="nokia5G", password="noki@123"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34",
    username="cmw_sg1",
    password="Noki_sg1@123!",
    port=51040,
)
_appserver_ssh1 = SshServiceDetails(
    addr="10.57.163.34",
    username="cmw_sg1",
    password="Noki_sg1@123!",
    port=51041,
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=51040,
)
_iperf1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh1,
    network_interface_address="10.57.163.34",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=51041,
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 51040

# CI_Detail_UE_Type='Huawei Honor 30s'
_sigspark1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.213", username="nokia5G", password="noki@123"
    ),
    serial_number="QKXUT20519006423",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_HONOR30s", "huawei"],
    imsi="460028001006151",
)

_sigspark2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.213", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20903003341",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf1,
    capabilities=["SG4_HONOR30s", "huawei"],
    imsi="460023032996641",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_gnb_1],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_sigspark1, _sigspark2],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
