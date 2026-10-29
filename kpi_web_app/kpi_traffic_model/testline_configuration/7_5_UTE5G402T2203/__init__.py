import os
from taf.config.testline.testline import TestLine

# from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import (
    EPCSim,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
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
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.flexi import Flexi


__maintainer__ = "Lou Shuhui"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "Shuhui.lou@nokia-sbell.com"


# common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.71.197.61", port_numbers=[4])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[4],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.71.197.56", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_smod = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_ru_enb], system_module=[_smod])

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.71.197.61", port_numbers=[4])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWPQZ.value,
    #radio_type="AWPQZ",
)

_capacity_unit = CapacityUnit(
    addr="172.22.0.2",
    hardware_type="ASOE",
    rus=[_ru_1],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_pdu = HBTE(addr="10.71.197.56", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASOE",
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
    f1_m_ip_addr="10.71.215.104",
    cablinks=_ru_cablinks,
)


##CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.215.104",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.215.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.215.104",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.215.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.215.104",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.215.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.215.104",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.215.97", ip_prefix_length=27),
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASOE_AWPQZ"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11109", global_bts_id="11109"
)


# Honor

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.243",
    username="vrf4_sg1",
    password="vrf4@sg1",
    port=51015,
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.243",
    iperf_path="/usr/bin/iperf",
    port="51015",
)

_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 51015
_spark_appserver_ssh1 = SshServiceDetails(
    addr="10.57.191.243", username="vrf4_sg1", password="vrf4@sg1", port=51015
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address="10.57.191.243",
    iperf_path="iperf",
    port=51015,
)
# _appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Guang hetong150'
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")

# SIGSPARK
_ue0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.130", username="nokia5G", password="noki@123"
    ),
    serial_number="3df8a4f4",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python3",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100010657",
    licensekeeper=_licensekeeper,
)

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.130", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCT50S88JZ",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python3",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100010694",
    licensekeeper=_licensekeeper,
)

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.52", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    enbs=[_lte_real_enb],
    ues=[_ue0, _ue1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
