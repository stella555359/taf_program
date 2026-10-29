import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    FPFH,
)
from taf.config.testline.pdu import TopYoung as PBTopYoung
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
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# from taf.config.testline.attenuator import (
#    AttenuationPort,
#    TopYoung,
# )  # added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as PAHBTE

from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
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

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline import NetworkAddress, RoutingInformation

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


##RealEnb #SA mode
"""
 _real_enb_pdu = PBTopYoung(addr="10.71.196.206", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

 _common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
 )

 _real_enb = Airscale(common_units=[_common_unit_2])

 _lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

"""

# 5GRU for classicalBTS

_attenuator = PAHBTE(
    ip_addr="10.71.214.10", port=5000, attenuation_port_numbers=[13, 14, 15, 16]
)

_ru1_pdu = PBTopYoung(addr="10.71.196.206", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQQL,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru2_pdu = PBTopYoung(addr="10.71.196.206", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQL,
)

_ru3_pdu = PBTopYoung(addr="10.71.196.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.18",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQL,
)

_ru4_pdu = PBTopYoung(addr="10.71.196.210", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.26",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.26",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru4_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQS,
)

# NO PB for AWHQX
_ru5_pdu = PBTopYoung(addr="10.71.XXX.XXX", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.30",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.30",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru5_pdu.pdu_ports[6],
    radio_type=RadioTypes.AWHQX,
)

_ru6_pdu = PBTopYoung(addr="10.71.197.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru6 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.34",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.34",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru6_pdu.pdu_ports[1],
    radio_type=RadioTypes.AKQJ,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIP",
)

_gnb_pdu = HBTE(addr="10.71.196.209", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=4),
        target=Endpoint(unit=_ru2, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=5),
        target=Endpoint(unit=_ru3, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=6),
        target=Endpoint(unit=_ru3, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="OPT", port_id=7),
        target=Endpoint(unit=_ru4, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="OPT", port_id=8),
        target=Endpoint(unit=_ru5, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="OPT", port_id=9),
        target=Endpoint(unit=_ru6, label="OPT", port_id=1),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.214.17",
    cablinks=_ru_cablinks,
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.17",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.1", destIpAddr="10.71.214.17/27"
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.17", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.17", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.214.17",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.1", destIpAddr="10.71.214.17/27"
        ),
    ),
    x2u=NetworkAddress(
        v4="10.71.214.17",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.1", destIpAddr="10.71.214.17/27"
        ),
    ),
    s1u=NetworkAddress(
        v4="10.71.214.17",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.1", destIpAddr="10.71.214.17/27"
        ),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASILL_ABIPB1_AQQL"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2660, global_bts_id=10919)

# CI_Detail_UE_Type='Huawei Honor 30s'
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55945
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55946,
)

_appserver = AppServer(_iperf)

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.62", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS5T19C13014719",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["Mate 30Pro", "cell_Mapping: [1]", "huawei"],
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.62", username="ute", password="ute"
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
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    ues=[_ue1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    attenuator=_attenuator,
)
