import os
import yaml
import re
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore4G
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress


__maintainer__ = "Xie Jiali"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "jia.xie@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.9", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_ru_4_pdu = FACOM(addr="10.57.251.253", port_numbers=[6])
_ru_4 = RU(
    ru_hw_group="AQQQ",
    serial_number="DH233064324",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.64", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[6],
)

_ru_3_pdu = FACOM(addr="10.57.251.253", port_numbers=[3])
_ru_3 = RU(
    ru_hw_group="AQQQA",
    serial_number="BL2349G604X",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.119", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[3],
)


_ru_2_pdu = FACOM(addr="10.57.172.235", port_numbers=[2])
_ru_2 = RU(
    ru_hw_group="AQQQA",
    serial_number="BL2408G606I",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.15", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[2],
)


_ru_1_pdu = FACOM(addr="10.57.241.165", port_numbers=[2])
_ru_1 = RU(
    ru_hw_group="AQQQA",
    serial_number="BL2329G6033",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.120", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.57.241.166", port_numbers=[2])
# gNB VM
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.9", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4], f1_m_ip_addr="10.57.228.68"
)

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.68", username="Nemuadmin", password="nemuuser"
    ),
)


# X2 ENB
_enb_pdu_0 = FACOM(addr="10.57.241.166", port_numbers=[1])

_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.70", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_enb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[1],
    test_pc=_enb_test_pc_0,
    hardware_type=None,
)
_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.57.228.69"),
    instance_id=8901,
    rms=[],
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=890, instance_id=890)

# classicalbts NetAct4-Chen(Gansu):10.108.248.82
# _netact = Netact("10.108.248.82")
# classicalbts NetAct5-Han:10.107.183.26
_netact = Netact("10.68.84.29")


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
