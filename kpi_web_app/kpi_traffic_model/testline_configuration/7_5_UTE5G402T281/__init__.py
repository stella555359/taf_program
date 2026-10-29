import os
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
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline import LicenseKeeper
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


__maintainer__ = "Hao Xiaoxia"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xiaoxia.haonokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.161", username="vrf4_sg6", password="vrf4@sg6", port="56281"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/data/local/tmp/iperf",
    port="56381",
)

_appserver = AppServer(_iperf)
# CI_Detail_UE_Type='MTK'
_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.221", username="nokia5G", password="noki@123"
)

_ue_host_ssh_1 = SshServiceDetails(
    addr="10.0.176.3", username="mn5gran", password="nokia123@"
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="262033100010706",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)
_ue_pdu = pdu_TopYoung(addr="1.1.1.1", port_numbers=[1])
# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.156", username="mn5gran", password="nokia123@"
    ),
    serial_number="d8454996",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
    pdu_port=_ue_pdu.pdu_ports[1],
)

# RealEnb
_real_enb_pdu = HBTE(addr="1.1.1.1", port_numbers=[1])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.213.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU for classicalBTS
_ru_0_pdu = pdu_TopYoung(addr="10.71.196.136", port_numbers=[4])
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
    pdu_port=_ru_0_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
)

_ru_1_pdu = HBTE(addr="10.71.196.140", port_numbers=[6])
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
    pdu_port=_ru_1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
)

_ru_2_pdu = HBTE(addr="10.71.196.142", port_numbers=[6])
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
    pdu_port=_ru_2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_gnb_pdu = HBTE(addr="10.71.196.144", port_numbers=[3])

_capacity_unit1 = CapacityUnit(
    addr="172.22.48.2",
    hardware_type="ABIO",
)
_capacity_unit2 = CapacityUnit(
    addr="172.22.48.18",
    hardware_type="ABIO",
)
# _capacity_unit3 = CapacityUnit(addr="172.22.48.10")


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASIL",
)


_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2],
    f1_m_ip_addr="192.168.255.129",
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.213.39",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.39", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.39", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.213.39",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.213.39",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.33", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.213.39",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.33", ip_prefix_length=27),
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=281, global_bts_id=281)

# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.39", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASILL_ABIOB1B2_3xAEHC_CMA"

tl = TestLine(
    test_pc=_test_pc,
    # test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    ues=[_android],
    core=RealCore(mcc=460, mnc=2),  # Use RealCore() for Real Core TL
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
