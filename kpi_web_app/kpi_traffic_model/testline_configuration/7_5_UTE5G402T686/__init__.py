import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
    TopYoung,
)  # added in taf.meta 5.4
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
from taf.config.testline.nms import NetAct

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer


__maintainer__ = "Shasha Liu"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_05_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "shasha.liu@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


##RealEnb
_real_enb_pdu = HBTE(addr="10.71.197.26", port_numbers=[1, 2, 3, 4, 5, 6, 7])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.241", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[7],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.71.197.24", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.154",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.154",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQE,  # radio_type='AEQE'
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.240", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.71.197.26", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.71.214.240")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.240",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.240/27"
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.240", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.240", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.214.240",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.240/27"
        ),
    ),
    x2u=NetworkAddress(
        v4="10.71.214.240",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.240/27"
        ),
    ),
    s1u=NetworkAddress(
        v4="10.71.214.240",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.240/27"
        ),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_AEQE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2586, global_bts_id=10917)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.52", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port="55955"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55686,
)
_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55687,
)
_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Honor 30s'

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.87", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220103005528",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG5_Mate30Pro", "cell_Mapping: [1]", "huawei"],
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.87", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="QKXUT20519006575",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf2,
    capabilities=["SG5_HONOR30s", "cell_Mapping: [1]", "huawei"],
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

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

# netact  qin
netact_id_Qin = {
    "cmwas_ip": "10.107.178.214",
    "user": "omc",
    "password": "Nokia123!",
    "url": "https://na20lbwas.qin1.srnhz.nsn-rdnet.net/",
    "url_user": "omc",
    "url_password": "Nokia123!",
    "mr": "MRC-5GSC-HZ/MR-5GSC-HZ",
}

_netact = NetAct(netact_id_Qin)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
    ues=[_ue1, _ue2],
)
