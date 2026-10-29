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

__maintainer__ = "Jin Journey"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "journey.jin@nokia-sbell.com"

# common
__all__ = ["tl"]


# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.115", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41492"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41493",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41492",
)

_appserver = AppServer(_iperf_details_on_appserver)

_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41491",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.23", username="nokia5G", password="noki@123"
    ),
    serial_number="fbb2941",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["NSA_UE", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
)

_sa_ue = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.23", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20903003330",
    server_dir="/cygdrive/c",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf2,
    capabilities=["SA_UE", "huawei"],
    clear_server_files="yes",
    clear_logs="yes",
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.71.195.228", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.210.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=246, global_bts_id=246
)


_real_enb_pdu2 = HBTE(addr="10.101.45.242", port_numbers=[6])

_common_unit_enb2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.51.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu2.pdu_ports[6],
)
_real_enb2 = Airscale(common_units=[_common_unit_enb2])
_lte_real_enb2 = RealEnb(
    airscale=_real_enb2, rms=None, instance_id=249, global_bts_id=249
)

# 5GRU------------------------------------
# add 2 more 5g ru info
_ru1_pdu = HBTE(addr="10.71.195.226", port_numbers=[3])

_ru1 = RU(
    # Above6GHZ or Below6GHZ
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQB,
    serial_number="1M195002740",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.71.195.228", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.71.210.228")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.210.228",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.228", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=246, global_bts_id=246)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb, _lte_real_enb2],
    gnbs=[_classical_bts],
    ues=[_android_0, _sa_ue],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
)

# Example for topyoung attenuator part
# print tl.gnbs[0].dus[0].rus[0].radio_type.value
# print tl.ues[0].iperf_details.port
# print tl.gnbs[0].dus[0].rus[0].serial_number
