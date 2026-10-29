import os
import re
import yaml
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
from taf.config.testline import RU, DU
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.pdu import TopYoung as PBTopYoung
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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as PAHBTE

from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline import NetworkAddress, RoutingInformation
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

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

## Add for CPE3.2
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

# from taf.compatibility.configuration import TestlineWrapper


__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##RealEnb
# _real_enb_pdu = HBTE(addr="10.71.197.26", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.241", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    #    pdu_port=_real_enb_pdu.pdu_ports[7],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

_enb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.26", username="ute", password="uteUTE!"
    ),
    connections=[],
)

##5GRU for classicalBTS
_ru1_pdu = PBTopYoung(addr="10.71.197.19", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_attenuator = TopYoung(
    ip_addr="10.10.10.10", port=23, attenuation_port_numbers=[9, 10, 11, 12]
)

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWHQV.value,  # radio_type='AWHQV'
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
    ],
    serial_number="EB2104R0066",
)

_ru2_pdu = PBTopYoung(addr="10.71.197.19", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AWHQV.value,  # radio_type='AWHQV'
    serial_number="EB2104R0068",
)

_ru3_pdu = PBTopYoung(addr="10.71.197.19", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[7],
    radio_type=RadioTypes.AWHTA.value,  # radio_type='AWHTA'
    serial_number="EB2131R0150",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    rus=[_ru1, _ru2, _ru3],
)

_gnb_pdu = HBTE(addr="10.71.197.23", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru1, label="OPT", port_id=3),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=4),
        target=Endpoint(unit=_ru2, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=5),
        target=Endpoint(unit=_ru2, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=6),
        target=Endpoint(unit=_ru2, label="OPT", port_id=3),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=7),
        target=Endpoint(unit=_ru3, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=8),
        target=Endpoint(unit=_ru3, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=9),
        target=Endpoint(unit=_ru3, label="OPT", port_id=3),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.71.214.234",
    cablinks=_ru_cablinks,
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.71.214.234", vlan_id=None),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.234", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.234", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.71.214.234", vlan_id=None),
    x2u=NetworkAddress(v4="10.71.214.234", vlan_id=None),
    s1u=NetworkAddress(v4="10.71.214.234", vlan_id=None),
)

##cloud_topology #UTE Type

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AWHQG_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1957, global_bts_id=1957)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.26", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# # netact - qin1
_netact = Netact("10.107.178.214")

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55910, 55911],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.71.218.159",
    root_password="973a2b82d6e3",
    ue_manage_ip="192.168.1.1",
    serial_number="0123456789ABCDEF",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

# UTE test pc
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.26", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_test_pc_gnb],
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    ues=[_fastmile_1],
)
