import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import FPFH
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
from taf.config.testline import LicenseKeeper

__maintainer__ = "Jiajing Cheng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "jiajing.1.cheng@nokia-sbell.com"


## common
# __all__ = ["tl"]
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host_primary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host_secondary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.209", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.221.135", username="haijtest", password="Nokia@12345"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)


# ##Prisma
# _airmosaic_ssh = SshServiceDetails(addr='10.57.152.84', username='nokia', password='Tester123')
# _airmosaic_harness = HttpConnectionDetails(addr='10.57.152.84', port=8090)
# _lsu_uu_ssh = SshServiceDetails(addr='10.57.152.83', username='user', password='user')
# _tstm_uu_ssh = SshServiceDetails(addr='10.57.152.83', username='user', password='user')
#
#
# _prisma = Prisma(airmosaic_ssh_connection_details=_airmosaic_ssh,
#                     airmosaic_harness_connection_details=_airmosaic_harness,
#                     lsu_uu_ssh_connection_details=_lsu_uu_ssh,
#                     tstm_uu_ssh_connection_details=_tstm_uu_ssh
#                     )

##RealEnb
_real_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

# 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[2])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)


##GNB1
##5GRU for TL2242 classicalBTS
_gnb_1_ru_1_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[1])
_gnb_1_ru_2_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[2])
_gnb_1_ru_3_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[6])
_gnb_1_ru_4_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[3])

_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[1],
    serial_number="L1233410015",
    radio_type="AVQL",
)

_gnb_1_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_2_pdu.pdu_ports[2],
    serial_number="1M240305768",
    radio_type="AVQC",
)

_gnb_1_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_3_pdu.pdu_ports[6],
    serial_number="EA201356342",
    radio_type="AZQG",
)

_gnb_1_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_4_pdu.pdu_ports[3],
    serial_number="CV193900625",
    radio_type="AEQN",
)

_attenuator = HBTE(
    ip_addr="10.68.88.40",
    port=5000,
    attenuation_port_numbers=[9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

# #DU for TL2242 classicalBTS
# _gnb_1_airscale_cu_lmp_left = SshServiceDetails(
#     addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
# )

# _gnb_1_airscale_cu_lmp_right = SshServiceDetails(
#     addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
# )

_gnb_1_airscale_BBMOD_left_1 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_1])
_gnb_1_airscale_BBMOD_left_2 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_2])
_gnb_1_airscale_BBMOD_right_1 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_3])
_gnb_1_airscale_BBMOD_right_2 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_4])

_gnb_1_pdu = FPFH(addr="10.68.87.30", port_numbers=[2],login="admin", password="admin")
_gnb_2_pdu = FPFH(addr="10.68.87.26", port_numbers=[4],login="admin", password="admin")

# _gnb_1_airscale_cu_left = CommonUnit(
#     lmp_connection=_gnb_1_airscale_cu_lmp_left,
#     capacity_units=[_gnb_1_airscale_BBMOD_left_1, _gnb_1_airscale_BBMOD_left_2],
#     pdu_port=_gnb_1_pdu.pdu_ports[4],
# )
#
# _gnb_1_airscale_cu_right = CommonUnit(
#     lmp_connection=_gnb_1_airscale_cu_lmp_right,
#     capacity_units=[_gnb_1_airscale_BBMOD_right_1, _gnb_1_airscale_BBMOD_right_2],
#     pdu_port=_gnb_1_pdu.pdu_ports[4],
# )

# _gnb_1_airscale = Airscale(
#     common_units=[_gnb_1_airscale_cu_left, _gnb_1_airscale_cu_right]
# )

# _gnb_1_du = DU(
#     airscale=_gnb_1_airscale,
#     rus=[_gnb_1_ru_1, _gnb_1_ru_2, _gnb_1_ru_3, _gnb_1_ru_4],
#     f1_m_ip_addr="10.68.88.4",
# )


_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_BBMOD_left_1, _gnb_1_airscale_BBMOD_left_2],
    pdu_port=_gnb_1_pdu.pdu_ports[2],
)

_common_unit2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_BBMOD_right_1, _gnb_1_airscale_BBMOD_right_2],
    pdu_port=_gnb_2_pdu.pdu_ports[4],
)


