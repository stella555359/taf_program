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
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    RealEnb,
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
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)

__maintainer__ = "Lingxue Cui"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.137", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41826"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41827",
)

_appserver = AppServer(_iperf_details_on_appserver)

# UE
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41826",
)

# tbd
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.210.42", username="nokia5G", password="noki@123"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "mtk"],
)


# 5GRU------------------------------------
# RU1 AHFIB FDD
_ru1_pdu_gnb = HBTE(addr="10.71.195.176", port_numbers=[2])
_ru2_pdu_gnb = HBTE(addr="10.71.195.178", port_numbers=[1])
_ru3_pdu_gnb = HBTE(addr="10.71.195.176", port_numbers=[6])
_ru4_pdu_gnb = HBTE(addr="10.71.195.176", port_numbers=[3])
_ru5_pdu_gnb = HBTE(addr="10.71.195.170", port_numbers=[3])

_ru1_gnb = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu_gnb.pdu_ports[2],
    radio_type=RadioTypes.AHPB,
    serial_number="EA204457541",
)
_ru2_gnb = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru2_pdu_gnb.pdu_ports[1],
    radio_type=RadioTypes.AHEGA,
    serial_number="EA205152441",
)
_ru3_gnb = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru3_pdu_gnb.pdu_ports[6],
    radio_type=RadioTypes.AHEH,
    serial_number="EA194550620",
)

_ru4_gnb = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru4_pdu_gnb.pdu_ports[3],
    radio_type=RadioTypes.AEQY,
    serial_number="1M220200007",
)

_ru5_gnb = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru5_pdu_gnb.pdu_ports[3],
    radio_type=RadioTypes.AEQP,
    serial_number="1M215206913",
)

# DU
_lmp_connection_gnb = SshServiceDetails(
    addr="10.71.210.42", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_gnb = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.71.195.172", port_numbers=[3])

_common_unit_gnb = CommonUnit(
    lmp_connection=_lmp_connection_gnb,
    capacity_units=[_capacity_unit_gnb],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale_gnb = Airscale(common_units=[_common_unit_gnb])

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru1_gnb, _ru2_gnb, _ru3_gnb, _ru4_gnb, _ru5_gnb],
    f1_m_ip_addr="10.71.210.42",
)

# CU
_cu_gnb = CU(
    backhaul_site_oam_ip="10.71.210.42",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.42", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.42", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_gnb = ClassicalBts(
    dus=[_du_gnb], cu=_cu_gnb, instance_id=413, global_bts_id=11171
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
_n2_address = NetworkAddress(v4="10.110.66.198")  # AMF
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
    gnbs=[_classical_bts_gnb],
    ues=[_android],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    core=_realcore,
)
