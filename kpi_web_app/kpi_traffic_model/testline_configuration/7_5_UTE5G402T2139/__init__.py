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

__maintainer__ = "ludan Fang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "ludan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.64", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41679"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41679",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41678",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.150", username="mn5gran", password="nokia123@"
    ),
    serial_number="aa632c9d",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
)
# TL2138
# 5GRU------------------------------------
# RU1 AEHC
_ru_pdu_2139_0 = HBTE(addr="10.71.195.174", port_numbers=[3])
_ru_pdu_2138_0 = HBTE(addr="10.71.195.176", port_numbers=[5])
_ru_pdu_2137_0 = HBTE(addr="10.71.195.176", port_numbers=[3])

_ru_2139_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_2139_0.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    serial_number="30821090056",
)
_ru_2138_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_2138_0.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    serial_number="1M222643820",
)
_ru_2137_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_2137_0.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    serial_number="1M201201764",
)


# DU
_lmp_connection_2139 = SshServiceDetails(
    addr="10.71.210.49", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_2138 = SshServiceDetails(
    addr="10.71.210.48", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_2137 = SshServiceDetails(
    addr="10.71.210.43", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit_2139 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_2138 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_2137 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu_2139 = HBTE(addr="10.71.195.173", port_numbers=[4])
_gnb_pdu_2138 = HBTE(addr="10.71.195.173", port_numbers=[3])
_gnb_pdu_2137 = HBTE(addr="10.71.195.173", port_numbers=[2])

_common_unit_2139 = CommonUnit(
    lmp_connection=_lmp_connection_2139,
    capacity_units=[_capacity_unit_2139],
    pdu_port=_gnb_pdu_2139.pdu_ports[4],
)

_common_unit_2138 = CommonUnit(
    lmp_connection=_lmp_connection_2138,
    capacity_units=[_capacity_unit_2138],
    pdu_port=_gnb_pdu_2138.pdu_ports[3],
)

_common_unit_2137 = CommonUnit(
    lmp_connection=_lmp_connection_2137,
    capacity_units=[_capacity_unit_2137],
    pdu_port=_gnb_pdu_2137.pdu_ports[2],
)

_airscale_2139 = Airscale(common_units=[_common_unit_2139])
_airscale_2138 = Airscale(common_units=[_common_unit_2138])
_airscale_2137 = Airscale(common_units=[_common_unit_2137])

_du_2139 = DU(
    airscale=_airscale_2139,
    rus=[_ru_2139_0],
    f1_m_ip_addr="10.71.210.49",
)

_du_2138 = DU(
    airscale=_airscale_2138,
    rus=[_ru_2138_0],
    f1_m_ip_addr="10.71.210.48",
)

_du_2137 = DU(
    airscale=_airscale_2137,
    rus=[_ru_2137_0],
    f1_m_ip_addr="10.71.210.43",
)

# CU
_cu_2139 = CU(
    backhaul_site_oam_ip="10.71.210.49",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.49", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.49", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_2138 = CU(
    backhaul_site_oam_ip="10.71.210.48",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.48", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.48", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_2137 = CU(
    backhaul_site_oam_ip="10.71.210.43",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.43", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.43", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_2139 = ClassicalBts(
    dus=[_du_2139], cu=_cu_2139, instance_id=37287, global_bts_id=37287
)
_classical_bts_2138 = ClassicalBts(
    dus=[_du_2138], cu=_cu_2138, instance_id=2138, global_bts_id=37286
)
_classical_bts_2137 = ClassicalBts(
    dus=[_du_2137], cu=_cu_2137, instance_id=2137, global_bts_id=11194
)
# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.110.133.68")  # AMF
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=None,
    five_g=_real_5g_core_details,
    mcc="310",
    mnc="260",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    enbs=None,
    gnbs=[_classical_bts_2139, _classical_bts_2138, _classical_bts_2137],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=None,
    core=_realcore,
)
