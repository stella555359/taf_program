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

__maintainer__ = "Fang ludan"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "ludan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.173", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.101.52.173",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        1, 34, 67, 100,
        5, 70,
        9, 42, 73, 106,
        11, 76,
        71, 104,
    ],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.251", username="vrf3_sg1", password="vrf3@sg1", port="41097"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.251",
    iperf_path="iperf",
    port="41098",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf_details_on_ue = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.251",
    iperf_path="/cygdrive/c/iperf",
    port="41099",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.49", username="nokia5G", password="noki@123"
    ),
    serial_number="e8307c46",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_ue,
    capabilities=["REAL_ANDROID_UE", "sdx70", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
    imsi="310260100008460",
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.101.46.42", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.170", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
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
    serial_number="EA182782353",
    attenuation_ports=[
        _attenuator.attenuator_ports[71],
        _attenuator.attenuator_ports[104],
    ],
)
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=[_lte_ru_0], instance_id=49, global_bts_id=49
)

# ------------------------------------ TL10152------------------------------------
# 5GRU------------------------------------

_ru_pdu_10152_0 = HBTE(addr="10.101.46.44", port_numbers=[2])
# _ru_pdu_10152_1 = HBTE(addr="10.101.46.44", port_numbers=[1])
# _ru_pdu_10152_2 = HBTE(addr="10.101.46.38", port_numbers=[6])
_ru_pdu_10152_1 = HBTE(addr="10.101.46.44", port_numbers=[6])
_ru_pdu_10153_0 = HBTE(addr="x.x.x.x", port_numbers=[2])
_ru_pdu_10153_1 = HBTE(addr="x.x.x.x", port_numbers=[1])

_ru_10152_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_10152_0.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    serial_number="L1211203221",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[34],
        _attenuator.attenuator_ports[67],
        _attenuator.attenuator_ports[100],
    ],
)

# _ru_10152_1 = RU(
#     ru_hw_group="Below6GHZ",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
#     pdu_port=_ru_pdu_10152_1.pdu_ports[1],
#     radio_type=RadioTypes.AHFIB,
#     serial_number="BL2043V0QPL",
#     attenuation_ports=[
#         _attenuator.attenuator_ports[69],
#         _attenuator.attenuator_ports[102],
#     ],
# )
#
# _ru_10152_2 = RU(
#     ru_hw_group="Below6GHZ",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
#     pdu_port=_ru_pdu_10152_2.pdu_ports[6],
#     radio_type=RadioTypes.AHFIB,
#     serial_number="K9183736398",
#     attenuation_ports=[
#         _attenuator.attenuator_ports[79],
#         _attenuator.attenuator_ports[112],
#     ],
# )

_ru_10152_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_10152_1.pdu_ports[6],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2034G1HNW",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[70],
    ],
)

_ru_10153_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_10153_0.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2048G1RDU",
    attenuation_ports=[
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[76],
    ],
)

_ru_10153_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_10153_1.pdu_ports[1],
    radio_type=RadioTypes.AWHHJ,
    serial_number="1M242908398",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[42],
        _attenuator.attenuator_ports[73],
        _attenuator.attenuator_ports[106],
    ],
)

# #DU
_lmp_connection_10152 = SshServiceDetails(
    addr="10.101.52.165", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_10152 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu_10152 = HBTE(addr="10.101.46.41", port_numbers=[2])

_common_unit_10152 = CommonUnit(
    lmp_connection=_lmp_connection_10152,
    capacity_units=[_capacity_unit_10152],
    pdu_port=_gnb_pdu_10152.pdu_ports[2],
)

_airscale_10152 = Airscale(common_units=[_common_unit_10152])

_du_10152 = DU(
    airscale=_airscale_10152,
    rus=[_ru_10152_0, _ru_10152_1, _ru_10153_0, _ru_10153_1],
    f1_m_ip_addr="10.101.52.165",
)

# CU
_cu_10152 = CU(
    backhaul_site_oam_ip="10.101.52.165",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.165", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.165", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_10152 = ClassicalBts(
    dus=[_du_10152], cu=_cu_10152, instance_id=10152, global_bts_id=10152
)

# ------------------------------------ TL10153------------------------------------
# 5GRU------------------------------------

# #DU
_lmp_connection_10153 = SshServiceDetails(
    addr="10.101.52.166", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_10153 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu_10153 = HBTE(addr="10.101.46.41", port_numbers=[2])

_common_unit_10153 = CommonUnit(
    lmp_connection=_lmp_connection_10153,
    capacity_units=[_capacity_unit_10153],
    pdu_port=_gnb_pdu_10153.pdu_ports[2],
)

_airscale_10153 = Airscale(common_units=[_common_unit_10153])

_du_10153 = DU(
    airscale=_airscale_10153,
    rus=[_ru_10153_0, _ru_10153_1],
    f1_m_ip_addr="10.101.52.166",
)

# CU
_cu_10153 = CU(
    backhaul_site_oam_ip="10.101.52.166",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.166", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.166", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts_10153 = ClassicalBts(
    dus=[_du_10153], cu=_cu_10153, instance_id=10153, global_bts_id=10153
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
    mcc="310",
    mnc="260",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts_10152, _classical_bts_10153],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
