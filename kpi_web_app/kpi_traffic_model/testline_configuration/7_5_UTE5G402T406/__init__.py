import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline import RU, DU
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb.du import Cablink, Endpoint
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
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
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

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid

__maintainer__ = "Zhenghua Lou"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "zhenghua.lou@nokia-sbell.com"

# common
__all__ = ["tl"]

_attenuator = ATTEN_HBTE(
    ip_addr="10.71.210.8",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[1, 2, 3, 4],
)

# _appserver_ssh = SshServiceDetails(
#     addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41812"
# )
#
# _iperf_details_on_appserver = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.57.178.10",
#     iperf_path="iperf",
#     port="41813",
# )
#
# _appserver = AppServer(_iperf_details_on_appserver)
#
# # Qualcomm
# _iperf = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.57.178.10",
#     iperf_path="/cygdrive/c/iperf",
#     port="41812",
# )
#
# _android_0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.71.217.106", username="mn5gran", password="nokia123@"
#     ),
#     serial_number="RFCW21P531R",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_ANDROID_UE", "samsung"],
# )

# AppServer info
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.57.191.194",
    user="vrf3_sg1",
    password="vrf3@sg1",
    ports=[41812, 41813],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    interface_name="rmnet_data0",
    bind_ue_ip="172.252.65.140",
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="wustatic", apnName="wustatic", apnType=["DEFAULT"]
)

# UE info
_android_1 = TafUeAndroid(
    serial_number="RFCW21P531R",
    capabilities=["REAL_UE","samsung_ue"],
    ue_pc_address="10.0.176.131",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.131", username="mn5gran", password="nokia123@"
    ),
    ue_pc_port="80",
    imei="355552518595658",
    imsi="262033100009248",
    pdns=[_pdn1],
    service_call_attach="17",
    service_call_detach="17",
    proxy_mngr_port="9955",
)


# TL406
# 5GRU------------------------------------
# RU1  AWMFIA FDD
_ru_pdu_406_0 = FPFH(
    addr="10.71.195.170",
    port_numbers=[2],
    login="admin",
    password="admin",
)

_ru_406_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_406_0.pdu_ports[2],
    radio_type="AWMFIA",
    serial_number="YK234700009",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# DU
_lmp_connection_406 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_406 = CapacityUnit(
    addr="192.168.253.20", hardware_type="ABIO"
)

ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_406, label="OPT", port_id=1),
        target=Endpoint(unit=_ru_406_0, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_406, label="OPT", port_id=2),
        target=Endpoint(unit=_ru_406_0, label="OPT", port_id=2),
    ),
     Cablink(
        source=Endpoint(unit=_capacity_unit_406, label="OPT", port_id=3),
        target=Endpoint(unit=_ru_406_0, label="OPT", port_id=3),
    ),
]

_gnb_pdu = HBTE(addr="10.71.195.172", port_numbers=[1])

_common_unit_406 = CommonUnit(
    lmp_connection=_lmp_connection_406,
    capacity_units=[_capacity_unit_406],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIL",
)

_airscale_406 = Airscale(common_units=[_common_unit_406])

_du_406 = DU(
    airscale=_airscale_406,
    rus=[_ru_406_0],
    f1_m_ip_addr="192.168.255.129",
)

# CU
_cu_406 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.37",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_406 = ClassicalBts(
    dus=[_du_406], cu=_cu_406, instance_id=10953, global_bts_id=10953
)

# cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MULTIRAT_ASILL_ABIOB1_AWMFIA"

# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="10.107.245.164", v6="xxx:xx::xxx", vlan_id=1)  # MME
_mme = MME(oam_ssh_connection_details=_mme_oam_ssh_connection_details, s1=_s1_address)
_real_4g_core_details = RealCore4GDetails(mme=_mme)

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.110.66.198")  # AMF
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=None,
    five_g=_real_5g_core_details,
    mcc="262",
    mnc="3",
    pdn=None,
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.64", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts_406.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_lte_real_enb = RealEnb(
    airscale=_airscale_406, rms=[_ru_406_0], instance_id=10953, global_bts_id=10503
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_406],
    enbs=[_lte_real_enb],
    ues=[_android_1],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    attenuators=[_attenuator],
    core=_realcore,
)
