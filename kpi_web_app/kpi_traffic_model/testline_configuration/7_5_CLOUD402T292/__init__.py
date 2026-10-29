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
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress


__maintainer__ = "lei nie"  # TL owner name
__team__ = "I_MI_MN_RAN_RD_VRF_HAZ_4_UUF_GMS@nokia.com"  # TL owner's team
__email__ = "lei.nie@nokia.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##testPC host(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.16", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.68.87.211", port_numbers=[4])
_ru = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2215V01DT",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.148", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
)

_ru_pdu2 = FACOM(addr="10.68.87.211", port_numbers=[3])
_ru2 = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2215V0124",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.167", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)

_ru_pdu3 = FACOM(addr="10.68.87.23", port_numbers=[5])
_ru3 = RU(
    ru_hw_group="AZHL",
    serial_number="AH211400610",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.88", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[5],
)

_ru_pdu4 = FACOM(addr="10.68.87.24", port_numbers=[3])
_ru4 = RU(
    ru_hw_group="AZHL",
    serial_number="YK210500042",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.98", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[3],
)
# ==================================================================================
# ==================================================================================
# ==================================================================================
# gnb_0
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_gnb_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.68.87.61", port_numbers=[5])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.16", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.27", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
    test_pc=_gnb_test_pc_1,
)
_airscale = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_du = DU(
    airscale=_airscale,
    rus=[_ru, _ru2, _ru3, _ru4],
    f1_m_ip_addr="10.101.48.42",
)
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.42", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.42", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=292)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# enb_0
#_lmp_connection_enb = SshServiceDetails(
#    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#)
#_enb_pdu = FACOM(addr="10.68.87.107", port_numbers=[4])
#_enb_test_pc_0 = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.155.18", username="ute", password="iW_K#8.ute%A10h0m0ra"
#    )
#)
#_enb_common_unit_1 = CommonUnit(
#    lmp_connection=_lmp_connection_enb,
#    capacity_units=[],
#    pdu_port=_enb_pdu.pdu_ports[4],
#    test_pc=_enb_test_pc_0,
#    hardware_type=None,
#)
#_real_enb = Airscale(common_units=[_enb_common_unit_1])
#_lte_real_enb = RealEnb(
#    system_module=_real_enb,
#    oam_ip=NetworkAddress(v4="10.57.236.185"),
#    instance_id=5420,
#    rms=[],
#)

# ==================================================================================
# ==================================================================================
# ==================================================================================
## switch Dtor
##switch port to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.120", port="1/6", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


_netact = Netact("10.108.243.22")

# ==================================================================================
# ==================================================================================
# ==================================================================================
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch],
)
