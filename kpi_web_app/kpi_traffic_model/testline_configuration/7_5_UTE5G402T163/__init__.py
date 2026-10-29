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
from taf.config.testline.pdu import PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import TopYoung, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek, TafUeFastmile
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer,TafUeAppServer
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
from taf.config.testline.lmi import LMI, Local

__maintainer__ = "Jerry"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_02@internal.nsn.com"
__email__ = "jerry.wu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# PB INFO of ENB IS NOT CORRECT #

# #5GRU_0 for cloudBTS
_ru_pdu = TopYoung(addr="10.71.196.22", port_numbers=[2,6])

_ru_lmi_pc_RU = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.47", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi_RU = LMI(product_code="",
              host=_ru_lmi_pc_RU,
              uart_mapping=[Local(port="COM4")])


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),    
    lmp_connection=SshServiceDetails(
        addr="10.0.176.47", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQHC,
    serial_number="1M231100808",
    lmi=_ru_lmi_RU
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),    
    lmp_connection=SshServiceDetails(
        addr="10.0.176.47", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AQHC,
    serial_number="1M231100807",
    lmi=_ru_lmi_RU
)

#9217
_pdu_1 = TopYoung(addr="10.71.196.21", port_numbers=[4])

_fsp_1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIO",
#    hardware_version="475266A.101",
#    serial_number="L1204104720",
)


_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[4],
    hardware_type="ASIL",
#    hardware_version="474767A.101",
#    serial_number="L1212006760",
)

_rmod_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type="AQHC",
)

_enb_sbts_1 = RealEnb(
#    system_module=[_common_unit_1],
    system_module=Airscale(common_units=[_common_unit_1]),
    rms=[_rmod_1],
    oam_ip=NetworkAddress("192.168.255.129"),
    instance_id=163,
    global_bts_id=163,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.71.218.176", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=42263,
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/usr/bin/iperf",
    port=42264,
)
_appserver = AppServer(_iperf_details_on_appserver)

# MTK
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/MTK/Item.3_NR16.R2.MP.W22.18.p1_MT6298_DONGLE(NLWCG_SAP_R16)_bin/MDDB_MT6298_S00_NR16_R2_MP_W22_18_P1.EDB",
    log_filter="2.Gen98_Default_Standard",
    imei="12345678901234",
    imsi="262033100012810",
    apn_url="dxdata2",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)

#MTK_LTE
_mtk_LTE_host_ssh = SshServiceDetails(
    addr="10.71.218.46", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk_LTE = IperfDataTransferDetails(
    ssh_connection_details=_mtk_LTE_host_ssh,
    network_interface_address="",
    iperf_path="C:/Tool/iperf-2.0.9-win64/iperf",
    port="47163",
)

_mtk_lte = MediaTek(
    ssh_connection_details=_mtk_LTE_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:\MTK\Item.3_NR16.R2.MP.W22.18.p1_MT6298_DONGLE(NLWCG_SAP_R16)_bin\MDDB_MT6298_S00_NR16_R2_MP_W22_18_P1.EDB",
    log_filter="2.Gen98_Default_Standard",
    imei="12345678901234",
    imsi="262033032995919",
    apn_url="dxdata4",
    iperf_details=_iperf_details_on_mtk_LTE,
    capabilities=["LTE", "mtk_lte"],
#    capabilities=["REAL_MEDIATEK_UE","mtk_lte"],
)


#CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
#    binary_path="/home/vrf3_sg2/cpe_iperf/iperf",
    binary_path="/usr/bin/iperf",
    ports=[42163, 42164],
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
    ue_pc_address="10.71.218.55",
    root_password="c22ae7525ba2",
    ue_manage_ip="192.168.1.1",
    serial_number="FSH2112001A9",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=6868,
    version="3.1",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.22", hardware_type="ABIO", rus=[_ru1])
_capacity_unit1 = CapacityUnit(addr="192.168.253.22", hardware_type="ABIO", rus=[_ru2])
_capacity_unit2 = CapacityUnit(addr="192.168.253.26", hardware_type="ABIO", rus=[_ru1])
_capacity_unit2 = CapacityUnit(addr="192.168.253.26", hardware_type="ABIO", rus=[_ru2])

_du_pdu = TopYoung(addr="10.71.196.21", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit1, _capacity_unit2],
    pdu_port=_du_pdu.pdu_ports[4],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=5),
        target=Endpoint(unit=_ru2, label="SFP", port_id=3),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit2, label="SFP", port_id=1),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit2, label="SFP", port_id=5),
        target=Endpoint(unit=_ru1, label="SFP", port_id=3),
    ),
]

_du = DU(
    airscale=_airscale, rus=[_ru1,_ru2], f1_m_ip_addr="10.71.211.138", cablinks=_ru_cablinks
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="192.168.255.129",
        vlan_id=None,
        routing=RoutingInformation(gateway="192.168.255.1", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.211.138",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.211.138",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.211.138",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=163, global_bts_id=163)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata4"),
]
_core = RealCore(pdns=_pdns, mcc=262, mnc=3)

# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.41", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASILL_ABIOB1B2_AQHC"

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    ues=[_mtk,_fastmile,_mtk_lte],
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)