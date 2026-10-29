import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.appserver import AppServer
from taf.config.testline import NetworkAddress, RoutingInformation

__maintainer__ = "y63li"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "george.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.101.45.232", port_numbers=[4])

_ru = RU(
    ru_hw_group="hw_group",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.226.195", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.234", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.226.195", cablinks=_ru_cablinks, oam_ip="10.57.226.195",
)

# RealEnb
_real_enb_pdu = HBTE(addr="10.101.45.234", port_numbers=[3])
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.226.194", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.0.0.0", port="1/6", username="xx", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

## switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.0.0.0", port="1/9", username="xx", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

##CU
_cu_oam_ip = NetworkAddress("10.101.43.66", vlan_id=None)
_f1m = NetworkAddress(v4="10.10.10.10", v6="xxxx", vlan_id=None)
_f1c = NetworkAddress(
    v4="10.57.159.66",
    v6="xxxx",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.159.65", ip_prefix_length=26),
)
_f1u = NetworkAddress(
    v4="10.57.159.67",
    v6="xxxx",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.159.65", ip_prefix_length=26),
)
_x2c = NetworkAddress(
    v4="10.57.159.136",
    v6="xxxx",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.159.129", ip_prefix_length=26),
)
_x2u = NetworkAddress(
    v4="10.57.159.137",
    v6="xxxx",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.159.129", ip_prefix_length=26),
)
_s1c = NetworkAddress(
    v4="10.57.159.136",
    v6="xxxx",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.159.129", ip_prefix_length=26),
)
_s1u = NetworkAddress(
    v4="10.57.159.137",
    v6="xxxx",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.159.129", ip_prefix_length=26),
)
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")

_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.195", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)


_classical_bts = ClassicalBts(
    dus=[_du],
    cu=_cu,
    instance_id=10210,
    global_bts_id=10210,
)


# iperf server
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.3", username="mmw_sg3", password="test@123!", port="43067"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/usr/bin/iperf",
    port="43077",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="iperf",
    port="43045",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# Qualcomm UE as Android
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.137", username="nokia5G", password="noki@123"
    ),
    serial_number="d98acb45",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    clear_server_files="yes",
    clear_logs="yes",
    # capabilities=["REAL_UE", "huawei"],
    capabilities=["REAL_UE", "qct_dx50"],
)

# Netact

_netact = Netact(addr="10.107.178.214")

tl = TestLine(
    test_pc=[_test_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    ues=[_android],
    appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
    nms=_netact,
)
