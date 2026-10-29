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

__maintainer__ = "Qi Xin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "xin.qi@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.179", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_attenuator = ATTEN_HBTE(
    ip_addr="10.71.204.117",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        1,
        34,
        67,
        100,
        5,
        38,
        71,
        104,
        9,
        42,
        75,
        108,
        31,
        64,
        95,
        128,
        13,
        46,
        79,
        112,
        17,
        50,
        83,
        116,
        21,
        54,
        87,
        120,
    ],
)
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41094"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41094",
)


_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41095",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.147", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="34801d0",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx60", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    setting_network_mode_text="Preferred network type",
)
# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.71.195.228", port_numbers=[2])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.210.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_2])
_lte_ru_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=None,
    radio_type=RadioTypes.FXEB,
    serial_number="NK164601292",
    attenuation_ports=[
        _attenuator.attenuator_ports[31],
        _attenuator.attenuator_ports[64],
        _attenuator.attenuator_ports[95],
        _attenuator.attenuator_ports[128],
    ],
)
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=[_lte_ru_0], instance_id=45, global_bts_id=45
)


# 5GRU------------------------------------
_ru_pdu_047_0 = HBTE(addr="10.71.195.231", port_numbers=[1])
_ru_pdu_047_1 = HBTE(addr="10.71.195.231", port_numbers=[2])
_ru_pdu_047_2 = HBTE(addr="10.71.195.231", port_numbers=[3])
_ru_pdu_047_3 = HBTE(addr="10.71.195.231", port_numbers=[4])
_ru_pdu_047_4 = HBTE(addr="10.71.195.231", port_numbers=[5])
_ru_pdu_047_5 = HBTE(addr="10.71.195.231", port_numbers=[8])


_ru_047_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_047_0.pdu_ports[1],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0705",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[34],
        _attenuator.attenuator_ports[67],
        _attenuator.attenuator_ports[100],
    ],
)
_ru_047_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_047_1.pdu_ports[2],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2230R0065",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[38],
        _attenuator.attenuator_ports[71],
        _attenuator.attenuator_ports[104],
    ],
)

_ru_047_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_047_2.pdu_ports[3],
    radio_type=RadioTypes.AWHQN,
    serial_number="EB2230R0053",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[42],
        _attenuator.attenuator_ports[75],
        _attenuator.attenuator_ports[108],
    ],
)

_ru_047_3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_047_3.pdu_ports[4],
    radio_type=RadioTypes.AWHQN,
    serial_number="EB2230R0053",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[46],
        _attenuator.attenuator_ports[79],
        _attenuator.attenuator_ports[112],
    ],
)

_ru_047_4 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_047_4.pdu_ports[5],
    radio_type=RadioTypes.AWHQN,
    serial_number="EB2230R0053",
    attenuation_ports=[
        _attenuator.attenuator_ports[17],
        _attenuator.attenuator_ports[50],
        _attenuator.attenuator_ports[83],
        _attenuator.attenuator_ports[116],
    ],
)

_ru_047_5 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_047_5.pdu_ports[8],
    radio_type=RadioTypes.AWHQN,
    serial_number="EB2230R0053",
    attenuation_ports=[
        _attenuator.attenuator_ports[21],
        _attenuator.attenuator_ports[54],
        _attenuator.attenuator_ports[87],
        _attenuator.attenuator_ports[120],
    ],
)
# #DU
_lmp_connection_047 = SshServiceDetails(
    addr="10.71.210.234", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_047 = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.228", port_numbers=[2])
_common_unit_047 = CommonUnit(
    lmp_connection=_lmp_connection_047,
    capacity_units=[_capacity_unit_047],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale_047 = Airscale(common_units=[_common_unit_047])
_du_047 = DU(
    airscale=_airscale_047,
    rus=[_ru_047_0, _ru_047_1, _ru_047_2, _ru_047_3, _ru_047_4, _ru_047_5],
    f1_m_ip_addr="10.71.210.234",
)
# CU
_cu_047 = CU(
    backhaul_site_oam_ip="10.71.210.234",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.234", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.234", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_047 = ClassicalBts(
    dus=[_du_047], cu=_cu_047, instance_id=11434, global_bts_id=11434
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
    gnbs=[_classical_bts_047],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
