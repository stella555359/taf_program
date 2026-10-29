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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import TopYoung, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "lenie"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com"
__email__ = "lei.nie@nokia-sbell.com"
# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.74", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
# 5GRU for classicalBTS
# PB for RU
_ru_pdu = HBTE(addr="10.57.172.204", port_numbers=[1])
_ru = RU(
    ru_hw_group="AQQJ",
    serial_number="1M222820456",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.13", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)
_ru_pdu2 = HBTE(addr="10.57.172.204", port_numbers=[3])
_ru2 = RU(
    ru_hw_group="AQQJ",
    serial_number="1M222820454",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.34", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)
_ru_pdu3 = HBTE(addr="10.57.172.204", port_numbers=[4])
_ru3 = RU(
    ru_hw_group="AQQJ",
    serial_number="1M222820455",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.239", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
)
_ru_pdu4 = HBTE(addr="10.57.172.204", port_numbers=[6])
_ru4 = RU(
    ru_hw_group="AHPJ",
    serial_number="K9231429128",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.17", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[6],
)
_ru_pdu5 = HBTE(addr="10.57.172.204", port_numbers=[5])
_ru5 = RU(
    ru_hw_group="AHPJ",
    serial_number="K9232032185",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.70", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[5],
)
_ru_pdu6 = HBTE(addr="10.57.172.204", port_numbers=[2])
_ru6 = RU(
    ru_hw_group="AHPJ",
    serial_number="K9232032183",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.179", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[2],
)
# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abio internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = HBTE(addr="10.57.241.141", port_numbers=[1])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.74", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.57.225.34",
)
# #CU


_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.34", username="Nemuadmin", password="nemuuser"
    ),
)
# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="1.1.1.1", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.1.1", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)
##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=888, global_bts_id=11554)


_netact = Netact("10.110.144.154")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[],
    test_pcs=[_docker_pc, _tce_pc],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
# tl = TestlineWrapper(tl)
