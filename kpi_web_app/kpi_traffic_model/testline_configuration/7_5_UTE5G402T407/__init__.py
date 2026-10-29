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

__maintainer__ = "Rong Wu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "rong.2.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.149", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.71.204.19",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[1, 2, 3, 4],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41814"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41813",
)

_appserver = AppServer(_iperf_details_on_appserver)

# Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41814",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.169", username="mn5gran", password="nokia123@"
    ),
    serial_number="123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "MTK"],
)

# TL407
# 5GRU------------------------------------
# RU1  AHFIB FDD
_ru_pdu_407_0 = HBTE(addr="10.71.204.19", port_numbers=[1])

_ru_407_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_407_0.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL2135V0K61",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# DU
_lmp_connection_407 = SshServiceDetails(
    addr="10.71.210.46", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_407 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.71.195.172", port_numbers=[1])

_common_unit_407 = CommonUnit(
    lmp_connection=_lmp_connection_407,
    capacity_units=[_capacity_unit_407],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale_407 = Airscale(common_units=[_common_unit_407])

_du_407 = DU(
    airscale=_airscale_407,
    rus=[_ru_407_0],
    f1_m_ip_addr="10.71.210.46",
)

# CU
_cu_407 = CU(
    backhaul_site_oam_ip="10.71.210.46",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.46", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.46", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_407 = ClassicalBts(
    dus=[_du_407], cu=_cu_407, instance_id=11595, global_bts_id=11595
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

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
_n2_address = NetworkAddress(v4="10.110.227.5")  # AMF
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=None,
    five_g=_real_5g_core_details,
    mcc="460",
    mnc="2",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_407],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
