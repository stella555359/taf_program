import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline import TopYoung_PDU
from taf.config.testline import HBTE_PDU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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
    MediaTek,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Li Liyu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "liyu.li@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.165", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.153", username="vrf4_sg6", password="vrf4@sg6", port="56079"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.153",
    iperf_path="/cygdrive/c",
    port="56979",
)

_appserver = AppServer(_iperf)

# MTK SA
_ue_host_ssh = SshServiceDetails(
    addr="10.57.150.160", username="mn5gran", password="nokia123@"
)

_mtk_sa = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="262033032994018",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="0123456789ABCDEF",
)

# MTK NSA
# _ue_host_ssh = SshServiceDetails(
#     addr="10.57.130.245", username="nokia5G", password="noki@123"
# )
# _mtk_nsa = MediaTek(
#     ssh_connection_details=_ue_host_ssh,
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     edb_file_path="auto",
#     imei="0123456789ABCDEF",
#     imsi="262033100009144",
#     apn_url="wap2.nokia.com",
#     iperf_details=_iperf,
#     capabilities=["REAL_MEDIATEK_UE2", "mtk"],
#     serial_number="0123456789ABCDEF",
# )

# #5GRU for classicalBTS
# attenuator
_attenuator1 = HBTE(
    ip_addr="10.57.156.51",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator2 = HBTE(
    ip_addr="10.57.156.52",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# #5GRU for classicalBTS
_ru1_pdu = FACOM(addr="10.57.172.21", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.57.172.22", port_numbers=[3])
_ru3_pdu = FACOM(addr="10.57.172.32", port_numbers=[4])
_ru4_pdu = FACOM(addr="10.57.172.22", port_numbers=[1])
_ru5_pdu = FACOM(addr="10.57.172.32", port_numbers=[3])
_ru6_pdu = FACOM(addr="10.57.172.22", port_numbers=[2])
_ru7_pdu = FACOM(addr="10.57.172.32", port_numbers=[5])
_ru8_pdu = FACOM(addr="10.57.172.32", port_numbers=[2])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
    serial_number="K9220312559",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
    serial_number="L1213713058",
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQK,
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
    serial_number="DH214500024",
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHLOA,
    attenuation_ports=[
        _attenuator2.attenuator_ports[1],
        _attenuator2.attenuator_ports[2],
    ],
    serial_number="K9182017415",
)

_ru5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator2.attenuator_ports[9],
        _attenuator2.attenuator_ports[10],
        _attenuator2.attenuator_ports[11],
        _attenuator2.attenuator_ports[12],
    ],
    serial_number="BL2215V01FD",
)

_ru6 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru6_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    attenuation_ports=[
        _attenuator2.attenuator_ports[5],
        _attenuator2.attenuator_ports[6],
    ],
    serial_number="BL2235G14FC",
)

_ru7 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru7_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator2.attenuator_ports[13],
        _attenuator2.attenuator_ports[14],
        _attenuator2.attenuator_ports[15],
        _attenuator2.attenuator_ports[16],
    ],
    serial_number="BL2147V0RJ5",
)

_ru8 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru8_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQK,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
    serial_number="1M204306419",
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.57.172.22", port_numbers=[5])


_common_unit_3 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.223.110", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_common_unit_4 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.223.111", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb_0 = Airscale(common_units=[_common_unit_3])
_real_enb_1 = Airscale(common_units=[_common_unit_4])

_lte_real_enb_0 = RealEnb(airscale=_real_enb_0, rms=None)
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=None)


# #DU for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.223.112", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.57.223.113", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")

_gnb_0_pdu = FACOM(addr="10.57.172.22", port_numbers=[4])
_gnb_1_pdu = FACOM(addr="10.57.172.21", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_0_pdu.pdu_ports[4],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_1_pdu.pdu_ports[6],
)

_airscale_0 = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_1])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7],
    f1_m_ip_addr="10.57.223.112",
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru8],
    f1_m_ip_addr="10.57.223.113",
)

# #CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu_0 = CU(
    backhaul_site_oam_ip="10.57.223.112",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.112", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.112", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.57.223.113",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.113", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.113", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

# classicalbts
_classical_bts_0 = ClassicalBts(dus=[_du_0], cu=_cu_0, instance_id=79, global_bts_id=79)
_classical_bts_1 = ClassicalBts(dus=[_du_1], cu=_cu_1, instance_id=78, global_bts_id=78)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0, _classical_bts_1],
    enbs=[_lte_real_enb_0, _lte_real_enb_1],
    ues=[_mtk_sa],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=[_attenuator1, _attenuator2],
    appserver=_appserver,
)