_airscale1_left = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_BBMOD_left_1, _gnb_1_airscale_BBMOD_left_2],
    pdu_port=_gnb_1_pdu.pdu_ports[2],
)

_airscale2_right = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_BBMOD_right_1, _gnb_1_airscale_BBMOD_right_2],
    pdu_port=_gnb_2_pdu.pdu_ports[4],
)


_gnb_1_airscale = Airscale(
    common_units=[_airscale1_left, _airscale2_right]
)

_gnb_1_du = DU(
    airscale=_gnb_1_airscale,
    rus=[
        _gnb_1_ru_1,
        _gnb_1_ru_2,
        _gnb_1_ru_3,
        _gnb_1_ru_4,
    ],
    f1_m_ip_addr="10.101.52.101",
)


##CU for TL2242 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

## TL2242 classicalBTS
# _classical_bts = ClassicalBts(
#     dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="37582", global_bts_id="37582"
# )

_classical_gnb_1 = ClassicalBts(cu=_gnb_1_cu, dus=[_gnb_1_du], instance_id="37582", global_bts_id="37582")
## for MTK UE, just a placeholder for now, TL config not supported yet.
## _mtk_appserver_ssh = SshServiceDetails(addr='10.57.153.46', username='srn', password='Nokia@123')  # wap2
# _mtk_appserver_ssh = SshServiceDetails(addr='10.110.149.24', username='srn', password='Nokia@123')  # wap1
# _iperf_details_on_appserver=IperfDataTransferDetails(
#    ssh_connection_details=_mtk_appserver_ssh,
#    # network_interface_address='10.57.153.46',   # wap2
#    network_interface_address='10.110.149.24',   # wap1
#    iperf_path='iperf',
#    port=51014)
#
# _appserver = AppServer(_iperf_details_on_appserver)
# _mtk_host_ssh = SshServiceDetails(addr='10.57.152.83', username='CNHZ5GRAN1231+tester', password='HZnokia123!')
# _iperf_details_on_mtk = IperfDataTransferDetails(
#    ssh_connection_details=_mtk_host_ssh,
#    network_interface_address="",
#    iperf_path='iperf',
#    port=51014)
#
# _mtk = MediaTek(ssh_connection_details=_mtk_host_ssh,
#                   server_dir='c:/pyro_server',
#                   server_port=8080,
#                   edb_file_path='D:/MTK/SW/fix_crash/w19.41.p9_v1_3GPP_15.6_June/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB',
#                   imei='1234512345123478',
#                   imsi='262032001000316',
#                   apn_url='wap1.nokia.com',
#                   iperf_details=_iperf_details_on_mtk,
#                   capabilities=['REAL_MEDIATEK_UE'])
#
# _mtk_pdu = FACOM(addr='10.57.152.210', port_numbers=[7]).pdu_ports[7]
# _mtk.pdu = _mtk_pdu
#
# _mtk.inject_file = "D:/MTK/sa_test_1008.tcl"

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# SIGSPARK
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.164", username="MN5GRAN", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.195.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.195.48",
    iperf_path="iperf",
    port=50000,
)
# CI_Detail_UE_Type = "Huawei Honor 30s"
# _sigspark = Android(
#     ssh_connection_details=_ue_host_ssh,
#     serial_number="QKXUT20519006740",
#     server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_appserver,
#     capabilities=["cell_Mapping: [1]", "huawei"],
#     imsi="460023032996639",
# )

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="c50b149d",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["cell_Mapping: [1]", "Guanghetong", "huawei_sigspark"],
    imsi="460023100017424",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="1ffa515b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["cell_Mapping: [1]", "Guanghetong", "huawei_sigspark"],
    imsi="460023032996639",
    licensekeeper=_licensekeeper,
)

# for Honor UL traffic
_appserver = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="QKXUT20519006740",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023032996639",
    capabilities=["samsung"],
)

tl = TestLine(
    test_pcs=[_host_primary_core, _host_secondary_core],
    test_pc=_host_primary_core,
    gnbs=[_classical_gnb_1],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    # ues=[_prisma],
    ues=[_sigspark1, _sigspark2],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
