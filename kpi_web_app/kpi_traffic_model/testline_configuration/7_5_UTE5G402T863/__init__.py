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
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
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
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Lei Nie"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ4_07_UUF_GMS@internal.nsn.com"  # TL owner's team
__email__ = "lei.nie@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.4", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_ru_pdu_7 = FACOM(addr="10.57.241.156", port_numbers=[1])
_ru_7 = RU(
    ru_hw_group="AVHA",
    serial_number="L1250304098",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.125", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[1],
)

_ru_pdu_8 = FACOM(addr="10.57.172.223", port_numbers=[5])
_ru_8 = RU(
    ru_hw_group="AVHA",
    serial_number="L1245007162",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.14", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[5],
)

_ru_pdu_9 = FACOM(addr="10.57.241.163", port_numbers=[2])
_ru_9 = RU(
    ru_hw_group="AVHA",
    serial_number="L1244106477",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.117", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_9.pdu_ports[2],
)

_ru_pdu_1 = FACOM(addr="10.57.172.223", port_numbers=[6])
_ru_1 = RU(
    ru_hw_group="AHLOB",
    serial_number="AH251802804",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.114", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[6],
)

_ru_pdu_2 = FACOM(addr="10.57.241.156", port_numbers=[2])
_ru_2 = RU(
    ru_hw_group="AHLOB",
    serial_number="AH243007610",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.116", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[2],
)

_ru_pdu_3 = FACOM(addr="10.57.172.236", port_numbers=[2])
_ru_3 = RU(
    ru_hw_group="AHLOB",
    serial_number="BL2247D5167",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.216", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[2],
)

_ru_pdu_4 = FACOM(addr="10.57.172.223", port_numbers=[4])
_ru_4 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2339N49V4",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.123", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[4],
)

_ru_pdu_5 = FACOM(addr="10.57.241.157", port_numbers=[2])
_ru_5 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2339N49V2",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.124", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[2],
)

_ru_pdu_6 = FACOM(addr="10.57.241.165", port_numbers=[3])
_ru_6 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2220N403S",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.118", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[3],
)

_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_gnb_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_0 = FACOM(addr="10.57.241.164", port_numbers=[5])
_gnb_pdu_1 = FACOM(addr="10.57.241.164", port_numbers=[7])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.4", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.18", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[5],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[7],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9],
    f1_m_ip_addr="10.57.225.163",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.163", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.163", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=863, global_bts_id=863)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

_netact = Netact("10.107.178.214")


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[],
    nms=_netact,
    tl_cloud_topology=_tl_cloud_topology,
)
