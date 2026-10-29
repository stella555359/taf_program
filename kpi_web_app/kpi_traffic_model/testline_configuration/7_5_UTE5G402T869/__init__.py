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
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "chen cheng"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com"  # TL owner's team
__email__ = "cheng.2.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.6", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu = FACOM(addr="10.71.196.46", port_numbers=[5])
_ru = RU(
    ru_hw_group="AZQS",
    serial_number="1M212807211",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.82", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

_ru_pdu2 = FACOM(addr="10.71.196.46", port_numbers=[6])
_ru2 = RU(
    ru_hw_group="AZQU",
    serial_number="4H210730017",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.83", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
)

_ru_pdu3 = FACOM(addr="10.71.196.40", port_numbers=[5])
_ru4 = RU(
    ru_hw_group="AHPE",
    serial_number="1M212706011",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.191", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[5],
)

_ru_pdu4 = FACOM(addr="10.71.196.44", port_numbers=[2])
_ru3 = RU(
    ru_hw_group="AHEH",
    serial_number="EA201354041",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.80", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[2],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.22")

# gNB PB
_gnb_pdu = FACOM(addr="10.71.196.45", port_numbers=[1, 2])
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.6", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_1,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2, _ru3, _ru4])

_common_unit_slave = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    test_pc=TestPc(
        default_ssh_connection_details=SshServiceDetails(
            addr="10.57.189.7", username="ute", password="iW_K#8.ute%A10h0m0ra"
        )
    ),
)
_du_slave = DU(
    airscale=Airscale(common_units=[_common_unit_slave]), rus=[_ru, _ru2, _ru3, _ru4]
)

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.195", username="Nemuadmin", password="nemuuser"
    ),
)
# gNB OAM M-plane IP
_cu_slave = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.194", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.194", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_pdu = FACOM(addr="10.71.196.45", port_numbers=[1])
_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.35", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
    test_pc=_enb_test_pc_1,
    hardware_type=None,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    system_module=_real_enb,
    oam_ip=NetworkAddress(v4="10.71.211.196"),
    rms=None,
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=869, global_bts_id=869)
_classical_bts_slave = ClassicalBts(
    dus=[_du_slave], cu=_cu_slave, instance_id=870, global_bts_id=870
)
## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.71.211.193", port="1/6", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts, _classical_bts_slave],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
