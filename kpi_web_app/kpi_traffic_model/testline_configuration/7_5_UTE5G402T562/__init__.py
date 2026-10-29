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
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    FPFH,
    TopYoung,
)

# from taf.config.testline.attenuator import HBTE as AHBTE
# from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
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
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer


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
        addr="10.57.157.98", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##RealEnb
# _lmp_connection_enb = SshServiceDetails(
#    addr="10.101.40.37", username="toor4nsn", password="oZPS0POrRieRtu"
# )
# _enb_pdu = HBTE(addr="10.101.45.132", port_numbers=[8])
# _common_unit_1 = CommonUnit(
#    lmp_connection=_lmp_connection_enb,
#    capacity_units=[],
#    pdu_port=_enb_pdu.pdu_ports[8],
# )
# _real_enb = Airscale(common_units=[_common_unit_1])
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS

_ru_pdu = TopYoung(addr="10.101.45.135", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQL,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.50.133", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.133", port_numbers=[2])

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
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.101.50.133",
    cablinks=_ru_cablinks,
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.133", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_ASIBA102R_ABIOA103B4_AQQL"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2462, global_bts_id=2462)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55977, 55978],
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
    ue_pc_address="10.68.86.96",
    root_password="d3da6422b9a3",
    ue_manage_ip="192.168.1.1",
    serial_number="85d9919b",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.1",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

_enb_sbts_1 = RealEnb(
    system_module=[_common_unit_0],
    airscale=_airscale,
    rms=[_ru],
    oam_ip=NetworkAddress("10.101.50.133"),
    instance_id=2462,
    global_bts_id=2462,
)


tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    gnbs=[_classical_bts],
    ues=[_fastmile_1],
    tl_cloud_topology=_tl_cloud_topology,
)
