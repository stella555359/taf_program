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
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb, PrismaEnb

# ,DocomoEnb

__maintainer__ = "Xing Jing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jing.1.xing@nokia-sbell.com"

PARAMS_TO_MODIFY_TL = [
    dict(
        value="172.18.10.20",
        dist_name="MRBTS-1900/NRBTS-1/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="172.18.10.11",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="172.18.10.12",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
    dict(
        value="172.18.10.12",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpAddr",
    ),
    dict(
        value="172.18.10.10",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
]

# tmp=_PARAMS_TO_MODIFY_SCF

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.119", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Airphone
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.71", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.167.71", username="Nemuadmin", password="nemuuser"
    ),
)

_egate = SshServiceDetails(addr="10.57.167.93", username="nokia", password="nokia123")

_l3 = SshServiceDetails(addr="10.57.163.13", username="_rcpadmin", password="RCP_owner")

_l2 = SshServiceDetails(addr="10.57.163.13", username="_rcpadmin", password="RCP_owner")

_airphone_pdu = FACOM(addr="10.57.241.134", port_numbers=[4])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.235.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_airphone_pdu.pdu_ports[4],
)

_l1 = Airscale(common_units=[_common_unit_1])

_airphone = Airphone(
    egate=_egate,
    l3_ssh_connection_details=_l3,
    l2_ssh_connection_details=_l2,
    l1=_l1,
    l3_port=7777,
    edaemon_port=11113,
    egate_port=10000,
    airphone_cloud=_airphone_cloud,
)

##lteemu sim enb
_lte_sim_enb = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.93", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/4g_uec/",
    cfg_filename="basic_wts_step1.cfg",
)


##DU
_lmp_connection = SshServiceDetails(
    addr="10.57.235.2", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.241.134", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale)

_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.235.2", username="Nemuadmin", password="nemuuser"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.57.235.2"),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_sim_enb],
    ues=[_airphone],
    tl_cloud_topology=_tl_cloud_topology,
)
