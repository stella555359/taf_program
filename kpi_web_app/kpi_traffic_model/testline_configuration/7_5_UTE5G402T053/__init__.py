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

__maintainer__ = "Fang ludan"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com>"
)
__email__ = "ludan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.151", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_topyoung_params_1 = {
    "ip_addr": "10.101.53.162",
    "port": "23",
    "attenuation_port_numbers":
        [5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117, 125, 133, 141, 149, 157, 165, 173, 181, 189,
         197, 205, 213, 221, 229, 237, 245, 253,
         6, 14, 22, 30, 38, 46, 54, 62, 70, 78, 86, 94, 102, 110, 118, 126, 134, 142, 150, 158, 166, 174, 182, 190,
         198, 206, 214, 222, 230, 238, 246, 254,
         7, 15, 23, 31, 39, 47, 55, 63, 71, 79, 87, 95, 103, 111, 119, 127, 135, 143, 151, 159, 167, 175, 183, 191,
         199, 207, 215, 223, 231, 239, 247, 255,
         8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192,
         200, 208, 216, 224, 232, 240, 248, 256],
    "model": "TAS32B8-51-120-1N-DES"
}

_attenuator = TopYoung(**_topyoung_params_1)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.154", username="vrf3_sg1", password="vrf3@sg1", port="41106"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.154",
    iperf_path="iperf",
    port="41106",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.154",
    iperf_path="/cygdrive/c/iperf",
    port="41107",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.16", username="mn5gran", password="nokia123@"
    ),
    serial_number="4acb1f05",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx65", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
    imsi="262033100001053",
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="xx.xx.xx.xx", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.185", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_ru_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=None,
    radio_type=RadioTypes.AHEH,
    serial_number="EA224156891",
)
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=[_lte_ru_0], instance_id=53, global_bts_id=53
)

# 5GRU------------------------------------
_ru_pdu_053_0 = HBTE(addr="10.101.53.163", port_numbers=[1])
_ru_pdu_053_1 = HBTE(addr="10.101.48.189", port_numbers=[2])
_ru_pdu_053_2 = HBTE(addr="10.101.53.163", port_numbers=[3])
_ru_pdu_053_3 = HBTE(addr="10.101.48.189", port_numbers=[4])
_ru_pdu_053_4 = HBTE(addr="10.101.48.189", port_numbers=[1])
_ru_pdu_053_5 = HBTE(addr="10.101.53.163", port_numbers=[2])
_ru_pdu_053_6 = HBTE(addr="10.101.53.163", port_numbers=[6])
_ru_pdu_053_7 = HBTE(addr="10.101.48.189", port_numbers=[6])
_ru_pdu_053_8 = HBTE(addr="10.101.48.171", port_numbers=[3])

_ru_53_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_0.pdu_ports[1],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2106G10IG",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[23]
    ],
)

_ru_53_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_1.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2106G10A2",
    attenuation_ports=[
        _attenuator.attenuator_ports[37],
        _attenuator.attenuator_ports[46],
        _attenuator.attenuator_ports[55],
        _attenuator.attenuator_ports[64],
    ],
)

_ru_53_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_2.pdu_ports[3],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL2307V0GVK",
    attenuation_ports=[
        _attenuator.attenuator_ports[69],
        _attenuator.attenuator_ports[78],
        _attenuator.attenuator_ports[87],
        _attenuator.attenuator_ports[96],
    ],
)

_ru_53_3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_3.pdu_ports[4],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL1923V0A8D",
    attenuation_ports=[
        _attenuator.attenuator_ports[101],
        _attenuator.attenuator_ports[110],
        _attenuator.attenuator_ports[119],
        _attenuator.attenuator_ports[128],
    ],
)

_ru_53_4 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_4.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL2120V0CXL",
    attenuation_ports=[
        _attenuator.attenuator_ports[133],
        _attenuator.attenuator_ports[142],
        _attenuator.attenuator_ports[151],
        _attenuator.attenuator_ports[160],
    ],
)

_ru_53_5 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_5.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    serial_number="L1204504876",
    attenuation_ports=[
        _attenuator.attenuator_ports[165],
        _attenuator.attenuator_ports[174],
        _attenuator.attenuator_ports[183],
        _attenuator.attenuator_ports[192],
    ],
)

_ru_53_6 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_6.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
    serial_number="L1204504876",
    attenuation_ports=[
        _attenuator.attenuator_ports[197],
        _attenuator.attenuator_ports[206],
        _attenuator.attenuator_ports[215],
        _attenuator.attenuator_ports[224],
    ],

)

_ru_53_7 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_7.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
    serial_number="L1205002750",
    attenuation_ports=[
        _attenuator.attenuator_ports[229],
        _attenuator.attenuator_ports[238],
        _attenuator.attenuator_ports[247],
        _attenuator.attenuator_ports[256],
    ],
)

_ru_53_8 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_053_8.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    serial_number="L1213413669",
)

# #DU
_lmp_connection_053 = SshServiceDetails(
    addr="10.101.48.185", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_053 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.48.190", port_numbers=[8])

_common_unit_53 = CommonUnit(
    lmp_connection=_lmp_connection_053,
    capacity_units=[_capacity_unit_053],
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale_53 = Airscale(common_units=[_common_unit_53])

_du_53 = DU(airscale=_airscale_53, rus=[_ru_53_0, _ru_53_1, _ru_53_2, _ru_53_3, _ru_53_4, _ru_53_5, _ru_53_6, _ru_53_7, _ru_53_8], f1_m_ip_addr="10.101.48.185")

# CU
_cu_053 = CU(
    backhaul_site_oam_ip="10.101.48.185",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.185", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.185", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_053 = ClassicalBts(
    dus=[_du_53], cu=_cu_053, instance_id=53, global_bts_id=10391
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
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts_053],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
