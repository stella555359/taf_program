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
from taf.config.testline.testpc import TestPc
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
from taf.config.testline.appserver import AppServer,TafUeAppServer
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


__maintainer__ = "Jerry"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "jerry.wu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.124", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", password="dcapuser123"
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", port=1234
    )
)

# PB INFO of ENB IS NOT CORRECT #

# 5GRU
_ru_pdu1 = FPFH(addr="10.57.172.68", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu2 = FPFH(addr="10.57.172.66", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
    radio_type=RadioTypes.AVHA,
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu1.pdu_ports[4],
    radio_type=RadioTypes.AVHQA,
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu1.pdu_ports[2],
    radio_type=RadioTypes.AQHC,
)
#enb
_pdu_1 = FPFH(addr="10.57.172.66", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_fsp_1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIO",
    hardware_version="475266A.1014",
    serial_number="L1214610518",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    serial_number="L1233402518",
)


_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AVHA,
    serial_number="L1244506717",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.57.228.195"),
    instance_id=127,
    global_bts_id=127,
)



# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/usr/bin/iperf",
    port=42137,
)
_appserver = AppServer(_iperf_details_on_appserver)



#CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
#    binary_path="/home/vrf3_sg2/cpe_iperf/iperf",
    binary_path="/usr/bin/iperf",
    ports=[42127, 42137],
)


_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.130.247",
    root_password="de3abba2927a",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL22140062F",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=2127,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.228.195", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_du_pdu = FPFH(addr="10.57.172.66", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru1, label="SFP", port_id=4),
    )
]

_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.57.228.195", cablinks=_ru_cablinks
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.228.195",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.195", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.228.195",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.228.195",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.228.195",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=127, global_bts_id=127)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata4"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SPARK_SA_ASIMR_ABIO_ABIQ2_AVHA_AVHQA_AQHC"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    ues=[_fastmile],
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)
