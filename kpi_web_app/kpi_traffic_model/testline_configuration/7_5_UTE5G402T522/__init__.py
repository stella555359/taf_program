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

__maintainer__ = "Dandan Fang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "dandan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.101.52.179",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[1, 2, 5, 6, 7, 8, 9, 10],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41108"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="iperf",
    port="41109",
)

_appserver = AppServer(_iperf_details_on_appserver)

# Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="/cygdrive/c/iperf",
    port="41108",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.207", username="nokia5G", password="noki@123"
    ),
    serial_number="73157682",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.207", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CR10CBRKR",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.101.46.42", port_numbers=[4])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.180", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=10275, global_bts_id=10275
)

# TL52-2
# 5GRU------------------------------------
# RU1  AHFIB FDD
_ru_pdu_522_0 = HBTE(addr="10.101.46.47", port_numbers=[2])

_ru_522_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_522_0.pdu_ports[2],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL1945V00LP",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

# RU2  AHLOA FDD
_ru_pdu_522_1 = HBTE(addr="10.101.46.40", port_numbers=[6])
_ru_522_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_522_1.pdu_ports[6],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2116G1CGJ",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

# RU3  AEHC FDD
_ru_pdu_522_2 = HBTE(addr="10.101.46.44", port_numbers=[5])
_ru_522_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_522_2.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    serial_number="L1212614395",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)


# DU
_lmp_connection_522 = SshServiceDetails(
    addr="10.101.52.178", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_522 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.46.42", port_numbers=[5])

_common_unit_522 = CommonUnit(
    lmp_connection=_lmp_connection_522,
    capacity_units=[_capacity_unit_522],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale_522 = Airscale(common_units=[_common_unit_522])

_du_522 = DU(
    airscale=_airscale_522,
    rus=[_ru_522_0, _ru_522_1, _ru_522_2],
    f1_m_ip_addr="10.101.52.178",
)

# CU
_cu_522 = CU(
    backhaul_site_oam_ip="10.101.52.178",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.178", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.178", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_522 = ClassicalBts(
    dus=[_du_522], cu=_cu_522, instance_id=10359, global_bts_id=10359
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="10.107.182.164", v6="xxx:xx::xxx", vlan_id=1)  # MME
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

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts_522],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
