import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Prisma, MediaTek
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import AttenuationPort, TopYoung

__maintainer__ = "bin.3.wang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "bin.3.wang@nokia-sbell.com"


## common
# __all__ = ["tl"]
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host_primary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host_secondary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.30", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_ru_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[1])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[1],
)

##RealEnb
_real_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##GNB1
##5GRU for TL1111 classicalBTS
_gnb_1_ru_1_pdu = PBHBTE(addr="10.101.45.78", port_numbers=[6])
_gnb_1_ru_2_pdu = PBHBTE(addr="10.101.45.78", port_numbers=[2])
##_gnb_1_ru_2_pdu = FACOM(addr="10.57.249.15", port_numbers=[2])
##_gnb_1_ru_3_pdu = FACOM(addr="10.57.249.29", port_numbers=[1])

_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[6],
    radio_type="AEQN",
    serial_number="CV192700894",
)

_gnb_1_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_2_pdu.pdu_ports[2],
    radio_type="AEQN",
    serial_number="CV194001530",
)

_attenuator = TopYoung(
    ip_addr="1.1.1.1", port=5000, attenuation_port_numbers=[1, 2, 9, 10]
)

##DU for TL1111 classicalBTS
_gnb_1_airscale_cu_lmp_left = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_lmp_right = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(addr="6.6.6.6", rus=[_gnb_1_ru_1])

_gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(addr="6.6.6.6", rus=[_gnb_1_ru_2])

_gnb_1_pdu = PBHBTE(addr="10.101.45.80", port_numbers=[8])

_gnb_1_airscale_cu_left = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_left,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_gnb_1_pdu.pdu_ports[8],
)

_gnb_1_airscale_cu_right = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_right,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_right],
    pdu_port=_gnb_1_pdu.pdu_ports[8],
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_airscale_cu_left, _gnb_1_airscale_cu_right]
)

_gnb_1_du = DU(
    airscale=_gnb_1_airscale,
    rus=[_gnb_1_ru_1, _gnb_1_ru_2],
    f1_m_ip_addr="10.101.49.212",
)


##CU for TL1111 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.212", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.212", username="Nemuadmin", password="nemuuser"
    ),
)

## TL1111 classicalBTS
_classical_gnb_1 = ClassicalBts(
    dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="10267", global_bts_id="10267"
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.99", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh1 = SshServiceDetails(
    # addr="10.57.163.50", username="nokia", password="nokia123"
    addr="10.57.163.34",
    username="cmw_sg1",
    password="Noki_sg1@123!",
)
_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=10001,
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.57.163.34", username="nokia", password="Noki_sg1@123!"
)
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=10000,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="63bfa226",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "GuangHeTong", "huawei_sigspark"],
    imsi="460028001006398",
)


_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="63bfa226",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "GuangHeTong", "huawei_sigspark"],
    imsi="460028001006398",
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"


tl = TestLine(
    test_pc=None,
    test_pcs=[_host_primary_core, _host_secondary_core],
    gnbs=[_classical_gnb_1],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_sigspark1, _sigspark2],
    # appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
