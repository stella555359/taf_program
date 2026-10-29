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
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41504"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41505",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41104",
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
# TL252
# 5GRU------------------------------------
# RU1 AEHC
_ru_pdu_252_0 = HBTE(addr="10.57.172.199", port_numbers=[3])
_ru_pdu_409_0 = HBTE(addr="10.57.172.199", port_numbers=[4])

_ru_252_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_252_0.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    serial_number="L1211609178",
)
_ru_409_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_409_0.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    serial_number="K9220312567",
)


# DU
_lmp_connection_252 = SshServiceDetails(
    addr="10.57.225.36", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_409 = SshServiceDetails(
    addr="10.57.225.35", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit_252 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_409 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu_252 = HBTE(addr="10.57.172.198", port_numbers=[5])
_gnb_pdu_409 = HBTE(addr="10.57.172.198", port_numbers=[1])

_common_unit_252 = CommonUnit(
    lmp_connection=_lmp_connection_252,
    capacity_units=[_capacity_unit_252],
    pdu_port=_gnb_pdu_252.pdu_ports[5],
)

_common_unit_409 = CommonUnit(
    lmp_connection=_lmp_connection_409,
    capacity_units=[_capacity_unit_409],
    pdu_port=_gnb_pdu_409.pdu_ports[1],
)

_airscale_252 = Airscale(common_units=[_common_unit_252])
_airscale_409 = Airscale(common_units=[_common_unit_409])

_du_252 = DU(
    airscale=_airscale_252,
    rus=[_ru_252_0],
    f1_m_ip_addr="10.57.225.36",
)

_du_409 = DU(
    airscale=_airscale_409,
    rus=[_ru_409_0],
    f1_m_ip_addr="10.57.225.35",
)

# CU
_cu_252 = CU(
    backhaul_site_oam_ip="10.57.225.36",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.36", username="Nemuadmin", password="nemuuser"
    ),
)
_cu_409 = CU(
    backhaul_site_oam_ip="10.57.225.35",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.35", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.35", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_252 = ClassicalBts(
    dus=[_du_252], cu=_cu_252, instance_id=252, global_bts_id=252
)
_classical_bts_409 = ClassicalBts(
    dus=[_du_409], cu=_cu_409, instance_id=409, global_bts_id=10063
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
    gnbs=[_classical_bts_252, _classical_bts_409],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=None,
    core=_realcore,
)
