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
from taf.config.testline import Mitron

__maintainer__ = "Yu Lu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "lu.1.yu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_optical_switch = Mitron(addr="10.57.231.115", model="OXC1000-32X32-SM-1356-DD-50-LP")

_optical_switch_1 = Mitron(addr="10.57.231.116", model="OXC1000-32X32-SM-1356-DD-50-LP")

_optical_switch_2 = Mitron(addr="10.57.231.117", model="OXC1000-32X32-SM-1356-DD-50-LP")

_optical_switch_3 = Mitron(addr="10.57.231.118", model="OXC1000-32X32-SM-1356-DD-50-LP")

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.140", username="ute", password="ute"
    )
)

# CI_Detail_UE_Type='Huawei'

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.236", username="vrf4_sg2", password="VERIFICATION@sg2"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="/usr/bin/iperf",
    port=52529,
)

_huawei_host_ssh = SshServiceDetails(
    addr="10.57.130.102", username="MN5GRAN", password="nokia123@"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_huawei_host_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52529,
)


_appserver = AppServer(iperf_details)


_huawei_pdu = HBTE(addr="1.1.1.1", port_numbers=[2]).pdu_ports[2]

_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.102", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9EQUT20903003324",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Huawei"],
)

_huawei.pdu = _huawei_pdu

# #5GRU for classicalBTS AEHB
_ru1_pdu = HBTE(addr="10.57.242.57", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.242.140", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
)

# #5GRU for classicalBTS AHPF
_ru2_pdu = HBTE(addr="10.57.172.96", port_numbers=[6])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.242.140", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHPF,
)

# #BU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.228", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.242.43", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.57.223.228")

# #CU
_cu = CU(
    backhaul_site_oam_ip="110.57.223.228",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.228", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id="20529", instance_id="20529"
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    ues=[_huawei],
    optical_switches=[
        _optical_switch,
        _optical_switch_1,
        _optical_switch_2,
        _optical_switch_3,
    ],
)
