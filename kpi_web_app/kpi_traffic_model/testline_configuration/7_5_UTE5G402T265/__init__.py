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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.104", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##RealEnb
_real_enb_pdu = HBTE(addr="10.57.246.206", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.152.139", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
##5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.57.249.28", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQV,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.57.241.149", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.227.229")
##CU #Auto TL Upgrading
_f1m = NetworkAddress(
    v4="10.57.249.138", v6="2a00:8a00:8000:136:10:57:249:8a", vlan_id=63
)
_x2c = NetworkAddress(
    v4="10.57.249.142", v6="2a00:8a00:8000:136:10:57:249:8e", vlan_id=64
)
_x2u = NetworkAddress(
    v4="10.57.249.146", v6="2a00:8a00:8000:136:10:57:249:92", vlan_id=65
)
_s1u = NetworkAddress(
    v4="10.57.227.229", v6="2a00:8a00:8000:136:10:57:227:e5", vlan_id=15
)
# _f1c = NetworkAddress(v4='9.9.1.2', v6='xxxx', vlan_id=2)
# _f1u = NetworkAddress(v4='9.9.1.3', v6='xxxx', vlan_id=3)
# _s1c = NetworkAddress(v4='9.9.3.1', v6='xxxx', vlan_id=1)
# _s1u = NetworkAddress(v4='9.9.3.2', v6='xxxx', vlan_id=2)
_tracing = NetworkAddress(
    v4="10.57.227.240", v6="2a00:8a00:8000:136:10:57:227:f0", vlan_id=1
)

_cu = CU(
    backhaul_site_oam_ip="10.57.227.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.229", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    x2c=_x2c,
    x2u=_x2u,
    s1u=_s1u,
    tracing=_tracing,
)
##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="2265", global_bts_id="1")

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
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
