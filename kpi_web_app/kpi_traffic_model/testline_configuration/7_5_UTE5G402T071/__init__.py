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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
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
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer


__maintainer__ = "Hao Xiaoxia"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xiaoxia.hao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.30", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.237", username="vrf4_sg6", password="Nokia@1234567", port="56071"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/opt/app/iperf",
    port="56171",
)
_ue_pdu = pdu_HBTE(addr="1.1.1.1", port_numbers=[1])

# CI_Detail_UE_Type='Qualcomm;Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
    addr="10.57.130.207", username="mn5gran", password="nokia123@"
    ),
    serial_number="962be702",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
    pdu_port=_ue_pdu.pdu_ports[1],
)

# #RealEnb
_attenuator_0 = HBTE(
    ip_addr="10.57.156.68",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
_real_enb_pdu = pdu_HBTE(addr="10.57.172.18", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.223.81", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU for classicalBTS
_ru_0_pdu = pdu_HBTE(addr="10.57.172.26", port_numbers=[2])
_ru_0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="root",
        password="umniedziala",
    ),
    pdu_port=_ru_0_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHHI,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[14],
        _attenuator_0.attenuator_ports[15],
        _attenuator_0.attenuator_ports[16],
    ],
)

_ru_1_pdu = pdu_HBTE(addr="10.57.172.26", port_numbers=[3])
_ru_1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.6",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="root",
        password="umniedziala",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHHI,
)

_ru_2_pdu = pdu_HBTE(addr="10.57.172.26", port_numbers=[4])
_ru_2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.10",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="root",
        password="umniedziala",
    ),
    pdu_port=_ru_2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWHHI,
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.80", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = pdu_HBTE(addr="10.57.172.17", port_numbers=[3])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2],
    f1_m_ip_addr="10.57.223.80",
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.223.80",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.80", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.80", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.223.80",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.223.80",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.223.80",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.65", ip_prefix_length=27),
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=71, global_bts_id=71)

_tl_cloud_topology = "AWHHI"

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    #    ues=[_android_sa, _android_nsa],
    #    enbs=[_lte_real_enb],
    ues=[_android],
#    core=RealCore(mcc=460, mnc=2),  # Use RealCore() for Real Core TL
    tl_cloud_topology=_tl_cloud_topology,
#    appserver=_appserver,
    attenuators=[_attenuator_0],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
