import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Android
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import LicenseKeeper
from taf.config.testline.radio import RadioTypes

from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
#from taf.compatibility.configuration import TestlineWrapper


__maintainer__ = "Lou Shuhui"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "Shuhui.lou@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# 4GRU for RealEnb , device to be added
#_ru_enb_pdu = HBTE(addr="10.71.197.35", port_numbers=[1])

#_ru_enb = RadioModule(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="usr", password="psswd"
#    ),
#    pdu_port=_ru_enb_pdu.pdu_ports[1],
#)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.101.45.80", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.208", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.101.45.78", port_numbers=[4])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWHQN.value,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22", hardware_type="ABIO")

_gnb_pdu = HBTE(addr="10.101.45.80", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIB",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    ),
]

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
    f1_m_ip_addr="10.101.49.211",
    cablinks=_ru_cablinks,
)


##CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.49.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.49.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.49.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.49.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.193", ip_prefix_length=27),
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_AWHQN_CMA"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11105", global_bts_id="11105"
)

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.22", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


# Honor
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.83", username="nokia5G", password="noki@123"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki_sg1@123!", port="51100"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="/usr/bin/iperf",
    port="51100",
)

_appserver = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="389e436c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["huawei_sigspark"],
    imsi="460028001006401",
)

# _appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Sansumg S21'
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
##1 cell sa AND nsa

_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4701a2b1",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100007892",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

##2 cell sa AND nsa
_2_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="93c87d7b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006399",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    enbs=[_lte_real_enb],
    ues=[_sigspark, _2_sigspark],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
