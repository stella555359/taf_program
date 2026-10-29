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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.gnb.du import Cablink, Endpoint
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
from taf.config.testline.attenuator import AttenuationPort
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

__maintainer__ = "Dandan Fang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "dandan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.194", username="vrf3_sg1", password="vrf3@sg1", port="41642"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="iperf",
    port="41642",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="/cygdrive/c/iperf",
    port="41643",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.190", username="mn5gran", password="nokia123@"
    ),
    serial_number="dd36afed",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/MN5GRAN/AppData/Local/Programs/Python/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx65", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# RealEnb---------------------------------------------------------

# 5GRU------------------------------------
_ru_pdu_AVQQ = HBTE(addr="10.57.241.138", port_numbers=[8])

_ru_AVQQ = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_AVQQ.pdu_ports[8],
    radio_type=RadioTypes.AVQQ.value,
    serial_number="1M242506311"
)

_ru_pdu_AQQF = HBTE(addr="10.57.172.199", port_numbers=[2])

_ru_AQQF = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.2", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_AQQF.pdu_ports[2],
    radio_type=RadioTypes.AQQF.value,
    serial_number="1M232010514"
)

# #DU
_lmp_connection_2121 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1_2121 = CapacityUnit(addr="192.168.253.36", hardware_type="ABIP", rus=[_ru_AVQQ])
_capacity_unit_2_2121 = CapacityUnit(addr="192.168.253.40", hardware_type="ABIO", rus=[_ru_AQQF])
_capacity_unit_3_2121 = CapacityUnit(addr="192.168.253.44", hardware_type="ABIP")
_gnb_pdu = HBTE(addr="10.57.172.198", port_numbers=[6])

_common_unit_2121 = CommonUnit(
    lmp_connection=_lmp_connection_2121,
    capacity_units=[_capacity_unit_1_2121, _capacity_unit_2_2121, _capacity_unit_3_2121],
    pdu_port=_gnb_pdu.pdu_ports[6],
    hardware_type="ASIL"
)

_airscale_2121 = Airscale(common_units=[_common_unit_2121])

_du_2121 = DU(airscale=_airscale_2121, rus=[_ru_AVQQ, _ru_AQQF], f1_m_ip_addr="10.57.225.4")

# CU
_cu_2121 = CU(
    backhaul_site_oam_ip="10.57.225.4",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.4", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts_2121 = ClassicalBts(
    dus=[_du_2121], cu=_cu_2121, instance_id=2121, global_bts_id=37160
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.59", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(interface="eth1", device=_classical_bts_2121.dus[0].airscale.common_units[0], interface_type="lmp")
    ],
)
# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts_2121],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
)
