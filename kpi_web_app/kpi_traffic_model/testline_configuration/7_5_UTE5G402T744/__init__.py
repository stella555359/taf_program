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
from taf.config.testline.dcap import DcapRnD, DcapBasic

# ==================================================================================
# This example include MORAN/DUAL CORE/ CONCURRENT/ NR ONLY/ X2 ENB testline format.
# ==================================================================================

__maintainer__ = "lu miao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"  # TL owner's team
__email__ = "miao.1.lu@nokia-sbell .com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.24", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# 5GRU for classicalBTS
_ru_0_pdu = FACOM(addr="10.71.195.136", port_numbers=[6])

_ru_0 = RU(
    ru_hw_group="AWEUC",
    serial_number="AH221504258",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.200", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[6],
)

_ru_1_pdu = FACOM(addr="10.71.195.136", port_numbers=[4])

_ru_1 = RU(
    ru_hw_group="AWEUC",
    serial_number="AH205100753",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.199", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
)

_ru_2_pdu = FACOM(addr="10.71.195.137", port_numbers=[3])

_ru_2 = RU(
    ru_hw_group="AWEWB",
    serial_number="YK212500170",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.144", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
)

_ru_3_pdu = FACOM(addr="10.71.195.140", port_numbers=[5])

_ru_3 = RU(
    ru_hw_group="FRIJ",
    serial_number="EA164381919",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[5],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# GNB 0
##DU for classicalBTS
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_0 = HBTE(addr="10.71.195.151", port_numbers=[2])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.24", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru_0, _ru_1, _ru_2, _ru_3],
    f1_m_ip_addr="10.71.209.197",
)


##CU
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="10.71.209.197",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.197",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.197",
        username="Nemuadmin",
        password="nemuuser",
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=744)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# Netact IP
_netact = Netact("10.68.84.15")

# ==================================================================================
# ==================================================================================
# ==================================================================================
# X2 ENB
# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.209.238", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_enb_1 = SshServiceDetails(
    addr="10.71.209.197", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu_0 = FACOM(addr="10.71.195.149", port_numbers=[6])
_enb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.11", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[6],
    test_pc=_enb_test_pc_0,
    hardware_type=None,
)


_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb_0 = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.71.209.238"),
    instance_id=744,
    rms=[],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# Testline Summary


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_0],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
