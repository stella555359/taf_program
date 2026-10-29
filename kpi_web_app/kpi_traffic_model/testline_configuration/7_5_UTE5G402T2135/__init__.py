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
__maintainer__ = "journey.jin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "journey.jin@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.176", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_2",
    address="10.57.191.251",
    user="vrf3_sg1",
    password="vrf3@sg1",
    ports=[41670, 41671],
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata1", apnName="dxdata1", apnType=["DEFAULT"]
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
        addr="10.68.86.88", username="mn5gran", password="nokia123@"
    ),
    serial_number="6ee8000c",
    capabilities=["REAL_ANDROID_UE", "sdx60", "qualcomm"],
    ue_pc_address="10.68.86.88",
    data_transfer=[_data_transfer_iperf],
    ue_pc_port="8080",# Note, default 443 or 80 are not acceptable for Debian
    imei="004403160842144",
    imsi="001010100009310",
    pdns=[_pdn1],
    service_call_attach="123",  #default
    service_call_detach="124", #default
    qualcomm_prototype=True,
    network_mode_switch_method="keyevents",
    airplane_mode_switcher_text='Airplane mode', #OPTIONAL Text next to switcher turning airplane mode on or off; essential for attemp to attach with key events;
    airplane_mode_confirm_button_text='OK',
)


# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.101.45.240", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.180", username="toor4nsn", password="oZPS0POrRieRtu"
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
    radio_type=RadioTypes.AHFB,
    serial_number="EA184413443",
)
_lte_real_enb = []

# 5GRU------------------------------------
_ru_pdu_420_0 = HBTE(addr="10.101.45.246", port_numbers=[1])
_ru_pdu_420_1 = HBTE(addr="10.101.45.246", port_numbers=[4])
_ru_pdu_420_2 = HBTE(addr="10.101.45.246", port_numbers=[5])
_ru_pdu_420_3 = HBTE(addr="10.101.45.244", port_numbers=[5])

_ru_420_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_420_0.pdu_ports[1],
    radio_type=RadioTypes.AQQY,
    serial_number="1M220739537",
)

_ru_51_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_420_0.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
    serial_number="1M201202391",
)

# #DU
_lmp_connection_420 = SshServiceDetails(
    addr="10.101.52.186", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_51 = SshServiceDetails(
    addr="10.101.52.185", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_420 = CapacityUnit(addr="192.168.253.20")

_capacity_unit_51 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.45.240", port_numbers=[1])

_common_unit_420 = CommonUnit(
    lmp_connection=_lmp_connection_420,
    capacity_units=[_capacity_unit_420],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_common_unit_51 = CommonUnit(
    lmp_connection=_lmp_connection_51,
    capacity_units=[_capacity_unit_51],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale_420 = Airscale(common_units=[_common_unit_420])

_airscale_51 = Airscale(common_units=[_common_unit_51])

_du_420 = DU(
    airscale=_airscale_420, rus=[_ru_420_0], f1_m_ip_addr="10.101.52.186"
)

_du_51 = DU(
    airscale=_airscale_51, rus=[_ru_51_0], f1_m_ip_addr="10.101.52.185"
)

_cu_420 = CU(
    backhaul_site_oam_ip="10.101.52.186",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.186", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.186", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_51 = CU(
    backhaul_site_oam_ip="10.101.52.185",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.185", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.185", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_420 = ClassicalBts(
    dus=[_du_420], cu=_cu_420, instance_id=4294967184, global_bts_id=4294967184
)

_classical_bts_51 = ClassicalBts(
    dus=[_du_51], cu=_cu_51, instance_id=37284, global_bts_id=37284
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
    mcc="1",
    mnc="1",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts_420, _classical_bts_51],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    core=_realcore,
)
