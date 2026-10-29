import os
from taf.config.testline.testline import TestLine

# from taf.config.testline.testpc import TestPc
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

# from taf.config.testline.radio import RadioTypes
from taf.config.testline.radio import (
    RadioTypes,
    RadioModule,
)
from taf.config.testline import LicenseKeeper

from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer

# from taf.compatibility.configuration import TestlineWrapper


__maintainer__ = "Lou Shuhui"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "Shuhui.lou@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# # 4GRU for RealEnb , device to be added
# _ru_enb_pdu = TopYoung(addr="10.101.45.85", port_numbers=[1])
#
# _ru_enb = RadioModule(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="1.1.1.1", username="usr", password="psswd"
#     ),
#     pdu_port=_ru_enb_pdu.pdu_ports[1],
# )
#
# # #RealEnb
# _real_enb_pdu = HBTE(addr="1.1.1.1", port_numbers=[4])
#
# _common_unit_2 = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.57.242.102", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     capacity_units=[],
#     pdu_port=_real_enb_pdu.pdu_ports[4],
# )
#
# _real_enb = Airscale(common_units=[_common_unit_2])
#
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.68.87.20", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHQX.value,
)

_ru_2_pdu = HBTE(addr="10.68.87.14", port_numbers=[8])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWHQN.value,
)

_ru_3_pdu = HBTE(addr="10.68.87.12", port_numbers=[2])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHQN.value,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)


_gnb_pdu = HBTE(addr="10.68.87.29", port_numbers=[4])

_capacity_unit1 = CapacityUnit(
    addr="172.22.0.2",
    hardware_type="ABIN",
)
_capacity_unit2 = CapacityUnit(
    addr="172.22.1.2",
    hardware_type="ABIO",
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3],
    f1_m_ip_addr="10.68.88.3",
    # cablinks=_ru_cablinks,
)


##CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.88.3",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.68.88.0", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.88.3",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.68.88.0", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.68.88.3",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.68.88.0", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.68.88.3",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.68.88.0", ip_prefix_length=27),
    ),
)


# Honor
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.42", username="nokia5G", password="noki@123"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.243", username="vrf4_sg1", password="vrf4@sg1", port="51100"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.243",
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

# CI_Detail_UE_Type='Guang hetong150'
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
_2_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="445f9c07",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006401",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

##1 cell sa AND nsa
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="389e436c",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100007899",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11051", global_bts_id="11051"
)

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.57", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASILL_ABINB1_2xAEQE"

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    #    enbs=[_lte_real_enb],
    ues=[_sigspark, _2_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
