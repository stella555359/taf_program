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
from taf.config.testline.pdu import TopYoung, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek, TafUeFastmile
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.testpc import TestPc, Connection
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
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "jerry.wu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host


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
_ru_pdu1 = HBTE(addr="10.57.251.234", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu2 = HBTE(addr="10.57.251.237", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu3 = HBTE(addr="10.57.251.235", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu4 = HBTE(addr="10.57.251.253", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

#lmi_info
_ru_lmi_pc_RU5 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.150.16", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi_RU5 = LMI(product_code="",
              host=_ru_lmi_pc_RU5,
              uart_mapping=[Local(port="COM3")])



_asiru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    radio_type=RadioTypes.APHG,
)

_ru1 = RU(
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
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AEQC,
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
    pdu_port=_ru_pdu2.pdu_ports[3],
    radio_type=RadioTypes.AHCA,
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
    pdu_port=_ru_pdu1.pdu_ports[6],
    radio_type=RadioTypes.AQHC,
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu4.pdu_ports[5],
    radio_type=RadioTypes.AVHA,
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
    pdu_port=_ru_pdu2.pdu_ports[5],
    radio_type=RadioTypes.AHCA,
)

_ru7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
    radio_type=RadioTypes.AHCA,
)

_ru8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    radio_type=RadioTypes.AHCA,
)

_ru9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
    radio_type=RadioTypes.AHEH,
)



# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.20", username="mmw_sg2_3", password="mm@2@3"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.20",
    iperf_path="/usr/bin/iperf",
    port=42163,
)
_appserver = AppServer(_iperf_details_on_appserver)

#CPE1
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.195",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.195",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42163, 43163],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.150.224",
    root_password="643ab2e2a586",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400634",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=1311,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile2 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.130.47",
    root_password="d52a3932d894",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL22140062E",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=1312,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


_fastmile_data_transfer_3 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile3 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.150.225",
    root_password="595aaa22b757",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214005F2",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=1313,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)




# #DU_0 for cloudlBTS

_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(addr="192.168.253.22", rus=[_asiru1, _ru2, _ru3, _ru6])
_gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(addr="192.168.253.22", rus=[_ru1, _ru4, _ru5, _ru7, _ru8, _ru9])

_du_pdu = TopYoung(addr="10.71.196.21", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
    addr="10.57.228.98", username="toor4nsn", password="oZPS0POrRieRtu"
),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_du_pdu.pdu_ports[4],
    hardware_type="ASIM",
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_right],
    pdu_port=_du_pdu.pdu_ports[4],
    hardware_type="ASIM",
)

_airscale1 = Airscale(common_units=[_common_unit_0])

_airscale2 = Airscale(common_units=[_common_unit_1])


_du1 = DU(
    airscale=_airscale1, rus=[_asiru1, _ru2, _ru3, _ru6], f1_m_ip_addr="10.57.228.98",
)

_du2 = DU(
    airscale=_airscale2, rus=[_ru1, _ru4, _ru5, _ru7, _ru8, _ru9], 
)

# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.228.98",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.98", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.228.98",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.228.98",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.228.98",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.97", ip_prefix_length=27),
    ),
)

#enb
_pdu_1 = TopYoung(addr="10.57.251.237", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_fsp_1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIQ",
    hardware_version="476397A.102",
    serial_number="L1233105858",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="10.57.228.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[1],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    serial_number="L1233505175",
)

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AHCA,
    serial_number="1M192217752",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    pdu_port=_ru_pdu2.pdu_ports[5],
)

_rmod_2 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AQHC,
    serial_number="1M192217752",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    pdu_port=_ru_pdu1.pdu_ports[6],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1, _rmod_2],
    oam_ip=NetworkAddress("10.57.228.98"),
    instance_id=131,
    global_bts_id=131,
    airscale=_airscale1,
)


# classicalbts------------------------------------------------
_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu, instance_id=131, global_bts_id=131)
_classical_bts2 = ClassicalBts(dus=[_du2], cu=_cu, instance_id=131, global_bts_id=131)

#test pc
_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.118", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts1.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.25", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts2.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata4"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MTK_SA_ASILL_ABIOB1_AQHC"

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2],
#    test_pcs=[_docker_pc, _tce_pc],
    ues=[_fastmile1, _fastmile2, _fastmile3],
    gnbs=[_classical_bts1, _classical_bts2],
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)
