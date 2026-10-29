import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import HBTE, TopYoung, FACOM
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline import LicenseKeeper

__maintainer__ = "wenjuan.cai"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "wenjuan.cai@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# # Test PC
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.58", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )
# Test PC
_host_primary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real EPC is used. epcsim is here only as a backup solution.
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

_ru_enb_pdu = HBTE(addr="10.68.87.29", port_numbers=[5])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[5],
)

##RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.13", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

# ##GNB1
##5GRU for TL1118 classicalBTS
_gnb_1_ru_1_pdu = HBTE(addr="10.68.87.10", port_numbers=[5])
#
_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[5],
    radio_type="AHLOA",
)
_attenuator = TopYoung(
    ip_addr="1.1.1.1", port=5000, attenuation_port_numbers=[1, 2, 9, 10]
)

_ru_1 = RU(
    ru_hw_group="",
    radio_type="AHLOA",
    serial_number="BL2223G1B4I",
)

_gnb_1_airscale_cu_lmp_primary_core = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)


_gnb_1_airscale_cu_capacity_unit_primary_core = CapacityUnit(
    addr="6.6.6.6", rus=[_ru_1]
)

_gnb_1_airscale_cu_primary_core = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_primary_core,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_primary_core],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu_primary_core])

_gnb_1_du = DU(airscale=_gnb_1_airscale, rus=[_gnb_1_ru_1], f1_m_ip_addr="10.101.36.3")
# _gnb_1_du = DU(
#     airscale=_gnb_1_airscale,
#     rus=[_gnb_1_ru_1, _gnb_1_ru_2],
#     f1_m_ip_addr="192.168.255.129",
# )


##CU for TL1118 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.36.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.36.3", username="Nemuadmin", password="nemuuser"
    ),
)

## TL1118 classicalBTS
_classical_gnb_1 = ClassicalBts(
    dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="430000", global_bts_id="430000"
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(addr="10.101.36.5", username="spark", password="spark")

_spark_appserver_ssh1 = SshServiceDetails(
    # addr="10.57.163.50", username="nokia", password="nokia123"
    addr="10.57.163.34",
    username="cmw_sg1",
    password="Noki_sg1@123!",
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki_sg1@123!"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51126,
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51127,
)

# spark license
_licensekeeper = LicenseKeeper(username="qian.liu@nokia-sbell.com", password="123456")

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="2347c249",
    server_dir="C:/Program Files (x86)/Spark1.1.2007.3/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100010646",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="2347c249",
    server_dir="C:/Program Files (x86)/Spark1.1.2007.3/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100010692",
    licensekeeper=_licensekeeper,
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

tl = TestLine(
    test_pcs=[_host_primary_core],
    test_pc=None,
    gnbs=[_classical_gnb_1],
    # enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_sigspark1, _sigspark2],
    # appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
