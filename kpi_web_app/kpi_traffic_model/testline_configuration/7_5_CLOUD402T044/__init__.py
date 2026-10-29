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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    ASC,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.appserver import AppServer

__maintainer__ = "Ren Biyao"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "biyao.ren@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.57.167.50",
    mcc=262,
    mnc="03",
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10300,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename=None,
)


# App Server
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.4", username="mmw_sg1", password="mm@1"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="iperf",
    port="5410",
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

# #Cobham
_tm500_ssh = SshServiceDetails(
    addr="10.57.161.5", username="nokia5G", password="noki@123"
)

_tm500_iperf = IperfDataTransferDetails(
    ssh_connection_details=_tm500_ssh,
    network_interface_address="9.6.6.6",
    iperf_path="/cygdrive/c/Users/tester/Desktop/iperf_2.0.8/",
    port="41112",
)

# CI_Detail_UE_Type='Viavi'
_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.161.5", username="nokia5G", password="noki@123", private_key=""
    ),
    tma_command_port=5030,
    pdu_port=None,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA 4.47.0/Test Mobile Application/"
    "TmaApplication.exe",
    iperf_details=_tm500_iperf,
    asc=ASC(ipaddr="192.168.10.9", port=10011),
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.57.241.168", port_numbers=[6])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.237.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=56, global_bts_id=56)

# 5GRU------------------------------------
_attenuator = TopYoung(
    ip_addr="10.57.249.55", port=23, attenuation_port_numbers=[9, 10, 11, 12]
)
_ru_pdu = FACOM(addr="10.57.246.227", port_numbers=[4])

_ru = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AAHF,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
    ],
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.57.237.50", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.241.168", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.237.50")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.57.237.50",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.237.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.237.50", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=44, global_bts_id=1)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    core=_epc_sim,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    ues=[_tm500],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    test_pcs=[_host],
    appserver=_appserver,
)


# SCF related configuration. Keep this part in this file temporary, will
# remove it when go to UTE
PARAMS_TO_MODIFY_SCF = [
    dict(
        value="TL044_ta_19B",
        dist_name="MRBTS-" + str(tl.gnbs[0].instance_id),
        p_name="btsName",
    ),
    dict(
        value="10.1.1.1",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/NRBTS-"
        + str(tl.gnbs[0].global_bts_id)
        + "/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="10.57.237.50",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="0.0.0.0",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="destIpAddr",
    ),
    dict(
        value="0",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="destinationIpPrefixLength",
    ),
    dict(
        value="10.57.237.33",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="gateway",
    ),
]
# Example for topyoung attenuator part
# print tl.attenuator.ip_addr
# print tl.attenuator.port
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[1].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
