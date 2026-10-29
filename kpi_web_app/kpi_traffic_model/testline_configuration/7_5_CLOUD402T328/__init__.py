import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import MediaTek
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
from taf.config.testline.legacy import SCF

__maintainer__ = "Dong Tingting"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "tingting.dong@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.119", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# #RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.81", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU for classicalBTS
_ru_0_pdu = FACOM(addr="10.68.87.78", port_numbers=[5])

_ru_0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQI,
    signal_analyzer=None,
)

# gnb for classiclBTS
_gnb_asik_ip = "10.68.88.199"

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr=_gnb_asik_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.68.87.81", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0], f1_m_ip_addr=_gnb_asik_ip)

# #CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip=_gnb_asik_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_gnb_asik_ip, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_gnb_asik_ip, username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=328)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="root", password="nokia123"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port="57328",
)
_appserver = AppServer(_iperf_details_on_appserver)

# Control PC and UE##########
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.25", username="nokia5G", password="noki@123"
)
_iperf_details_on_ue = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="10.68.86.25",
    iperf_path="iperf",
    port=57102,
)
_mtk_ue = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/mtk/Apollo5G-SW_24.2.2020/MDDB_MT6297_S00_VMOLY_M70_DEV_W20_09_P1.EDB",
    imei="35190103100565",
    apn_url="c3static",
    iperf_details=_iperf_details_on_ue,
    capabilities=["REAL_MEDIATEK_UE"],
)


_tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    tl_cloud_topology="classical",
    enbs=[_lte_real_enb],
    ues=[_mtk_ue],
    appserver=_appserver,
)
tl = _tl


# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
