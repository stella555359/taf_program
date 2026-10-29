import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import PduPort, Pdu, HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
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
from taf.config.testline.attenuator import (
    AttenuationPort,
)
from taf.config.testline.attenuator import HBTE as AHBTE
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
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
 
from taf.config.testline.flexi import Flexi
 
 
__maintainer__ = "Shasha Liu"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_05_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "shasha.liu@nokia-sbell.com"  # TL owner's email
 
# common
__all__ = ["tl"]
 
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
 
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.12", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
 
# import HBTE as AHBTE
_attenuator = AHBTE(
    ip_addr="10.101.52.230",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
 
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port="55955"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55956,
)
_appserver = AppServer(_iperf)
 
# CI_Detail_UE_Type='Huawei Honor 30s'
 
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.xx", username="nokia5G", password="noki@123"
    ),
    serial_number="QKX4C204280085xx",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG5_HONOR30s", "cell_Mapping: [1]", "huawei"],
)
 
# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.208", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.101.45.132", port_numbers=[4])
 
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
 
# 5GRU for classicalBTS
_ru1_pdu = TopYoung(addr="10.101.46.50", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
 
_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQK,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)
_ru2_pdu = TopYoung(addr="10.101.46.54", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
 
_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.14",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.14",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQJ,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)
 
_ru3_pdu = TopYoung(addr="10.101.46.52", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
 
_ru3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.38",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.38",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQE,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)
 
 
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.213.208", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.22")
 
_gnb_pdu = HBTE(addr="10.71.196.194", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
 
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1,_ru2,_ru3], f1_m_ip_addr="10.71.213.208")
 
# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.213.208",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.193/29"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.208", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.208", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.213.208",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.193/29"),
    ),
    x2u=NetworkAddress(
        v4="10.71.213.208",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.193/29"),
    ),
    s1u=NetworkAddress(
        v4="10.71.213.208",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.193/29"),
    ),
)
 
# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB+ABIO_AEQE*3"
 
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2589, global_bts_id=2589)
 
tl = TestLine(
    test_pc=_host,
    core=RealCore(mcc=262, mnc=3),
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
    ues=[_ue1],
)