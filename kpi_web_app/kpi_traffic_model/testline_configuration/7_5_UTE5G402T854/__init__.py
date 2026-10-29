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
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "yin.4.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.84", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.84",
        username="coam",
        password="zO&n1W*ktp7",
        port=22,
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.84",
        username="coam",
        password="zO&n1W*ktp7",
        port=22,
    )
)

# _lss
_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.84", port="22", username="coam", password="zO&n1W*ktp7"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_1_pdu = FACOM(addr="10.57.172.212", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="AQQQ",
    serial_number="DH233090082",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    # lmp_connection=SshServiceDetails(
    #     addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    # ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
)

_ru_2_pdu = FACOM(addr="10.57.172.212", port_numbers=[3])
_ru_2 = RU(
    ru_hw_group="AQQQ",
    serial_number="1M234301462",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    # lmp_connection=SshServiceDetails(
    #     addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    # ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
)

_ru_3_pdu = FACOM(addr="10.57.172.212", port_numbers=[2])
_ru_3 = RU(
    ru_hw_group="AQQQ",
    serial_number="DH233064313",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    # lmp_connection=SshServiceDetails(
    #     addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    # ),
    pdu_port=_ru_3_pdu.pdu_ports[2],
)

_ru_4_pdu = FACOM(addr="10.57.172.212", port_numbers=[4])
_ru_4 = RU(
    ru_hw_group="AHPB",
    serial_number="K9201111631",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    # lmp_connection=SshServiceDetails(
    #     addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    # ),
    pdu_port=_ru_4_pdu.pdu_ports[4],
)

_ru_5_pdu = FACOM(addr="10.57.172.212", port_numbers=[5])
_ru_5 = RU(
    ru_hw_group="AHPB",
    serial_number="K9201111623",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    # lmp_connection=SshServiceDetails(
    #     addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    # ),
    pdu_port=_ru_5_pdu.pdu_ports[5],
)
# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.57.241.232", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5], f1_m_ip_addr="10.57.151.240")

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.240", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.240", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_pdu = FACOM(addr="10.57.241.233", port_numbers=[7])
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.151.6", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[7],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, global_bts_id=10283, instance_id=10283
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=854, global_bts_id=854)

# _lss
_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.84", port="22", username="coam", password="zO&n1W*ktp7"
    )
)

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57854,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.79", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19919002146",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

# Real Core
# _real_5g_core_details = RealCore5GDetails(
#     amf=AMF(
#         oam_ssh_connection_details=SshServiceDetails(
#             addr="10.110.227.5", username="xxx", password="xxx"
#         ),
#         n2=NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1),
#     )
# )
# _pdns = [
#     PDN(pdp_type=PDPTypes.IPV4V6.value, apn="wap1.nokia.com"),
#     PDN(pdp_type=PDPTypes.IPV4V6.value, apn="wap1.nokia.com"),
# ]
# _realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="2", pdns=_pdns)
#
# _iperf_ul = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.57.162.10",
#     iperf_path="iperf",
#     port=47854,
# )
#
# _appserver = AppServer(iperf_details=_iperf_ul)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    expected_prompt="[cmw_sg7@APPServer-2 ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[57854, 58854],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="35",
    # ue_pc_address="10.57.150.52",
    ue_pc_address="10.57.130.197",
    root_password="f7aa49923a68",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL22140068F",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)

_attenuator = HBTE(
    ip_addr="10.57.232.52",
    port="5000",
    attenuation_port_numbers=[5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc, _lss],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1],
    attenuator=[_attenuator],
)
