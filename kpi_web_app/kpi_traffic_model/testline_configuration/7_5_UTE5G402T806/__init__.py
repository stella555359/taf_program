import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import MediaTek
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, MME, AMF, RealCore
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress


__maintainer__ = "Lei Nie"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ4_07@internal.nsn.com"  # TL owner's team
__email__ = "lei.nie@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.13", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu5 = FACOM(addr="10.57.241.143", port_numbers=[6])
_ru5 = RU(
    ru_hw_group="AKQJ",
    serial_number="1M222011910",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[6],
)
_ru_pdu6 = FACOM(addr="10.57.176.32", port_numbers=[3])
_ru6 = RU(
    ru_hw_group="AEQK",
    serial_number="DH214500197",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.111", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[3],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# GNB 0
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_gnb_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_0 = HBTE(addr="10.57.241.141", port_numbers=[8])
_gnb_pdu_1 = HBTE(addr="10.57.172.202", port_numbers=[3])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.13", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.234", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[8],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[3],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru5, _ru6],
    f1_m_ip_addr="10.57.225.37",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.37", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.37", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(
    dus=[_gnb_du_0], cu=_gnb_cu_0, global_bts_id=806, instance_id=806
)



##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# ==================================================================================
# ==================================================================================
# ==================================================================================
# UE
_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    ports=[57806],
    port=57806,
)
_appserver = AppServer(_iperf_details_on_appserver)
_mtk_host_ssh = SshServiceDetails(
    addr="10.57.130.49", username="mn5gran", password="nokia123@"
)

_iperf_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    ports=[58806],
    port=58806,
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100009157",
    apn_url="dxdata1",
    # iperf_details=_iperf_mtk,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="DUJAINT-V216GT-H1035",
)

_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[
        _mtk,
    ],
    appserver=_appserver,
)
