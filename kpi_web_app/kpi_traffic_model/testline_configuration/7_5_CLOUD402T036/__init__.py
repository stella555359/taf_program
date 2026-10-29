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
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek


__maintainer__ = "Xing Jing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jing.1.xing@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.143", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.161", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.228.113", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU for classicalBTS

_ru_pdu = FACOM(addr="10.57.246.244", port_numbers=[1])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.228.107", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.241.161", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])

_f1m = NetworkAddress(v6="2a00:8a00:8000:136:10:57:157:143")

# #CU
_routing = RoutingInformation(gateway="10.57.143.157", ip_prefix_length=0)
_f1m = NetworkAddress(
    v4="10.57.228.107",
    v6="2a00:8a00:8000:136:10:57:228:6b",
    vlan_id=5,
    routing=_routing,
)
_f1c = NetworkAddress(v4="10.57.228.107", vlan_id=5)
_f1u = NetworkAddress(v4="10.57.228.107", vlan_id=5)
_x2c = NetworkAddress(v4="10.57.228.107", vlan_id=5)
_x2u = NetworkAddress(v4="10.57.228.107", vlan_id=5)
_s1c = NetworkAddress(v4="10.57.228.107", vlan_id=5)
_s1u = NetworkAddress(v4="10.57.228.107", vlan_id=5)
_tracing = NetworkAddress(v4="10.57.228.107", vlan_id=5)

_cu = CU(
    backhaul_site_oam_ip="10.57.228.107",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.107", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.107", username="Nemuadmin", password="nemuuser"
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
# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1033)

# netact
_netact = Netact("10.57.243.56")


# for MTK UE, just a placeholder for now, TL config not supported yet.
_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="cmw_sg3", password="cmw_sg3"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port=53036,
)

# _mtk_pdu = FACOM(addr='10.57.249.10', port_numbers=[2]).pdu_ports[2]

_appserver = AppServer(_iperf_details_on_appserver)
_mtk_host_ssh = SshServiceDetails(
    addr="10.57.130.16", username="nokia5G", password="noki@123"
)
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="C:/07_MTK-UE/iPerfGui+/iperf.exe",
    port=53136,
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/07_MTK-UE/sw/0827knife/MDDB_MT6297_S00_VMOLY_APOLLO_SQC_W19_34_P4.EDB",
    imei="1234512345123478",
    imsi="262033032990160",
    # apn_url='wap1.nokia.com',
    apn_url="c3static",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_mtk],
    appserver=_appserver,
    enbs=[_lte_real_enb],
    nms=_netact,
    tl_cloud_topology=_tl_cloud_topology,
)
