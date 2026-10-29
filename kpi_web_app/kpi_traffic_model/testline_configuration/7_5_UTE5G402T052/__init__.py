import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
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

from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid
__maintainer__ = "Wu Rong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "rong.2.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.172", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.57.179.235",
    user="vrf3_sg1",
    password="vrf3@sg1",
    ports=[41105, 41104],
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="wap2.nokia.com", apnName="wap2.nokia.com", apnType=["DEFAULT"]
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
#    interface_name="rmnet_data2",
    server_close_delay=50,
)

_android_0 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.138", username="mn5gran", password="nokia123@"
    ),
    serial_number="7d38a4d4",
    capabilities=["REAL_ANDROID_UE", "sdx60", "qualcomm"],
    ue_pc_address="10.68.86.138",
    data_transfer=[_data_transfer_iperf],
    ue_pc_port="8080",# Note, default 443 or 80 are not acceptable for Debian
    imei="351602006210031",
    imsi="310260100010204",
    pdns=[_pdn1],
    service_call_attach="123",  #default
    service_call_detach="124", #default
    qualcomm_prototype=True,
    network_mode_switch_method="keyevents",
    airplane_mode_switcher_text='Airplane mode', #OPTIONAL Text next to switcher turning airplane mode on or off; essential for attemp to attach with key events;
    airplane_mode_confirm_button_text='OK',
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.101.46.42", port_numbers=[6])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.180", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=10275, global_bts_id=10275
)

## TL52-1,TL52-2
# 5GRU------------------------------------
_ru_pdu_52_1_0 = HBTE(addr="10.101.46.44", port_numbers=[5])  # AEHC
_ru_pdu_52_2_0 = HBTE(addr="10.101.46.38", port_numbers=[1])  # AEHC

_ru_52_1_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_52_1_0.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    serial_number="L1212614395",
    attenuation_ports=None,
)

_ru_52_2_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_52_2_0.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    serial_number="K9220328049",
    attenuation_ports=None,
)


# #DU
_lmp_connection_52_1 = SshServiceDetails(
    addr="10.101.52.164", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_52_2 = SshServiceDetails(
    addr="10.101.52.178", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_52 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.46.44", port_numbers=[5])

_common_unit_52_1 = CommonUnit(
    lmp_connection=_lmp_connection_52_1,
    capacity_units=[_capacity_unit_52],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_common_unit_52_2 = CommonUnit(
    lmp_connection=_lmp_connection_52_2,
    capacity_units=[_capacity_unit_52],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale_52_1 = Airscale(common_units=[_common_unit_52_1])
_airscale_52_2 = Airscale(common_units=[_common_unit_52_2])

_du_52_1 = DU(airscale=_airscale_52_1, rus=[_ru_52_1_0], f1_m_ip_addr="10.101.52.164")
_du_52_2 = DU(airscale=_airscale_52_2, rus=[_ru_52_2_0], f1_m_ip_addr="10.101.52.178")

# CU
_cu_52_1 = CU(
    backhaul_site_oam_ip="10.101.52.164",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.164", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.164", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_52_2 = CU(
    backhaul_site_oam_ip="10.101.52.178",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.178", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.178", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_52_1 = ClassicalBts(
    dus=[_du_52_1], cu=_cu_52_1, instance_id=10151, global_bts_id=10151
)

_classical_bts_52_2 = ClassicalBts(
    dus=[_du_52_2], cu=_cu_52_2, instance_id=10359, global_bts_id=10359
)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="10.108.225.167", v6="xxx:xx::xxx", vlan_id=1)
_mme = MME(oam_ssh_connection_details=_mme_oam_ssh_connection_details, s1=_s1_address)
_real_4g_core_details = RealCore4GDetails(mme=_mme)

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.107.180.5")
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
    enbs=None,
    gnbs=[_classical_bts_52_2, _classical_bts_52_1],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    # attenuators=[_attenuator],
    core=_realcore,
)
