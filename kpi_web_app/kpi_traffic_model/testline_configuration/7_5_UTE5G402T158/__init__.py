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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import TopYoung, HBTE, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek, TafUeFastmile
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

# added in taf.meta 5.4
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
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)


__maintainer__ = "Charlotte Wu"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "charlotte.wu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #RMOD-1 AQQL
_ru_1_pdu = FPFH(
    addr="10.71.196.13",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    serial_number="L1214608877",
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQL,
)

# RMOD-2 AQQY
_ru_2_pdu = TopYoung(addr="10.71.196.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AQQY,
    serial_number="1M232304340",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_2_pdu.pdu_ports[4],
)

# 9217
_pdu_1 = TopYoung(addr="10.71.196.21", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_fsp_1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIO",
    hardware_version="475266A.104",
    serial_number="L1214608242",
)

_fsp_2 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIQ",
    hardware_version="476397A.102",
    serial_number="L1233103998",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1, _fsp_2],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIM",
    hardware_version="475765A.102",
    serial_number="L1230610711",
)

# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_fsp_1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_fsp_1, label="OPT", port_id=2),
        target=Endpoint(unit=_ru_2, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_fsp_2, label="OPT", port_id=1),
        target=Endpoint(unit=_ru_1, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_fsp_2, label="OPT", port_id=2),
        target=Endpoint(unit=_ru_2, label="OPT", port_id=1),
    ),
]


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/usr/bin/iperf",
    port=42158,
)
_appserver = AppServer(_iperf_details_on_appserver)

# UE-1 LTE CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42158, 43158],
)


_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile_1 = TafUeFastmile(
    com_port="3",
    ue_pc_address="10.71.218.226",
    root_password="47eaf832c585",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400611",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=6158,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# UE-2 NR CPE
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42158, 43158],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile_2 = TafUeFastmile(
    com_port="3",
    ue_pc_address="10.71.218.228",
    root_password="c9aaa982f9ef",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214005FB",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5158,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


# ENB
_real_enb = Airscale(common_units=[_fct_1])

_enb_sbts_1 = RealEnb(airscale=_real_enb, rms=None)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_airscale = Airscale(common_units=[_fct_1])


_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2],
    f1_m_ip_addr="10.71.211.136",
    cablinks=_ru_cablinks,
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.211.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.136", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.211.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.211.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.211.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10905, global_bts_id=10905)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.61", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)
_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIML_ABIOB1_ABIQB2_AQQL_AQQY"

tl = TestLine(
    test_pc=_host,
    ues=[_fastmile_1, _fastmile_2],
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)
