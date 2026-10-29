import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Airphone, Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE
from taf.config.testline import LicenseKeeper

__maintainer__ = "Li Yajie"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "yajie.li@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.186", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim  AMF3 10.110.227.5:10.110.227.70 for , AMF4 10.108.221.70:10.108.221.135
_epc_sim = EPCSim(
    mme_ip="10.108.221.70",
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
_ru_enb_pdu = PBHBTE(addr="10.71.197.56", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[3],
)


# #RealEnb
_real_enb_pdu = PBHBTE(addr="10.71.197.58", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)


##GNB1
##5GRU for TL003 classicalBTS
_ru_pdu = PBHBTE(addr="10.71.197.58", port_numbers=[2])
_ru2_pdu = PBHBTE(addr="10.71.197.58", port_numbers=[3])
# _ru3_pdu = PBHBTE(addr="10.57.246.209", port_numbers=[5])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.2.3.4", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.2.3.4", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type="AEQN",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.2.3.4", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.2.3.4", username="user", password="pass"),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type="AEQN",
)

# _ru3 = RU(
#    ru_hw_group="hw_group",
#    default_ssh_connection_details=SshServiceDetails(
#       addr="1.2.3.4", username="user", password="pass"
#    ),
#    lmp_connection=SshServiceDetails(addr="1.2.3.4", username="user", password="pass"),
#    pdu_port=_ru3_pdu.pdu_ports[5],
#    radio_type="AEQN",
# )


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.71.197.58", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    #    rus=[_ru, _ru2, _ru3],
    rus=[_ru, _ru2],
    f1_m_ip_addr="10.71.215.98",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.98", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="MRBTS-19003", global_bts_id="NRBTS-19003"
)


##GNB2
##5GRU for TL003_2 classicalBTS
#
# _gnb_2_ru_pdu = FACOM(addr="10.57.246.209", port_numbers=[3])
# _gnb_2_ru = RU(
#     ru_hw_group="hw_group",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.34", username="user", password="pass"
#     ),
#     lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
#     pdu_port=_gnb_2_ru_pdu.pdu_ports[3],
#     radio_type="AEQN",
# )
#
# ##DU for TL003_2 classicalBTS
# _gnb_2_airscale_cu_lmp = SshServiceDetails(
#     addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
# )
#
# _gnb_2_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")
#
# _gnb_2_pdu = FACOM(addr="10.57.246.201", port_numbers=[3])
#
# _gnb_2_airscale_cu = CommonUnit(
#     lmp_connection=_gnb_2_airscale_cu_lmp,
#     capacity_units=[_gnb_2_airscale_cu_capacity_unit],
#     pdu_port=_gnb_2_pdu.pdu_ports[3],
# )
#
# _gnb_2_airscale = Airscale(common_units=[_gnb_2_airscale_cu])
#
# _gnb_2_du = DU(airscale=_gnb_2_airscale, rus=[_gnb_2_ru])
#
#
# ##CU for TL003_2 classicalBTS
# _gnb_2_cu = CU(
#     backhaul_site_oam_ip="10.57.131.103",
#     oam_ssh_connection_details=SshServiceDetails(
#         addr="10.57.131.103", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     oam_http_connection_details=HttpConnectionDetails(
#         addr="10.57.131.103", username="Nemuadmin", password="nemuuser"
#     ),
# )
#
# # TL203 classicalBTS
# _classical_gnb_2 = ClassicalBts(
#     dus=[_gnb_2_du], cu=_gnb_2_cu, instance_id="MRBTS-1903", global_bts_id="NRBTS-203"
# )


_attenuator = HBTE(
    ip_addr="10.71.206.178",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    model="PA-16-16-6-127-0.5-B-S",
)


# UE-SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.218.61", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.71.219.233", username="cmw_sg1", password="cm@1"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.233",
    iperf_path="iperf",
    port=51003,
)
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")

## SA UE
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="f20825f3",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460028001006044",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

## NSA UE
_2_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="c08c718d",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460028001006029",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

tl = TestLine(
    test_pc=_host,
    # gnbs=[_classical_bts, _classical_gnb_2],
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_sigspark, _2_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
