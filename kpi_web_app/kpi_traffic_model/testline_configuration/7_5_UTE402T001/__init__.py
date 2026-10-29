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
from taf.config.testline.core import EPCSim
from taf.config.testline.pdu import FACOM, HBTE, TopYoung
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.attenuator import HBTE as PAHBTE


__maintainer__ = "Gao Ge"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "ge.gao@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.102", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
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
_ru_enb_pdu = HBTE(addr="10.101.45.82", port_numbers=[6])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[6],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.68.87.114", port_numbers=[3])

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

_ru_1_pdu = TopYoung(addr="10.101.45.56", port_numbers=[4])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type="AEQN",
)

_ru_2_pdu = HBTE(addr="10.101.45.52", port_numbers=[6])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[6],
    radio_type="AEQV",
)

_ru_3_pdu = HBTE(addr="10.101.45.4", port_numbers=[6])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[6],
    radio_type="AQQL",
)

_ru_4_pdu = TopYoung(addr="10.101.45.53", port_numbers=[3])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_4_pdu.pdu_ports[3],
    radio_type="AEQN",
)

_ru_5_pdu = TopYoung(addr="10.101.45.5", port_numbers=[1])

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_5_pdu.pdu_ports[1],
    radio_type="AEQY",
)

_ru_6_pdu = HBTE(addr="10.101.45.4", port_numbers=[5])

_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_6_pdu.pdu_ports[5],
    radio_type="AQQL",
)

_ru_7_pdu = HBTE(addr="10.101.45.52", port_numbers=[4])

_ru_7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_7_pdu.pdu_ports[4],
    radio_type="AEQN",
)

_ru_8_pdu = TopYoung(addr="10.101.45.56", port_numbers=[5])

_ru_8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_8_pdu.pdu_ports[5],
    radio_type="AEQY",
)

_ru_9_pdu = HBTE(addr="10.101.45.9", port_numbers=[5])

_ru_9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_9_pdu.pdu_ports[5],
    radio_type="AQQL",
)

_ru_10_pdu = TopYoung(addr="10.101.45.83", port_numbers=[4])

_ru_10 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_10_pdu.pdu_ports[4],
    radio_type="AEQN",
)

_ru_11_pdu = TopYoung(addr="10.101.45.53", port_numbers=[6])

_ru_11 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_11_pdu.pdu_ports[6],
    radio_type="AEQV",
)

_ru_12_pdu = TopYoung(addr="10.101.45.5", port_numbers=[4])

_ru_12 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_12_pdu.pdu_ports[4],
    radio_type="AQQL",
)

_ru_13_pdu = HBTE(addr="10.101.45.82", port_numbers=[6])

_ru_13 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_13_pdu.pdu_ports[6],
    radio_type="AEQN",
)

_ru_14_pdu = TopYoung(addr="10.101.45.6", port_numbers=[7])

_ru_14 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_14_pdu.pdu_ports[7],
    radio_type="AEQV",
)

_ru_15_pdu = HBTE(addr="10.101.45.70", port_numbers=[5])

_ru_15 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_15_pdu.pdu_ports[5],
    radio_type="AQQL",
)

_ru_16_pdu = HBTE(addr="10.101.45.82", port_numbers=[3])

_ru_16 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_16_pdu.pdu_ports[3],
    radio_type="AEQN",
)

_ru_17_pdu = TopYoung(addr="10.101.45.87", port_numbers=[4])

_ru_17 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_17_pdu.pdu_ports[4],
    radio_type="AEQY",
)

_ru_18_pdu = HBTE(addr="10.101.45.82", port_numbers=[2])

_ru_18 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_18_pdu.pdu_ports[2],
    radio_type="AQQL",
)

_attenuator = PAHBTE(ip_addr="10.68.88.11", port=5000, attenuation_port_numbers=[7, 8])

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = TopYoung(addr="10.101.45.54", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru_1,
        _ru_2,
        _ru_3,
        _ru_4,
        _ru_5,
        _ru_6,
        _ru_7,
        _ru_8,
        _ru_9,
        _ru_10,
        _ru_11,
        _ru_12,
        _ru_13,
        _ru_14,
        _ru_15,
        _ru_16,
        _ru_17,
        _ru_18,
    ],
    f1_m_ip_addr="10.101.49.101",
)

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.101", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.101", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="1901", global_bts_id="1901"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.112", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="nokia", password="nokia123"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port=51040,
)

# CI_Detail_UE_Type='Huawei Mate 20'
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="L8K5T19920007306",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460028001006181",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
