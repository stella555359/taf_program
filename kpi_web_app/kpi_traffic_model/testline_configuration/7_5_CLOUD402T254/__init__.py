import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Liu Zheng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "zheng.4.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.182", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.4", username="mmw_sg1", password="mm@1", port="41508"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="/cygdrive/c/iperf",
    port="41509",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="iperf",
    port="41508",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.123", username="nokia5G", password="noki@123"
    ),
    serial_number="3839aaac",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.101.45.246", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=1170, global_bts_id=1170
)

# 5GRU------------------------------------

_ru1_pdu = HBTE(addr=" 10.101.45.246", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    serial_number="L1205002770",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.101.51.202", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.45.240", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.101.51.202")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.202",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.202", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.202", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1170, global_bts_id=1170)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
)

# SCF related configuration. Keep this part in this file temporary, will
# remove it when go to UTE
PARAMS_TO_MODIFY_SCF = [
    dict(
        value="TL254_ta",
        dist_name="MRBTS-" + str(tl.gnbs[0].instance_id),
        p_name="btsName",
    ),
    dict(
        value="0.0.0.0",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/NRBTS-"
        + str(tl.gnbs[0].global_bts_id)
        + "/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="10.57.228.109",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="28",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.57.228.97",
        dist_name="MRBTS-"
        + str(tl.gnbs[0].instance_id)
        + "/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="gateway",
    ),
]
# Example for topyoung attenuator part
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[1].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
