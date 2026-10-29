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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
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
from taf.config.testline import NetworkAddress, RoutingInformation

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
        addr="10.57.157.30", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_ru_pdu = HBTE(addr="10.57.242.25", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_attenuator = TopYoung(
    ip_addr="10.10.10.10", port=23, attenuation_port_numbers=[9, 10, 11, 12]
)

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[7],
    radio_type=RadioTypes.AWHQG,  # radio_type='AWHQG'
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
    ],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.243.75", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.57.242.14", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.243.75", cablinks=_ru_cablinks
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.243.75",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.243.73", ip_prefix_length=29),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.243.75", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.243.75", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.243.75",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.243.73", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.57.243.75",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.243.73", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="10.57.243.75",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.243.73", ip_prefix_length=29),
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AWHQG"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1957, global_bts_id=1957)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="4.4.4.4", port="1/18", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="5.5.5.5", port="1/18", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# # netact - qin1
_netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)

# old version keyword under robotws5g/resource compatibility workaround
tl = TestlineWrapper(tl)
