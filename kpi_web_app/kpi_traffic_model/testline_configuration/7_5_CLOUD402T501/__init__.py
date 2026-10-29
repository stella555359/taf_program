import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
    OSP,
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
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# SCF_modify
PARAMS_MODSCF_pid01 = [
    dict(
        value="5G19/5g_pid11_class_4CC_eoc",
        dist_name="MRBTS-1900/EQM-1/APEQM-1",
        p_name="rapProfile",
    ),
    dict(value="210", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="pMax"),
    dict(value="210", dist_name="MRBTS-1900/NRBTS-1/NRCELL-2", p_name="pMax"),
    dict(value="210", dist_name="MRBTS-1900/NRBTS-1/NRCELL-3", p_name="pMax"),
    dict(value="210", dist_name="MRBTS-1900/NRBTS-1/NRCELL-4", p_name="pMax"),
    dict(
        value="true",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SECADM-1",
        p_name="actServiceAccountSsh",
    ),
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),
    dict(
        value="10.57.226.196",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="10.57.226.196",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="0.0.0.0",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="destIpAddr",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="destinationIpPrefixLength",
    ),
    dict(
        value="10.57.226.193",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        p_name="gateway",
    ),
]

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.12", username="root", password="nokia123"
    )
)

##RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.157", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.236.106", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.249.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEUA,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.226.196", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = FACOM(addr="10.57.241.130", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.226.196")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.226.196",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.196", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKA101L_ABILA101B2_AEUA"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1/1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1/1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# # netact
_netact = Netact("10.108.243.11")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)

# old version keyword under robotws5g/resource compatibility workaround
tl = TestlineWrapper(tl)
