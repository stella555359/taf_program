import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.core import RealCore

# from taf.config.testline.gnb.du import DU
from taf.config.testline import RU, DU
from taf.config.testline.gnb.du import Cablink, Endpoint

# from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine

# from taf.config.testline import HBTE_PDU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE

# from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
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
from taf.config.testline.attenuator import HBTE as hbte
from taf.config.testline.gnb.networkaddress import (
    NetworkAddress,
    RoutingInformation,
)  # add in taf.meta 5.4
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
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.testpc import Connection

__maintainer__ = "xiaodan.li"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "xiaodan.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53556",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53456",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53356",
)

_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei Mate 20'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.44", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCT32A5G7H",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung22"],
    imsi="10.57.167.18",
    sec_key="iW_K#8.ute%A10h0m0ra",
    dmc_path="10.70.255.38",
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.176.161", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.137", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=35621)

_hbte_params = {
    "ip_addr": "10.57.230.69",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator = hbte(**_hbte_params)

_ru1_pdu = HBTE(addr="10.57.176.161", port_numbers=[7])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[7],
    radio_type=RadioTypes.AWHHI.value,
    signal_analyzer=None,
    serial_number="EB2025R0336",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIL",
    # rus=[_ru1],
)

_gnb_pdu = HBTE(addr="10.57.176.161", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_common_unit_0])

# DU
# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
]

_du = DU(
    airscale=_airscale,
    f1_m_ip_addr="10.57.227.136",
    f1_c_ip_addr="10.57.227.136",
    f1_u_ip_addr="10.57.227.136",
    # cablinks=_ru_cablinks,
    rus=[_ru1],
)

# #CU
_cu = CU(
    # backhaul_site_oam_ip="10.57.236.184",
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.227.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.136", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.227.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.227.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.227.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
)

# classicalbts
_gnb = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=356111, global_bts_id=3561199999
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(addr="10.57.251.58", username="ute", password="uteUTE!"),
    connections=[Connection(interface="eth1", device=_gnb.dus[0].airscale.common_units[0],
                            interface_type="lmp")],
)

# #cloud_topology
# _tl_cloud_topology = "CLOUD_5G_BB3"
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIKL_ABILB1_AWHHI"

tl = TestLine(
    test_pc=_host,
    gnbs=[_gnb],
    enbs=[_lte_real_enb],
    ues=[_android],
    core=RealCore(mcc=262, mnc=3),
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
