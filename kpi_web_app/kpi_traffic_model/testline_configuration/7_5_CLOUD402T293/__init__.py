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
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)

__maintainer__ = "Xing Casbo"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ4_07@internal.nsn.com"  # TL owner's team
__email__ = "casbo.xing@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.162", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_l3call_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.130.103", port="22", username="mn5gran", password="nokia123@"
    )
)
# 5GRU for classicalBTS
# PB for RU
_ru_pdu = FACOM(addr="10.57.241.138", port_numbers=[5])
_ru = RU(
    ru_hw_group="AQQQ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)
_ru_pdu2 = FACOM(addr="10.57.172.202", port_numbers=[1])
_ru2 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
)
_ru_pdu3 = FACOM(addr="10.57.241.156", port_numbers=[4])
_ru3 = RU(
    ru_hw_group="AKQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
)
_ru_pdu4 = FACOM(addr="10.57.241.138", port_numbers=[3])
_ru4 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[3],
)
_ru_pdu5 = FACOM(addr="10.57.241.222", port_numbers=[6])
_ru5 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[6],
)

_ru_pdu6 = FACOM(addr="10.57.241.236", port_numbers=[3])
_ru6 = RU(
    ru_hw_group="AVQL",
    serial_number="L1233006661",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.14", username="ute", password="3edc4rfv%TGB"
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
_gnb_pdu_0 = FACOM(addr="10.57.241.147", port_numbers=[2])
_gnb_pdu_1 = FACOM(addr="10.57.241.147", port_numbers=[3])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.162", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.82", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[2],
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
    rus=[_ru, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.57.225.98",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.98", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(
    dus=[_gnb_du_0], cu=_gnb_cu_0, global_bts_id=293, instance_id=293
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# ==================================================================================
# ==================================================================================
# ==================================================================================
# UE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    expected_prompt="[vrf3_sg6@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[57293, 58293],
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
    ue_pc_address="10.57.130.103",
    root_password="75aa26825455",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400466",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)

_attenuator = HBTE(
    ip_addr="10.57.239.35",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)


_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    test_pcs=[_l3call_pc],
    gnbs=[_classical_bts_0],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    # switches=[_dell_s4048on_switch],
    ues=[_fastmile_1],
    attenuator=[_attenuator],
)
