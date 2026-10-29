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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.attenuator import HBTE
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

__maintainer__ = "Wu Haihua"
__team__ = "NSB MN SRAN Prod HZH RRM 1 Vrf"
__email__ = "haihua.wu@nokia-sbell.com"

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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
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
        addr="10.56.17.22", username="spark", password="spark"
    ),
    serial_number="92fe6d23",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100015481",
    capabilities=["spark", "spark8"],
)

##RealEnb
_real_enb_pdu = FPFH(
    addr="10.56.17.20",
    port_numbers=[1],
    login="admin",
    password="admin",
#    model="FPFH",
)

# 5GRU for classicalBTS
_ru_pdu = FPFH(
    addr="10.56.17.24",
    port_numbers=[2],
    login="admin",
    password="admin",
#    model="FPFH",
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
    hardware_type="ASOE"
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# attenuator
_attenuator = TopYoung(
    ip_addr="10.56.17.23",
    port=1000,
    attenuation_port_numbers=[i for i in range(1, 256)],
    model="TAS32B8-51-120-1N-DES",
)

_ru_0 = RU(
    ru_hw_group="AHPB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.37.129", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type="AHPB",
#    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
    serial_number=None,
)

## DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
	hardware_type="ABIO"
	)
    
_gnb_pdu = FPFH(
    addr="10.56.17.20",
    port_numbers=[1],
    login="admin",
    password="admin",
#    model="FPFH",
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
	hardware_type="ASOE"
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=1),
    )
]

_du = DU(
    airscale=_airscale,
    rus=[_ru_0],
    f1_m_ip_addr="10.56.17.76",
    cablinks=_ru_cablinks,
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.56.17.76",
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.56.17.76", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.56.17.76", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.56.17.76",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    x2u=NetworkAddress(
        v4="10.56.17.76",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    ngc=NetworkAddress(
        v4="10.56.17.76",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    ngu=NetworkAddress(
        v4="10.56.17.76",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    xnc=NetworkAddress(
        v4="10.56.17.76",
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    xnu=NetworkAddress(
        v4="10.56.17.76",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
    s1u=NetworkAddress(
        v4="10.56.17.76",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.56.17.65", ip_prefix_length=24),
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du],instance_id=37545, global_bts_id=37545)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37545, global_bts_id=37545)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROIDx37545_ASOE_3xAQQJ_2xAHPB"

# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.56.198.96", username="ute", password="uteUTE!"
    ),
    connections=[_common_unit_2],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    ues=[_sigspark,_sigspark_1,_sigspark_2,_sigspark_3,_sigspark_4,_sigspark_5,_sigspark_6,_sigspark_7],
    appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
)
