import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH, HBTE
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.attenuator import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline import Connection
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    Android,
    Qualcomm,
    QualcommUeType,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.appserver import AppServer
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.core import RealCore
from taf.config.testline.lmi import SerialOverTcp, Remote

__maintainer__ = "Song Jiana"
__team__ = "NSB MN SRAN Prod HZH RRM 1 Vrf"
__email__ = "jiana.song@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Iperf 
_appserver_ssh = SshServiceDetails(
    addr="10.21.41.84", username="ute", password="UTE.debian12", port="54015"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.21.41.84",
    iperf_path="/usr/bin/iperf",
    port="54015",
)

_appserver = AppServer(_iperf)

# Qualcomm

_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="f9ab6d9",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015474",
    capabilities=["spark", "spark1"],
)
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="fb137dc1",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015475",
    capabilities=["spark", "spark2"],
)
_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="c2ed32ff",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015476",
    capabilities=["spark", "spark3"],
)
_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="e56cda43",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015477",
    capabilities=["spark", "spark4"],
)
_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="d62d30f5",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015478",
    capabilities=["spark", "spark5"],
)
_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="b9d28f96",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015479",
    capabilities=["spark", "spark6"],
)
_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="9f94c6b1",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015480",
    capabilities=["spark", "spark7"],
)
_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.215", username="spark", password="spark"
    ),
    serial_number="92fe6d23",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015481",
    capabilities=["spark", "spark8"],
)

# smod port 2, AHLOB 3, 4, 5
_pdu_1 = PBHBTE(addr='10.108.190.163', port_numbers=[1, 2, 3, 4, 5, 6])

# AVHA port 1, 2, 3
_pdu_2 =  FPFH(addr='10.108.190.168', port_numbers=[1, 2, 3, 4, 5, 6], login="admin", password="admin")

# AHFII port 3, 4, 6
_pdu_3 =  FPFH(addr='10.56.202.66', port_numbers=[1, 2, 3, 4, 5, 6], login="admin", password="admin")

# attenuator
_attenuator = TopYoung(
    ip_addr="10.56.107.214",
    port=1000,
    attenuation_port_numbers=[i for i in range(1, 256)],
    model="TAS32B8-51-120-1N-DES",
)

_rmod_1 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHLOB",
    serial_number="AH252235839",
    pdu_port=_pdu_1.pdu_ports[3],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.245", port=5001),
        ]
    ),
)
_rmod_2 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHLOB",
    serial_number="AH252125642",
    pdu_port=_pdu_1.pdu_ports[4],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.246", port=5001),
        ]
    ),
)
_rmod_3 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHLOB",
    serial_number="AH252235625",
    pdu_port=_pdu_1.pdu_ports[5],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.244", port=5001),
        ]
    ),
)
_rmod_4 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHFII",
    serial_number="K9250711830",
    pdu_port=_pdu_3.pdu_ports[3],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.247", port=5001),
        ]
    ),
)
_rmod_5 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHFII",
    serial_number="K9250711712",
    pdu_port=_pdu_3.pdu_ports[4],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.248", port=5001),
        ]
    ),
)
_rmod_6 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHFII",
    serial_number="K9250711836",
    pdu_port=_pdu_3.pdu_ports[6],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.243", port=5001),
        ]
    ),
)
_rmod_7 = RU(
    ru_hw_group="cMAAr7.1_64T64R",
    radio_type="AVHA",
    serial_number="L1204708737",
    pdu_port=_pdu_2.pdu_ports[1],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.209", port=5001),
            Remote(addr="10.255.26.209", port=5002),
        ]
    ),
)
_rmod_8 = RU(
    ru_hw_group="cMAAr7.1_64T64R",
    radio_type="AVHA",
    serial_number="L1251001215",
    pdu_port=_pdu_2.pdu_ports[2],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.209", port=5001),
            Remote(addr="10.255.26.209", port=5002),
        ]
    ),
)
_rmod_9 = RU(
    ru_hw_group="cMAAr7.1_64T64R",
    radio_type="AVHA",
    serial_number="L1251001217",
    pdu_port=_pdu_2.pdu_ports[3],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.26.210", port=5001),
            Remote(addr="10.255.26.210", port=5002),
        ]
    ),
)

_fsp_1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIP",
    hardware_version="475792A.102",
    serial_number="L1251802089",
    rus=[_rmod_1, _rmod_2, _rmod_3],
)

_fsp_2 = CapacityUnit(
    addr="192.168.253.36",
    hardware_type="ABIP",
    hardware_version="475792A.102",
    serial_number="L1251802043",
    rus=[_rmod_7, _rmod_8, _rmod_9],
)

_fsp_3 = CapacityUnit(
    addr="192.168.253.40",
    hardware_type="ABIP",
    hardware_version="475792A.102",
    serial_number="L1251802046",
    rus=[_rmod_4, _rmod_5, _rmod_6],
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[2],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    serial_number="DH250612737",
)

_fct_2 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_2, _fsp_3],
    pdu_port=_pdu_1.pdu_ports[2],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    serial_number="DH250612728",
)

_smod_1 = Airscale([_fct_1])
_smod_2 = Airscale([_fct_2])

_enb_sbts_1 = RealEnb(system_module=_smod_1, rms=[_rmod_1, _rmod_2, _rmod_3])
_enb_sbts_2 = RealEnb(
    system_module=_smod_2, rms=[_rmod_4, _rmod_5, _rmod_6, _rmod_7, _rmod_8, _rmod_9]
)
_enb_sbts_1.slave = _enb_sbts_2

## DU for classicalBTS
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[2],
	hardware_type="ASIM"
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_2, _fsp_3],
    pdu_port=_pdu_1.pdu_ports[2],
	hardware_type="ASIM"
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5, _rmod_6, _rmod_7, _rmod_8, _rmod_9],
    f1_m_ip_addr="10.56.107.138",
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.56.107.138",
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.56.107.138", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.56.107.138", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.56.107.138",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.56.107.138",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.56.107.138",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.56.107.138",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    xnc=NetworkAddress(
        v4="10.56.107.138",
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    xnu=NetworkAddress(
        v4="10.56.107.138",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.56.107.138",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.107.129", ip_prefix_length=26),
    ),
)

# #host
_test_pc_1 = TestPc(
    SshServiceDetails(addr="10.56.218.242", username="ute", password="uteUTE!"),
    connections=[
        Connection(
            interface="eth1",
            device=_enb_sbts_1.system_module.common_units[0],
            interface_type="lmp",
        )
    ],
)
_test_pc_2 = TestPc(
    SshServiceDetails(addr="10.56.218.243", username="ute", password="uteUTE!"),
    connections=[
        Connection(
            interface="eth1",
            device=_enb_sbts_2.system_module.common_units[0],
            interface_type="lmp",
        )
    ],
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37545, global_bts_id=37545)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_Android_2xASIM_3xABIP_3xAHLOB_3xAHFII_3xAVHA_TMO"

tl = TestLine(
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1, _test_pc_2],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_enb_sbts_1, _enb_sbts_2],
    ues=[_sigspark,_sigspark_1,_sigspark_2,_sigspark_3,_sigspark_4,_sigspark_5,_sigspark_6,_sigspark_7],
    appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
)
