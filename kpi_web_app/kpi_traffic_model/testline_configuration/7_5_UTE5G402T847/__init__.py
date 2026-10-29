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

__maintainer__ = "Qu Jing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "Jing.Qu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.12", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# PB for RU
_ru_pdu1 = FACOM(addr="10.101.46.20", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="AHLOB",
    serial_number="BL2243D50WW",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.63", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
)

_ru_pdu2 = FACOM(addr="10.101.46.20", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="AHLOB",
    serial_number="AH243007733",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.215", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)

_ru_pdu3 = FACOM(addr="10.101.46.22", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="AHLOB",
    serial_number="AH242902840",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.21", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[6],
)

_ru_pdu4 = FACOM(addr="10.101.45.16", port_numbers=[1])

_ru4 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2234N41KI",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.126", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[1],
)

_ru_pdu5 = FACOM(addr="10.101.45.16", port_numbers=[2])

_ru5 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2227N40O4",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.125", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[2],
)

_ru_pdu6 = FACOM(addr="10.101.45.16", port_numbers=[3])

_ru6 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2224N40AH",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.47", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[3],
)

_ru_pdu7 = FACOM(addr="10.101.46.22", port_numbers=[4])

_ru7 = RU(
    ru_hw_group="AEHC",
    serial_number="L1204110681",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.134", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu7.pdu_ports[4],
)

_ru_pdu8 = FACOM(addr="10.101.46.22", port_numbers=[5])

_ru8 = RU(
    ru_hw_group="AEHC",
    serial_number="L1211609180",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.136", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu8.pdu_ports[5],
)

_ru_pdu9 = FACOM(addr="10.101.46.20", port_numbers=[1])

_ru9 = RU(
    ru_hw_group="AEHC",
    serial_number="L1204708774",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.135", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu9.pdu_ports[1],
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
_gnb_pdu_0 = HBTE(addr="10.101.45.165", port_numbers=[1])
_gnb_pdu_1 = HBTE(addr="10.101.45.165", port_numbers=[1])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.12", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[1],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9],
    f1_m_ip_addr="10.101.50.198",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.198", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=847)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# X2 ENB
#_enb_pdu_0 = FACOM(addr="10.68.87.60", port_numbers=[2])
#_enb_lmp_connection_0 = SshServiceDetails(
#    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#)
#
#_enb_test_pc_0 = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.167.151", username="ute", password="iW_K#8.ute%A10h0m0ra"
#    )
#)
#_enb_common_unit_0 = CommonUnit(
#    lmp_connection=_enb_lmp_connection_0,
#    capacity_units=[],
#    pdu_port=_enb_pdu_0.pdu_ports[2],
#    test_pc=_enb_test_pc_0,
#    hardware_type=None,
#)
#_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
#_lte_real_enb_0 = RealEnb(
#    system_module=_real_enb_0,
#    oam_ip=NetworkAddress(v4="10.101.48.39"),
#    instance_id=4847,
#)

# ==================================================================================
# Concurrent ENB 1
_enb_pdu_1 = FACOM(addr="10.101.45.165", port_numbers=[5])
_enb_lmp_connection_common = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.94", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_enb_common_unit_1 = CommonUnit(
    lmp_connection=_enb_lmp_connection_common,
    capacity_units=[],
    pdu_port=_enb_pdu_1.pdu_ports[5],
    test_pc=_enb_test_pc_1,
    hardware_type=None,
)

_real_enb_1 = Airscale(common_units=[_enb_common_unit_1])
_lte_real_enb_1 = RealEnb(
    system_module=_real_enb_1,
    oam_ip=NetworkAddress(v4="10.101.50.202"),
    instance_id=8472,
)

####################################################################################
# Concurrent ENB 2
#_enb_pdu_2 = FACOM(addr="10.101.45.165", port_numbers=[5])
#_enb_lmp_connection_common = SshServiceDetails(
#    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#)
#
#_enb_test_pc_2 = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.155.14", username="ute", password="iW_K#8.ute%A10h0m0ra"
#    )
#)
#
#_enb_common_unit_2 = CommonUnit(
#    lmp_connection=_enb_lmp_connection_common,
#    capacity_units=[],
#    pdu_port=_enb_pdu_2.pdu_ports[5],
#    test_pc=_enb_test_pc_2,
#    hardware_type=None,
#)
#
#_real_enb_2 = Airscale(common_units=[_enb_common_unit_2])
#_lte_real_enb_2 = RealEnb(
#    system_module=_real_enb_2,
#    oam_ip=NetworkAddress(v4="10.101.50.199"),
#    instance_id=8471,
#)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# ==================================================================================
# ==================================================================================
# ==================================================================================



## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.101.63.95", port="1/12", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

_netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
 #   enbs=[_lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch],
)
