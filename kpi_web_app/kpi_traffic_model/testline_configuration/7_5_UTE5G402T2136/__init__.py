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
        addr="10.57.157.174", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.***.**.**",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[5, 70, 1, 34, 67, 100, 13, 78, 73, 106, 71, 104],
)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.55", username="mmw_sg1", password="mm@1", port="41510"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.55",
    iperf_path="iperf",
    port="41372",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.55",
    iperf_path="/cygdrive/c/iperf",
    port="41373",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.236", username="mn5gran", password="nokia123@"
    ),
    serial_number="b44517aa",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/MN5GRAN/AppData/Local/Programs/Python/Python39/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx60", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
    imsi="262033100010099",
)

# RealEnb---------------------------------------------------------
# _real_enb_pdu = HBTE(addr="10.***.**.**", port_numbers=[1])
#
# _common_unit_2 = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.101.**.**", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     capacity_units=[],
#     pdu_port=_real_enb_pdu.pdu_ports[1],
# )
#
# _real_enb = Airscale(common_units=[_common_unit_2])
# _lte_ru_0 = RU(
#     ru_hw_group="Below6GHZ",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
#     pdu_port=None,
#     radio_type=RadioTypes.FRIJ,
#     serial_number="EA184174400",
#     attenuation_ports=[
#         _attenuator.attenuator_ports[71],
#         _attenuator.attenuator_ports[104],
#     ],
# )
# _lte_real_enb = RealEnb(
#     airscale=_real_enb, rms=[_lte_ru_0], instance_id=943, global_bts_id=943
# )

# 5GRU------------------------------------
_ru_pdu_943_0 = HBTE(addr="10.**.**.**", port_numbers=[1])
# _ru_pdu_255_1 = HBTE(addr="10.101.45.246", port_numbers=[4])
# _ru_pdu_255_2 = HBTE(addr="10.101.45.246", port_numbers=[5])
# _ru_pdu_255_3 = HBTE(addr="10.101.45.244", port_numbers=[5])

_ru_943_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_943_0.pdu_ports[1],
    radio_type=RadioTypes.AQQK,
    serial_number="L1220104695",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[34],
        _attenuator.attenuator_ports[67],
        _attenuator.attenuator_ports[100],
    ],
)

# _ru_255_1 = RU(
#     ru_hw_group="Below6GHZ",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
#     pdu_port=_ru_pdu_255_1.pdu_ports[4],
#     radio_type=RadioTypes.AHLOA,
#     serial_number="BL2034G1HI5",
#     attenuation_ports=[
#         _attenuator.attenuator_ports[5],
#         _attenuator.attenuator_ports[70],
#     ],
# )
#
# _ru_255_2 = RU(
#     ru_hw_group="Below6GHZ",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
#     pdu_port=_ru_pdu_255_2.pdu_ports[5],
#     radio_type=RadioTypes.AHLOA,
#     serial_number="BL2034G1HHW",
#     attenuation_ports=[
#         _attenuator.attenuator_ports[13],
#         _attenuator.attenuator_ports[78],
#     ],
# )
#
# _ru_255_3 = RU(
#     ru_hw_group="Below6GHZ",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
#     pdu_port=_ru_pdu_255_3.pdu_ports[5],
#     radio_type=RadioTypes.AWHHJ,
#     serial_number="1M242106970",
#     attenuation_ports=[
#         _attenuator.attenuator_ports[73],
#         _attenuator.attenuator_ports[106],
#     ],
# )

# #DU
_lmp_connection_943 = SshServiceDetails(
    addr="10.57.246.187", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_943 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.**.**", port_numbers=[1])

_common_unit_943 = CommonUnit(
    lmp_connection=_lmp_connection_943,
    capacity_units=[_capacity_unit_943],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale_943 = Airscale(common_units=[_common_unit_943])

_du_943 = DU(
    airscale=_airscale_943, rus=[_ru_943_0], f1_m_ip_addr="10.57.246.187"
)

# CU
_cu_943 = CU(
    backhaul_site_oam_ip="10.57.246.187",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.246.187", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.246.187", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_943 = ClassicalBts(
    dus=[_du_943], cu=_cu_943, instance_id=943, global_bts_id=11621
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
    mcc="262",
    mnc="3",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    # enbs=[_lte_real_enb],
    gnbs=[_classical_bts_943],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
