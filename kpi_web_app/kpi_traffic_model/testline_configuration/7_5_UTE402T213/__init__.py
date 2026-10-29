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
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Prisma, Airphone, Qualcomm, QualcommUeType, Android
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline import LicenseKeeper
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

__maintainer__ = "xiangli.kong"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "xiangli.kong@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.138", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.108.221.70",
    mcc="460",
    mnc="2",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.221.135", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.68.87.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[4],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.68.87.81", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.211", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.71.197.38", port_numbers=[5])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWHQN,
)

_ru1_pdu = HBTE(addr="10.71.197.39", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHQN,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.71.197.37", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru, _ru1],
    f1_m_ip_addr="10.71.215.4",
)

_cu = CU(
    backhaul_site_oam_ip="10.71.215.4",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="MRBTS-10546", global_bts_id="NRBTS-10546"
)

# for QualComm UE
_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.149", username="nokia5G", password="noki@123"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki@123!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51213,
)
# CI_Detail_UE_Type='Askey'
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="2085f6b2",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006397",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)
##1 cell sa AND nsa
_2_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="c3d0c1ae",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006384",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_sigspark, _2_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
)
