import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Android
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.attenuator import HBTE
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Frank Luo"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "frank.s.luo@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.240.37", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 4GRU for RealEnb , device to be added
_ru_enb_pdu = PBHBTE(addr="10.68.87.8", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[8],
)

##RealEnb
_real_enb_pdu = PBHBTE(addr="10.68.87.29", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.27", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)
##5GRU for classical BTS
_ru1_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type="AWPQZ",
)

_ru2_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type="AWPQZ",
)

_ru3_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[3])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type="AWPQZ",
)

_ru4_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[4])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type="AWPQZ",
)

_ru5_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[5])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.158",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru5_pdu.pdu_ports[5],
    radio_type="AWPQZ",
)

_ru6_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[6])

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.162",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru6_pdu.pdu_ports[6],
    radio_type="AWPQZ",
)
_attenuator = HBTE(
    ip_addr="10.68.88.11",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = PBHBTE(addr="10.68.87.22", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru3, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=7),
        target=Endpoint(unit=_ru4, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=8),
        target=Endpoint(unit=_ru5, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=9),
        target=Endpoint(unit=_ru6, label="SFP", port_id=1),
    ),
]
_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.101.52.99",
    cablinks=_ru_cablinks,
)

##CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.52.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.99", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.52.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.52.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.52.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.97", ip_prefix_length=27),
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1_AWHQN_ENB"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="19209", global_bts_id="19209"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.164", username="nokia5G", password="noki@123"
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
    serial_number="9YS0220103005660",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["huawei_sigspark"],
    imsi="460028001006163",
)
# _appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G;Huawei Mate 30 Pro 5G'
# SA
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9YS0220103005660",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006163",
    capabilities=["huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=RealCore(mcc=460, mnc=2),
    enbs=[_lte_real_enb],
    ues=[_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
)
