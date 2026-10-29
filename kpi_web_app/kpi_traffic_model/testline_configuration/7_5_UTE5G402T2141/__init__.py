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
        addr="10.57.157.26", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41683"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41683",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41682",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.59", username="nokia5G", password="noki@123"
    ),
    serial_number="3839aaac",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
)
# TL2141
# 5GRU------------------------------------
# RU1 AEHC
_ru_pdu_2142_0 = HBTE(addr="10.57.172.197", port_numbers=[4])
_ru_pdu_2141_0 = HBTE(addr="10.57.172.199", port_numbers=[3])
_ru_pdu_2140_0 = HBTE(addr="10.57.172.199", port_numbers=[4])

_ru_2142_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_2142_0.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    serial_number="L1211609178",
)
_ru_2141_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_2141_0.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    serial_number="L1211609178",
)
_ru_2140_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_2140_0.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    serial_number="K9220312567",
)


# DU
_lmp_connection_2142 = SshServiceDetails(
    addr="10.57.225.39", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_2141 = SshServiceDetails(
    addr="10.57.225.36", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_2140 = SshServiceDetails(
    addr="10.57.225.35", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit_2142 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_2141 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_2140 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu_2142 = HBTE(addr="10.57.172.199", port_numbers=[5])
_gnb_pdu_2141 = HBTE(addr="10.57.172.198", port_numbers=[5])
_gnb_pdu_2140 = HBTE(addr="10.57.172.198", port_numbers=[1])

_common_unit_2142 = CommonUnit(
    lmp_connection=_lmp_connection_2142,
    capacity_units=[_capacity_unit_2142],
    pdu_port=_gnb_pdu_2142.pdu_ports[5],
)

_common_unit_2141 = CommonUnit(
    lmp_connection=_lmp_connection_2141,
    capacity_units=[_capacity_unit_2141],
    pdu_port=_gnb_pdu_2141.pdu_ports[5],
)

_common_unit_2140 = CommonUnit(
    lmp_connection=_lmp_connection_2140,
    capacity_units=[_capacity_unit_2140],
    pdu_port=_gnb_pdu_2140.pdu_ports[1],
)

_airscale_2142 = Airscale(common_units=[_common_unit_2142])
_airscale_2141 = Airscale(common_units=[_common_unit_2141])
_airscale_2140 = Airscale(common_units=[_common_unit_2140])

_du_2142 = DU(
    airscale=_airscale_2142,
    rus=[_ru_2142_0],
    f1_m_ip_addr="10.57.225.39",
)

_du_2141 = DU(
    airscale=_airscale_2141,
    rus=[_ru_2141_0],
    f1_m_ip_addr="10.57.225.36",
)

_du_2140 = DU(
    airscale=_airscale_2140,
    rus=[_ru_2140_0],
    f1_m_ip_addr="10.57.225.35",
)

# CU
_cu_2142 = CU(
    backhaul_site_oam_ip="10.57.225.39",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.39", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.39", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_2141 = CU(
    backhaul_site_oam_ip="10.57.225.36",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.36", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_2140 = CU(
    backhaul_site_oam_ip="10.57.225.35",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.35", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.35", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_2142 = ClassicalBts(
    dus=[_du_2142], cu=_cu_2142, instance_id=2142, global_bts_id=2142
)
_classical_bts_2141 = ClassicalBts(
    dus=[_du_2141], cu=_cu_2141, instance_id=2141, global_bts_id=37288
)
_classical_bts_2140 = ClassicalBts(
    dus=[_du_2140], cu=_cu_2140, instance_id=2140, global_bts_id=10063
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
    gnbs=[_classical_bts_2141, _classical_bts_2140, _classical_bts_2142],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=None,
    core=_realcore,
)
