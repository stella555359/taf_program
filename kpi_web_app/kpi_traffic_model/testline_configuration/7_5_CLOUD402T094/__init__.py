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
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "yin.4.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.32", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# _docker_pc = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.195.82",
#        username="utfuser",
#        password="utfadmin!",
#        port=49148,
#    )
# )
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)
# _tce_pc = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.195.82",
#        username="utfuser",
#        password="utfadmin!",
#        port=49148,
#    )
# )
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

External_PCs_For_CellTrace = dict(docker=_docker_pc, tce=_tce_pc)
_HOTarget_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.128", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.57.241.232", port_numbers=[3])
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
)

_ru_pdu2 = HBTE(addr="10.57.241.226", port_numbers=[4])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.189", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.151.231", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.57.241.233", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2], f1_m_ip_addr="10.57.151.231")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.231", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.231", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.151.17", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, global_bts_id=94, instance_id=94)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=94, global_bts_id=94)
_netact = Netact("10.110.144.147")

# PB for RU
_ru_pdu_828 = FACOM(addr="10.57.241.228", port_numbers=[2])
_ru_828 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu_828.pdu_ports[2],
)

_ru_pdu2_828 = FACOM(addr="10.57.241.226", port_numbers=[4])
_ru2_828 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu2_828.pdu_ports[4],
)

# gNB LMP IP
_lmp_connection_828 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit_828 = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu_828 = FACOM(addr="10.57.241.233", port_numbers=[5])
_common_unit_828 = CommonUnit(
    lmp_connection=_lmp_connection_828,
    capacity_units=[_capacity_unit_828],
    pdu_port=_gnb_pdu_828.pdu_ports[5],
)
_airscale_828 = Airscale(common_units=[_common_unit_828])
_du_828 = DU(
    airscale=_airscale_828, rus=[_ru_828, _ru2_828], f1_m_ip_addr="10.57.151.237"
)

# gNB OAM M-plane IP
_cu_828 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.237", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.237", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts_828 = ClassicalBts(
    dus=[_du_828], cu=_cu_828, instance_id=828, global_bts_id=828
)

# CI_Detail_UE_Type='LG'
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57094,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.169", username="mn5gran", password="nokia123@"
    ),
    serial_number="9EQUT20903003188",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)
# lg_v50
# _appserver_ssh = SshServiceDetails(addr='10.57.252.107', username='root', password='APPpass')
# _iperf=IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address='10.57.252.107',
#     iperf_path='/opt/app/iperf'
# )
# _android = Android(
#     ssh_connection_details=SshServiceDetails(addr='10.57.151.7', username='CNHZ5GRAN1130+tester', password='tester123'),
#     serial_number='c803df5a',
#     server_dir='/cygdrive/c/pyro_server',
#     python_path='C:/Python27/python.exe',
#     qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe',
#     diag_cfg_path='C:/pyro_server/DIAG.cfg',
#     iperf_details=_iperf,
#     capabilities=['REAL_UE', 'REAL_ANDROID_UE']
# )

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc, _HOTarget_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    nms=_netact,
)

# tl = TestlineWrapper(tl)
