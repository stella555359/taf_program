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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Jing Qu"  # TL owner name

__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_7_IV@internal.nsn.com"  # TL owner's team

__email__ = "jing.qu@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# classical gNB LMP
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.7", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_0_pdu = FACOM(addr="10.57.241.143", port_numbers=[3])
_ru_0 = RU(
    ru_hw_group="AEHC",
    serial_number="K9223130062",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.82", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[3],
)

_ru_1_pdu = FACOM(addr="10.57.241.172", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="AEHC",
    serial_number="AH242420603",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.235", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.57.241.144", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.57.227.167")

# gNB MPlane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.167", username="Nemuadmin", password="nemuuser"
    ),
)

# instance_id=MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=290, global_bts_id=290)

_netact = Netact(addr="10.108.248.82")

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    enbs=[],
    nms=_netact,
    tl_cloud_topology=_tl_cloud_topology,
)
