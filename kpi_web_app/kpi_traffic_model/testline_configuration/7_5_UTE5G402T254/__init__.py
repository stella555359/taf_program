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
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)

__maintainer__ = "Cui Lingxue"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.182", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.101.51.210",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        145,
        178,
        211,
        244,
        149,
        214,
        157,
        222,
        153,
        218,
        151,
        184,
    ],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.179.235", username="vrf3_sg1", password="vrf3@sg1", port="41508"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.179.235",
    iperf_path="iperf",
    port="41508",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.179.235",
    iperf_path="/cygdrive/c/iperf",
    port="41509",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.97", username="mn5gran", password="nokia123@"
    ),
    serial_number="257b2356",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx70", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
    imsi="460028001006311",
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.101.45.239", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.51.212", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_ru_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=None,
    radio_type=RadioTypes.FRIJ,
    serial_number="EA181980603",
    attenuation_ports=[
        _attenuator.attenuator_ports[151],
        _attenuator.attenuator_ports[184],
    ],
)
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=[_lte_ru_0], instance_id=254, global_bts_id=254
)

# 5GRU------------------------------------

_ru_pdu_254_0 = HBTE(addr="10.101.45.246", port_numbers=[2])
_ru_pdu_254_1 = HBTE(addr="10.101.45.244", port_numbers=[2])
_ru_pdu_254_2 = HBTE(addr="10.101.45.246", port_numbers=[1])

_ru_254_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_254_0.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    serial_number="L1205002770",
    attenuation_ports=[
        _attenuator.attenuator_ports[145],
        _attenuator.attenuator_ports[178],
        _attenuator.attenuator_ports[211],
        _attenuator.attenuator_ports[244],
    ],
)
_ru_254_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_254_1.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL1828G1057",
    attenuation_ports=[
        _attenuator.attenuator_ports[157],
        _attenuator.attenuator_ports[222],
    ],
)

_ru_254_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_254_2.pdu_ports[1],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2051G1TRB",
    attenuation_ports=[
        _attenuator.attenuator_ports[149],
        _attenuator.attenuator_ports[214],
    ],
)

_ru_254_3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=None,
    radio_type=RadioTypes.AWHHH,
    serial_number="EB2218R0698",
    attenuation_ports=[
        _attenuator.attenuator_ports[153],
        _attenuator.attenuator_ports[218],
    ],
)


# #DU
_lmp_connection_254 = SshServiceDetails(
    addr="10.101.51.202", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_254 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.45.240", port_numbers=[6])

_common_unit_254 = CommonUnit(
    lmp_connection=_lmp_connection_254,
    capacity_units=[_capacity_unit_254],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale_254 = Airscale(common_units=[_common_unit_254])

_du_254 = DU(
    airscale=_airscale_254, rus=[_ru_254_0, _ru_254_1, _ru_254_2, _ru_254_3], f1_m_ip_addr="10.101.51.202"
)

# CU
_cu_254 = CU(
    backhaul_site_oam_ip="10.101.51.202",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.202", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.202", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_254 = ClassicalBts(
    dus=[_du_254], cu=_cu_254, instance_id=1170, global_bts_id=1170
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1)
_mme = MME(oam_ssh_connection_details=_mme_oam_ssh_connection_details, s1=_s1_address)
_real_4g_core_details = RealCore4GDetails(mme=_mme)

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.110.133.68")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=_real_4g_core_details,
    five_g=_real_5g_core_details,
    mcc="460",
    mnc="2",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts_254],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
