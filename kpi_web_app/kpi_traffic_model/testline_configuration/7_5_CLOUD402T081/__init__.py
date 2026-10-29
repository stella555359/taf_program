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
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Su Li"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "li.su@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.112", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="10.57.240.164", username="nokia", password="nokia123"
)

_airmosaic_harness = HttpConnectionDetails(addr="10.57.240.164", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.249.84", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.249.84", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.166", port_numbers=[7])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[7],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.243.7", port_numbers=[5])

_ru = RU(
    ru_hw_group="Above6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.247.50", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.241.166", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])

_cu = CU(
    backhaul_site_oam_ip="10.57.247.50",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.247.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.247.50", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_prisma_ue],
    tl_cloud_topology=_tl_cloud_topology,
)

# compatibility workaround
tl = TestlineWrapper(tl)

# parameters with new values
PARAMS_TO_MODIFY_SCF = [
    dict(value="Nokia HZ TL081", dist_name="MRBTS-1900", p_name="btsName"),
    dict(value="262", dist_name="MRBTS-1900/NRBTS-1", p_name="mcc"),
    dict(value="03", dist_name="MRBTS-1900/NRBTS-1", p_name="mnc"),
    dict(value="2", dist_name="MRBTS-1900/NRBTS-1", p_name="mncLength"),
    dict(value="2073343", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="nrarfcn"),
    dict(value="5", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="dllaIniMcs"),
    dict(value="5", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="ullaIniMcs"),
    dict(
        value="15",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="zeroCorrelationZoneConfig",
    ),
    dict(value="22452", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="gscn"),
    dict(
        value="semiStatic",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="frameStructureType",
    ),
    dict(
        value="2Symbols",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="guardPeriodLength",
    ),
    dict(
        value="1/4", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="ulDlDataSlotRatio"
    ),
    dict(
        value="1pps/ToD from Sync Hub Master",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SYNC-1/CLOCK-1",
        p_name="syncInputType",
    ),
    dict(
        value="::",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPRTV6-1",
        p_name="destIpv6Addr",
    ),
    dict(
        value="2a00:8a00:8000:136:10:57:247:7d",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPRTV6-1",
        p_name="gatewayIpv6Addr",
    ),
]

PARAMS_TO_DELETE_SCF = [
    dict(list_name="mPlane"),
    dict(list_name="s1Uplane"),
    dict(list_name="x2Cplane"),
    dict(list_name="x2Uplane"),
]

PARAMS_TO_ADD_SCF = [
    dict(
        value="150",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SYNC-1/CLOCK-1",
        p_name="totalDelayFromSHM",
    )
]

OBJECT_TO_ADD_SCF = [
    dict(
        class_name="com.nokia.srbts.tnl:VLANIF",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/ETHSVC-1/ETHIF-1/VLANIF-1",
        version="TNL5G18A_1810_010",
    ),
    dict(
        class_name="com.nokia.srbts.tnl:VLANIF",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/ETHSVC-1/ETHIF-1/VLANIF-2",
        version="TNL5G18A_1810_010",
    ),
]

ITEM_TO_ADD_SCF = [
    dict(
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="mPlane",
        elements=dict(
            ipV6AddressDN1="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV6-1"
        ),
    ),
    dict(
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="s1Uplane",
        elements=dict(
            ipV6AddressDN1="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-2/IPADDRESSV6-1"
        ),
    ),
    dict(
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="x2Cplane",
        elements=dict(
            ipV6AddressDN1="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-2/IPADDRESSV6-1"
        ),
    ),
    dict(
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="x2Uplane",
        elements=dict(
            ipV6AddressDN1="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-2/IPADDRESSV6-1"
        ),
    ),
]

LIST_TO_ADD_SCF = [
    dict(dist_name="MRBTS-1900/NRBTS-1", list_name="mPlane"),
    dict(dist_name="MRBTS-1900/NRBTS-1", list_name="s1Uplane"),
    dict(dist_name="MRBTS-1900/NRBTS-1", list_name="x2Cplane"),
    dict(dist_name="MRBTS-1900/NRBTS-1", list_name="x2Uplane"),
]
