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
__maintainer__ = "Dandan Fang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "dandan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]



_attenuator = ATTEN_HBTE(
    ip_addr="10.57.239.22",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[1, 34, 67, 100, 5, 38, 71, 104, 9, 42, 75, 108],
)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_2",
    address="10.57.191.251",
    user="vrf3_sg1",
    password="vrf3@sg1",
    ports=[41640, 41641],
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

# UE info
# 2933e1ab is sdx75    9b77be8a is sdx85, which move to tl419
_android_0 = TafUeAndroid(
    serial_number="2933e1ab",
    capabilities=["REAL_ANDROID_UE", "sdx85", "qualcomm"],
    ue_pc_address="10.57.130.135",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.135", username="MN5GRAN", password="nokia123@"
    ),
    ue_pc_port="8080",# Note, default 443 or 80 are not acceptable for Debian
    imei="004403162455564",
    imsi="262038001006015",
    pdns=[_pdn1],
    service_call_attach="123",  #default
    service_call_detach="124", #default
    qualcomm_prototype=True,
    network_mode_switch_method="keyevents",
    airplane_mode_switcher_text='Airplane mode', #OPTIONAL Text next to switcher turning airplane mode on or off; essential for attemp to attach with key events;
    airplane_mode_confirm_button_text='OK',
)
              
# Note: RMOD index should be matched with SCF 
# 5GRU need to update------------------------------------
_ru_pdu_AVQD_1 = HBTE(addr="10.57.172.197", port_numbers=[4])


_ru_AVQD_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.30", 
        username="serviceuser", 
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_AVQD_1.pdu_ports[4],
    radio_type=RadioTypes.AVQD,
    serial_number="1M242005847",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[34],
        _attenuator.attenuator_ports[67],
        _attenuator.attenuator_ports[100],
    ],
)

_ru_pdu_AVQA_2 = HBTE(addr="10.57.172.199", port_numbers=[1])


_ru_AVQA_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.30", 
        username="serviceuser", 
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_AVQA_2.pdu_ports[1],
    radio_type=RadioTypes.AVQA,
    serial_number="L1251400642",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[38],
        _attenuator.attenuator_ports[71],
        _attenuator.attenuator_ports[104],
    ],
)

_ru_pdu_AVQF_3 = HBTE(addr="10.57.172.197", port_numbers=[5])

#RadioTypes need to support AVQF, current for pipe issue , type with AVQA first.
_ru_AVQF_3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.30", 
        username="serviceuser", 
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_AVQF_3.pdu_ports[5],
    radio_type=RadioTypes.AVQA,
    serial_number="1M251103764",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[42],
        _attenuator.attenuator_ports[75],
        _attenuator.attenuator_ports[108],
    ],
)

# #DU
_lmp_connection_2120 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1_2120 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP", rus=[_ru_AVQF_3, _ru_AVQD_1])
_capacity_unit_2_2120 = CapacityUnit(addr="192.168.253.24", hardware_type="ABIP", rus=[_ru_AVQA_2])

_gnb_pdu = HBTE(addr="10.57.172.198", port_numbers=[8])

_common_unit_2120 = CommonUnit(
    lmp_connection=_lmp_connection_2120,
    capacity_units=[_capacity_unit_1_2120, _capacity_unit_2_2120],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIM",
)

_airscale_2120 = Airscale(common_units=[_common_unit_2120])

_du_2120 = DU(airscale=_airscale_2120, rus=[_ru_AVQD_1, _ru_AVQA_2, _ru_AVQF_3], f1_m_ip_addr="10.57.225.3")

# CU
_cu_2120 = CU(
    backhaul_site_oam_ip="10.57.225.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.3", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_2120 = ClassicalBts(
    dus=[_du_2120], cu=_cu_2120, instance_id=4294967183, global_bts_id=4294967183
)


# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.68", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(interface="eth1", device=_classical_bts_2120.dus[0].airscale.common_units[0], interface_type="lmp")
    ],
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
_n2_address = NetworkAddress(v4="10.107.180.5")
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
    gnbs=[_classical_bts_2120],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    core=_realcore,
    attenuators=[_attenuator]
)
