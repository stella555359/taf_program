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

__maintainer__ = "Shen jian"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "jian.shen@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.205", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.163",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)

_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.163",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# RU List
_ru_pdu = FACOM(addr="10.101.46.22", port_numbers=[2])
_ru = RU(
    ru_hw_group="AHPE",
    serial_number="1M194709204",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.200", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)

_ru_pdu2 = FACOM(addr="10.101.46.22", port_numbers=[3])
_ru2 = RU(
    ru_hw_group="AHPE",
    serial_number="1M194709200",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.251", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)

_ru_pdu4 = FACOM(addr="10.101.46.20", port_numbers=[3])
_ru4 = RU(
    ru_hw_group="AZQJ",
    serial_number="1M204740633",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.149", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[3],
)

_ru_pdu5 = FACOM(addr="10.101.46.20", port_numbers=[1])
_ru5 = RU(
    ru_hw_group="AZQJ",
    serial_number="1M204740652",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.150", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[1],
)

_ru_pdu6 = FACOM(addr="10.101.46.20", port_numbers=[2])
_ru6 = RU(
    ru_hw_group="AZQJ",
    serial_number="1M204740638",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.151", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[2],
)

_ru_pdu7 = FACOM(addr="10.68.87.111", port_numbers=[1])
_ru7 = RU(
    ru_hw_group="AEQV",
    serial_number="1M200802154",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.119", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu7.pdu_ports[1],
)

_ru_pdu8 = FACOM(addr="10.68.87.111", port_numbers=[2])
_ru8 = RU(
    ru_hw_group="AEQV",
    serial_number="1M200802159",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.120", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu8.pdu_ports[2],
)

_ru_pdu9 = FACOM(addr="10.68.87.109", port_numbers=[2])
_ru9 = RU(
    ru_hw_group="AEQV",
    serial_number="1M200209130",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.118", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu9.pdu_ports[2],
)
# ==================================================================================
# ==================================================================================
# ==================================================================================
# GNB 0
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.205", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_pdu = FACOM(addr="10.101.45.165", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9])
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.200", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.200", username="Nemuadmin", password="nemuuser"
    ),
)
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=848, global_bts_id=848)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.68.87.107", port_numbers=[4])
_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.205", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
    test_pc=_enb_test_pc_0,
    hardware_type=None,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    system_module=_real_enb,
    oam_ip=NetworkAddress(v4="10.68.89.21"),
    instance_id=809,
    rms=[],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# Real Core
_real_5g_core_details = RealCore5GDetails(
    amf=AMF(
        oam_ssh_connection_details=SshServiceDetails(
            addr="10.110.66.198", username="xxx", password="xxx"
        ),
        n2=NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1),
    )
)
_realcore = RealCore(five_g=_real_5g_core_details, mcc="262", mnc="3")


## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.68.85.9", port="1/42", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)
_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    test_pcs=[_docker_pc, _tce_pc],
    enbs=[_lte_real_enb],
    core=_realcore,
    switches=[_dell_s4048on_switch],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
