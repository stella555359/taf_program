import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, HBTE, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import HBTE as PA_HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes


__maintainer__ = "Chen Jun"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jun.8.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.240", username="vrf4_sg6", password="Nokia@1234567", port="56084"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.240",
    iperf_path="/cygdrive/c",
    port="56184",
)
_appserver = AppServer(_iperf)


# CI_Detail_UE_Type='MTK'
_ue_host_ssh_mtk_sa = SshServiceDetails(
    addr="10.57.150.140", username="MN5GRAN", password="nokia123@"
)

_mtk_sa = MediaTek(
    ssh_connection_details=_ue_host_ssh_mtk_sa,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100008738",
    apn_url="dxdata2",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="0123456789ABCDEF",
)


# attenuator
_attenuator = PA_HBTE(
    ip_addr="10.57.156.34",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

# #5GRU for classicalBTS
_ru1_pdu = FPFH(addr="10.57.172.34", port_numbers=[2])
_ru2_pdu = FPFH(addr="10.57.172.34", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    serial_number="1M251002412",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AVQC,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
    serial_number="1M251002413",
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIQ",
)

_capacity_unit2 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIQ",
)

_gnb_pdu = HBTE(addr="10.57.172.16", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.223.68",
)

# CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.223.68",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.68", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.223.68",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.223.68",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.223.68",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=84, global_bts_id=84)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.27", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MTK_SA_ASILR_ABIQB4B5_2xAVQC"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_mtk_sa],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
)
