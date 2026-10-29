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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Chen Cheng"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com"  # TL owner's team
__email__ = "cheng.2.chen@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.5", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# 5GRU for classicalBTS
# PB for RU
_ru_pdu7 = FACOM(addr="10.71.196.46", port_numbers=[1])
_ru7 = RU(
    ru_hw_group="AEHC",
    serial_number="L1205002772",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.228", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu7.pdu_ports[1],
)
_ru_pdu8 = FACOM(addr="10.71.196.40", port_numbers=[4])
_ru8 = RU(
    ru_hw_group="AEHC",
    serial_number="K9214824402",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.227", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu8.pdu_ports[4],
)
_ru_pdu9 = FACOM(addr="10.71.196.43", port_numbers=[1])
_ru9 = RU(
    ru_hw_group="AEHC",
    serial_number="K9221730258",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.226", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu9.pdu_ports[1],
)
_ru_pdu = FACOM(addr="10.71.196.42", port_numbers=[1])
_ru = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2114G1A7P",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.186", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)
_ru_pdu2 = FACOM(addr="10.71.196.40", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2114G1A7T",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.234", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
)
_ru_pdu3 = FACOM(addr="10.71.196.44", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="AHLOA",
    serial_number="K9182103369",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.229", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
)
_ru_pdu4 = FACOM(addr="10.71.196.42", port_numbers=[6])
_ru4 = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2133V0HYH",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.233", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[6],
)
_ru_pdu5 = FACOM(addr="10.71.196.42", port_numbers=[5])
_ru5 = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2133V0HZG",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.231", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[5],
)
_ru_pdu6 = FACOM(addr="10.71.196.42", port_numbers=[4])
_ru6 = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2120V0CVO",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.204.230", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[4],
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
_gnb_pdu_0 = FACOM(addr="10.71.196.36", port_numbers=[4])
_gnb_pdu_1 = FACOM(addr="10.71.196.36", port_numbers=[5])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.5", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[4],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[5],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9],
    f1_m_ip_addr="10.71.211.170",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.170", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.170", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=868)


# ==================================================================================
# ==================================================================================
# ==================================================================================
# X2 ENB
#_enb_pdu_0 = FACOM(addr="10.57.241.160", port_numbers=[1])
#_enb_lmp_connection_0 = SshServiceDetails(
#    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#)

#_enb_test_pc_0 = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.157.226", username="ute", password="iW_K#8.ute%A10h0m0ra"
#    )
#)
#_enb_common_unit_0 = CommonUnit(
#    lmp_connection=_enb_lmp_connection_0,
#    capacity_units=[],
#    pdu_port=_enb_pdu_0.pdu_ports[1],
#    test_pc=_enb_test_pc_0,
#    hardware_type=None,
#)
#_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
#_lte_real_enb_0 = RealEnb(
#    system_module=_real_enb_0,
#    oam_ip=NetworkAddress(v4="10.57.236.185"),
#   instance_id=5420,
#)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.68.85.28", port="1/12", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.162.10",
    user="cmw_sg7",
    password="Nokia07!",
    bind_interface_ip="10.57.162.10",
    expected_prompt="[cmw_sg7@APPServer-2 ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[57868, 58868],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.0.176.204",
    root_password="a66a2fb2bded",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400692",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_2 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.0.176.126",
    root_password="89baa7f22e22",
    ue_manage_ip="192.168.2.1",
    serial_number="LPL2214004D4",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

_fastmile_3 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.0.176.126",
    root_password="63ea69f2f52c",
    ue_manage_ip="192.168.3.1",
    serial_number="LPL2214004C4",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE3", "nokia_fastmile"],
)

_ue_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.204", username="mn5gran", password="nokia123@"
    )
)

_ue_pc_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.126", username="mn5gran", password="nokia123@"
    )
)

_ue_pc_3 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.126", username="mn5gran", password="nokia123@"
    )
)

_netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_host,
    test_pcs=[_ue_pc_1, _ue_pc_2, _ue_pc_3],
    gnbs=[_classical_bts_0],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[_fastmile_1, _fastmile_2, _fastmile_3],
    #    appserver=_appserver,
)
