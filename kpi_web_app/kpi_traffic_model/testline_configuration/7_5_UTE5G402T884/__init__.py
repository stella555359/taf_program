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

__maintainer__ = "jqu003"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "jing.qu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.38", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_ru_pdu = FACOM(addr="10.57.241.156", port_numbers=[5])

_ru = RU(
    ru_hw_group="AZQG",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.10.10.10", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

# _ru_pdu2 = FACOM(addr='10.57.241.224', port_numbers=[3])
#
# _ru2 = RU(
#     ru_hw_group='hw_group',
#     default_ssh_connection_details=SshServiceDetails(addr='172.16.1.5', username='root', password='root'),
#     lmp_connection=SshServiceDetails(addr='172.16.1.5', username='root', password='root'),
#     pdu_port=_ru_pdu2.pdu_ports[3])

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.57.241.160", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru])

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.228.173",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.173", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.173", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="1.1.1.1", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="1.1.1.1", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

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

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=11553, global_bts_id=11553)
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
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
