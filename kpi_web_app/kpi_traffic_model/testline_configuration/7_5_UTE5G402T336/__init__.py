import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE
from taf.config.testline.attenuator import HBTE as PBHBTE
from taf.config.testline.ue import Android
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint

from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import LicenseKeeper

__maintainer__ = "Zhang Yu 8, Lei Jingyu"
__team__ = "MN 5G RAN I&V 3 Pz HZG SG2"
__email__ = "yu.8.zhang@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.165", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# 4GRU for RealEnb , device to be added
_ru_enb_pdu = HBTE(addr="10.57.1.2", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[1],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.101.45.80", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.101.45.210", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[5],
    radio_type="AHLOA",
)

_attenuator_RU1 = PBHBTE(
    ip_addr="10.101.51.54",
    port=5000,
    attenuation_port_numbers=[12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.40.232", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.45.208", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=2),
    )
]

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru_1], f1_m_ip_addr="10.101.51.71", cablinks=_ru_cablinks
)


##CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.71",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.71", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.71",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.71",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.71",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AEQN_HZIV"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="1100", global_bts_id="1100"
)


# Honor
# _ue_host_ssh = SshServiceDetails(
#     addr="10.101.47.50", username="nokia5G", password="noki@123"
# )
_ue_host_ssh = SshServiceDetails(
    addr="10.101.51.78", username="spark", password="spark"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="42336"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.2",
    iperf_path="/usr/bin/iperf",
    port="42336",
)

_appserver = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9EQUT20903003352",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
    imsi="460028001006181",
)
# _appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Honor 30s'
_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")
_ue1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4743a069",
    # server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    # python_path="/cygdrive/c/Python27/python.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100007838",
    licensekeeper=_licensekeeper,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    enbs=[_lte_real_enb],
    ues=[_ue1],
    tl_cloud_topology=_tl_cloud_topology,
    attenuators=[_attenuator_RU1],
    appserver=_appserver,
)
