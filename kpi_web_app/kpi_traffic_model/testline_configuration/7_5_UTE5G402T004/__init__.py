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
from taf.config.testline import LicenseKeeper
from taf.config.testline.attenuator import AttenuationPort, TopYoung

__maintainer__ = "Wang Lixia"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "lixia.wang@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.96", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.108.221.70",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="10.101.45.82", port_numbers=[6])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[6],
)

# #RealEnb
_real_enb_pdu = PBHBTE(addr="10.68.87.114", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.89.59", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classical BTS

_ru_1_pdu = PBHBTE(addr="10.68.87.18", port_numbers=[6])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[6],
    radio_type="AEQZ",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = PBHBTE(addr="10.68.87.21", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_1])

##CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.56",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.56", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.56", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="19605", global_bts_id="19605"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.111", username="mn5gran", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.71.207.142", username="vrf4_sg1", password="vrf4@sg1"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port=51040,
)

_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
# CI_Detail_UE_Type='Huawei Mate 20'
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9ec3260b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100007892",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
)
