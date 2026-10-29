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

# from taf.config.testline.attenuator import (
#    AttenuationPort,
#    TopYoung,
# )  # added in taf.meta 5.4
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

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.71.197.24", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQE,  # radio_type='AEQE'
    serial_number="1M211717561",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
)

_gnb_pdu = HBTE(addr="10.71.197.26", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.71.214.236",
    cablinks=_ru_cablinks,
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.236",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.236/27"
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.236", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.236", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.214.236",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.236/27"
        ),
    ),
    x2u=NetworkAddress(
        v4="10.71.214.236",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.236/27"
        ),
    ),
    s1u=NetworkAddress(
        v4="10.71.214.236",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.71.214.225", destIpAddr="10.71.214.236/27"
        ),
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIKL_ABILB1_AEQE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1961, global_bts_id=10915)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55995
)

_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55996
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55997,
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55998,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
ue_config_path = os.path.join(_cfg_dir, "TestData/ue.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        _ue_read = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_read)
        for item in qci_port:
            _ue_read = _ue_read.replace(item, str(eval(item)))
        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
else:
    _ue_config = ""

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.60", username="ute", password="uteUTE!"
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
    gnbs=[_classical_bts],
    core=RealCore(mcc=460, mnc=2),
    ues=[_ue_config],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
