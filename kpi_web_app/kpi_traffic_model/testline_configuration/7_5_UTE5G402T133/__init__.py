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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE, TopYoung
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
        addr="10.57.159.25", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

# #5GRU_0 for cloudBTS
_ru_pdu1 = TopYoung(addr="10.57.251.234", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu2 = TopYoung(addr="10.57.251.235", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu2.pdu_ports[5],
    radio_type=RadioTypes.AVQL,
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AQHC,
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu1.pdu_ports[6],
    radio_type=RadioTypes.AQHC,
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.AHCA,
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
    radio_type=RadioTypes.AHCA,
)

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
    radio_type=RadioTypes.AHCA,
)

#9217
_pdu_1 = HBTE(addr="10.57.251.237", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="10.57.228.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_pdu_1.pdu_ports[4],
    hardware_type="ASOH",
    hardware_version="476255A.101",
    serial_number="L1241401977",
)

_ru_pdu = TopYoung(addr="10.57.251.235", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AVQL,
    serial_number="L1233203408",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22", username="rfsw", password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0="
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.57.228.99"),
    instance_id=133,
    global_bts_id=133,
)



# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.20", username="mmw_sg2_3", password="mm@2@3"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.71.218.176", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=43133,
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.20",
    iperf_path="/usr/bin/iperf",
    port=42133,
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
    address="10.57.162.2",
    user="mmw_sg2",
    password="mm@2",
    bind_interface_ip="10.57.162.2",
    expected_prompt="[mmw_sg2@appserver ~]$",
    binary_path="/home/mmw_sg2/cpe_iperf/iperf",
    ports=[42163, 43163],
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
    addr="10.57.228.99", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_du_pdu = TopYoung(addr="10.57.251.237", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    )
]

_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6], f1_m_ip_addr="10.57.228.99", cablinks=_ru_cablinks
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.228.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.99", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.228.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.228.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.228.99",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=133, global_bts_id=133)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata4"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MTK_SA_ASILL_ABIOB1_AQHC"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    ues=[_mtk,_fastmile,_mtk_lte],
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)
