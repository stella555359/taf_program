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

__maintainer__ = "Lin Zhe"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "zhe.1.lin@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.92", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_ru_pdu = FACOM(addr="10.57.241.165", port_numbers=[3])

_ru = RU(
    ru_hw_group="AZQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
)

# _ru_pdu2 = FACOM(addr='10.57.241.224', port_numbers=[3])
#
# _ru2 = RU(
#     ru_hw_group='hw_group',
#     default_ssh_connection_details=SshServiceDetails(addr='172.16.1.5', username='root', password='root'),
#     lmp_connection=SshServiceDetails(addr='172.16.1.5', username='root', password='root'),
#     pdu_port=_ru_pdu2.pdu_ports[3])

##DU for classicalBTS
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_0 = FACOM(addr="10.57.241.167", port_numbers=[4])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.92", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[4],
    test_pc=_gnb_test_pc_0,
)

_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru],
    f1_m_ip_addr="10.57.225.163",
)

##CU
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="10.57.225.163",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.163", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.163", username="Nemuadmin", password="nemuuser"
    ),
)
# classicalbts
_classical_bts_0 = ClassicalBts(
    dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=298, global_bts_id=298
)

# RealEnb
_enb_pdu_1 = FACOM(addr="10.57.241.167", port_numbers=[7])

# _enb_test_pc_0 = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.167.87", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )
_enb_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_common_unit_1 = CommonUnit(
    lmp_connection=_enb_lmp_connection_1,
    capacity_units=[],
    pdu_port=_enb_pdu_1.pdu_ports[7],
    # test_pc=_enb_test_pc_0,
    hardware_type=None,
)
_real_enb_1 = Airscale(common_units=[_enb_common_unit_1])
_lte_real_enb_1 = RealEnb(
    rms=[],
    oam_ip=NetworkAddress(v4="10.57.225.178"),
    system_module=_real_enb_1,
    global_bts_id=4298,
    instance_id=4298,
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.215", port="1/5", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

## switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.57.129.214", port="1/11", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
