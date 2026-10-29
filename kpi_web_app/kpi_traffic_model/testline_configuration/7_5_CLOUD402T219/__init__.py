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
)
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

__maintainer__ = "Ji Jian"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "jian.ji@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.163", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/usr/bin/iperf",
    port=52026,
)

_huawei_host_ssh = SshServiceDetails(
    addr="10.68.86.40", username="nokia5G", password="noki@123"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_huawei_host_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52026,
)


_appserver = AppServer(iperf_details)

_huawei_host_ssh = SshServiceDetails(
    addr="10.68.86.40", username="nokia5g", password="noki@123"
)

_iperf_details_on_huawei = IperfDataTransferDetails(
    ssh_connection_details=_huawei_host_ssh,
    network_interface_address="",
    iperf_path="iperf",
    port=52026,
)
_huawei_pdu = HBTE(addr="1.1.1.1", port_numbers=[2]).pdu_ports[2]
_elt_path = "/cygdrive/d/MTK/ELT_exe_v2.1943.0_customer_Gen97_FT"

_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.40", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0219C14014084",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_huawei.pdu = _huawei_pdu
_huawei.elt_path = _elt_path

# RealEnb
_real_enb_pdu = HBTE(addr="10.68.87.21", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.68.87.18", port_numbers=[6])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQB,
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")
_capacity_unit2 = CapacityUnit(addr="192.168.253.24")
_capacity_unit3 = CapacityUnit(addr="192.168.253.28")
_capacity_unit4 = CapacityUnit(addr="192.168.253.32")

_gnb_pdu = HBTE(addr="10.68.87.21", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2, _capacity_unit3, _capacity_unit4],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.88.37")

_cu = CU(
    backhaul_site_oam_ip="10.68.88.37",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.37", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.37", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="219", global_bts_id="219")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_huawei],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)

# compatibility workaround
# tl = TestlineWrapper(tl)
