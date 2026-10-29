import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.core import EPCSim
from taf.config.testline.pdu import HBTE
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule, RadioTypes
from taf.config.testline.attenuator import AttenuationPort

# TL002 configuration

__maintainer__ = "Frank Luo"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "frank.s.luo@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.240.18", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="2000",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.57.249.30", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[3],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.241.171", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.237.91", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classical BTS

_ru_1_pdu = HBTE(addr="10.57.249.31", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.5", username="user", password="pass"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQJ,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = HBTE(addr="10.57.241.131", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_1], f1_m_ip_addr="10.57.226.195")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.195", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="19002", global_bts_id="19002"
)

# qualcomm
_ue_host_ssh = SshServiceDetails(
    addr="10.57.150.74", username="nokia5G", password="noki@123"
)


####
_spark_appserver_ssh1 = SshServiceDetails(
    addr="10.57.163.34", username="nokia", password="nokia123"
)
_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=10000,
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.57.163.50", username="nokia", password="nokia123"
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port=10001,
)

# qualcomm on top cell
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="f67a63de",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    imsi="460028001006213",
    #    capabilities=["cell_Mapping: [1]", "qct_dx50"],
    capabilities=["huawei_sigspark"],
)

# qualcomm on bottom cell
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="c803df5a",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    imsi="460028001006214",
    #    capabilities=["cell_Mapping: [2]", "qct_dx50"],
    capabilities=["huawei_sigspark"],
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_sigspark, _sigspark_1],
    tl_cloud_topology=_tl_cloud_topology,
)
