import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore5G
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.enb import RealEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer

__maintainer__ = "Shasha Liu"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_05_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "shasha.liu@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.62", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #RealEnb
_real_enb_pdu = HBTE(addr="5.5.5.5", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.200", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=949)

# #5GRU for classicalBTS
# attenuator
_attenuator = AHBTE(
    ip_addr="9.8.8.8",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6],
    model="TAS16T16-51-120-1SDES",
)

_ru1_pdu = TopYoung(addr="10.101.46.52", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZQJ,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru2_pdu = TopYoung(addr="10.101.46.52", port_numbers=[5])

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru3_pdu = TopYoung(addr="10.101.46.52", port_numbers=[3])

_ru3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.10",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQJ,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru4_pdu = HBTE(addr="5.5.5.5", port_numbers=[3])

_ru4 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.49.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.49.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWEUA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = TopYoung(addr="10.101.46.54", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4], f1_m_ip_addr="10.101.52.226")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.52.226",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.101.52.225", destIpAddr="10.101.52.226/27"
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.226", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.52.226",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.101.52.225", destIpAddr="10.101.52.226/27"
        ),
    ),
    x2u=NetworkAddress(
        v4="10.101.52.226",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.101.52.225", destIpAddr="10.101.52.226/27"
        ),
    ),
    s1u=NetworkAddress(
        v4="10.101.52.226",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.101.52.225", destIpAddr="10.101.52.226/27"
        ),
    ),
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1B2B3_3*AZQJ_AWEUA"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2576, global_bts_id=10756)

# L3call
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55970
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/usr/bin/iperf",
    port=55971,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Samsung'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.225", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CR50DK0CH",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100001084",
    capabilities=["Samsung Galaxy S21", "cell_Mapping: [1]", "samsung"],
)

# netact
_netact = Netact("5.5.5.5")

_core = RealCore5G(mcc=262, mnc=3)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_core,
    nms=_netact,
    enbs=[_lte_real_enb],
    ues=[_ue1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
