import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import TopYoung as PBTopYoung
from taf.config.testline.ue import Prisma, MediaTek
from taf.config.testline.ue import Android
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE
from taf.config.testline import NetworkAddress

__maintainer__ = "Gao Ge"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "ge.gao@nokia-sbell.com"

## common The TL is same as TL10, The different is FDD configured as Primary of TL1113.
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.47", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real 5G Core

_amf_ssh = SshServiceDetails(
    addr="10.110.227.70", username="haijtest", password="Nokia_1234"
)

_amf_n2_addr = NetworkAddress(
    v4="10.110.227.5", v6="2a00:8a00:4000:65ef:ffff:ffff:ffff:b804", vlan_id=None
)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)


_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=460, mnc=2)


# 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="10.101.45.118", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[4],
)

##RealEnb
_real_enb_pdu = PBTopYoung(addr="10.101.45.54", port_numbers=[6])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.105", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##GNB1
##5GRU for TL010 classicalBTS

_left_ru_1_pdu = PBHBTE(addr="10.101.45.55", port_numbers=[1])
_left_ru_2_pdu = PBHBTE(addr="10.101.45.55", port_numbers=[3])
_left_ru_3_pdu = PBTopYoung(addr="10.101.45.56", port_numbers=[3])

_left_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_left_ru_1_pdu.pdu_ports[1],
    radio_type="AHLOA",
)

_left_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_left_ru_2_pdu.pdu_ports[3],
    radio_type="AHLOA",
)

_left_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_left_ru_3_pdu.pdu_ports[3],
    radio_type="AHLOA",
)

_attenuator = HBTE(
    ip_addr="10.68.88.110",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)


# #DU for TL010 classicalBTS
_airscale_cu_lmp = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_pdu = PBTopYoung(addr="10.101.45.56", port_numbers=[1])

_airscale_cu = CommonUnit(
    lmp_connection=_airscale_cu_lmp,
    capacity_units=[_airscale_cu_capacity_unit],
    pdu_port=_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_airscale_cu])

_du = DU(
    airscale=_airscale,
    rus=[
        _left_ru_1,
        _left_ru_2,
        _left_ru_3,
    ],
)

##CU for TL101 classicalBTS
_cu = CU(
    backhaul_site_oam_ip="10.101.49.99",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.99", username="Nemuadmin", password="nemuuser"
    ),
)

## TL10 classicalBTS
_classical = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="MRBTS-1011", global_bts_id="NRBTS-1011"
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.111", username="nokia5G", password="noki@123"
)

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

# CI_Detail_UE_Type='Huawei Mate 20;Huawei Mate 30'

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="WSY0220109002526",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    imsi="460028001006151",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="L8K5T19910016408",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    imsi="460028001006173",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical],
    enbs=[_lte_real_enb],
    core=_core,
    ues=[_sigspark1, _sigspark2],
    # appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
