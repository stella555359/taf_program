import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Wang Ming"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "ming.5.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.171", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.90.130",
    mcc="262",
    mnc="03",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.90.130", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# #Cobham
_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678", port="52017"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/usr/bin/iperf",
    port="52017",
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.57.130.153", username="nokia5G", password="noki@123"
)
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port="52217",
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="C:/pyro_server",
    server_port=8080,
    edb_file_path=r"C:\Users\nokia5G\Desktop\1029\sw\MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB",
    imsi="262038001006052",
    imei="262038001006052",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)
_mtk.inject_file = r"C:\Users\nokia5G\Desktop\MTK\panxinyu\nokia_sa_tl217.tcl"

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)  # wap1
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/usr/bin/iperf",
    port="52217",
)

_appserver = AppServer(_iperf_details_on_appserver)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.57.241.137", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.235.37", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=1, global_bts_id=217)
# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.57.241.137", port_numbers=[6])

_ru = RU(
    #'AEHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.246.137", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.227.36")

_cu = CU(
    backhaul_site_oam_ip="10.57.227.36",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.36", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1217, global_bts_id=1048)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    core=_epc_sim,
    ues=[_mtk],
    tl_cloud_topology=_tl_cloud_topology,
    #    attenuator=_attenuator,
    test_pcs=[_host],
    appserver=_appserver,
)
