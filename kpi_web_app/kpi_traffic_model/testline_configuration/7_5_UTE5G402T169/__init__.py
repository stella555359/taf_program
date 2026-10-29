import os
from taf.config.testline.appserver import AppServer,TafUeAppServer
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import (
    Android,
    TafUeFastmile,
)  # added in taf.meta.5.4
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
# added in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    RU,
)
from taf.config.testline.attenuator import (
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.mcs import HBTE as HBTE_MCS
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.pdn import PDNTafUeAndroidDetails

__maintainer__ = "Helen.1.Chen"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "helen.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #attenuator
_hbte_params = {
    "ip_addr": "10.71.212.101",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

##HBTE_MCS
_hbte = HBTE_MCS(
    ip_addr="10.71.204.201",
    port="5000",
    mcs_port_numbers=list(range(1,17)),
    model="PPSAM-64X16-2.3-3.8-90-0.5-360-1-A",
)

##5GRU_1

_ru1_pdu = TopYoung(addr="10.71.196.18", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.158",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
)

##5GRU_2
_ru2_pdu = TopYoung(addr="10.71.196.18", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQY,
)

##5GRU_3
_ru3_pdu = TopYoung(addr="10.71.196.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQL,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2", port="42169"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/usr/bin/iperf",
    port=42169,
)

#UE-1 CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42169, 42269],
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
    ue_pc_address="10.0.176.57",
    root_password="3e3a2d826fec",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400626",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=2158,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

#UE-2 NR CPE
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.71.207.155",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.71.207.155",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42369, 42469],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile_2 = TafUeFastmile(
    com_port="6",
    ue_pc_address="10.0.176.66",
    root_password="EVVem9HnzPLpq3.N",
    ue_manage_ip="192.168.2.1",
    serial_number="LPL241800A95",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=3158,
    version="Receiver 5G19-A",
    default_user_password="WSxXHy+3D93K.C7.",
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

#UE-3 CPE
_fastmile_appserver_3 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.71.207.155",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.71.207.155",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42569, 42669],
)

_fastmile_data_transfer_3 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_3,
    interval=1,
    binary_path="iperf",
    version=1,
)
_fastmile_3 = TafUeFastmile(
    com_port="10",
    ue_pc_address="10.0.176.59",
    root_password="Xc4Uugnh@.V:CLrw",
    ue_manage_ip="192.168.3.1",
    serial_number="LPL241800B8C",
    data_transfer=[_fastmile_data_transfer_3],
    ue_pc_port=4158,
    version="Receiver 5G19-A",
    default_user_password="idu-XXcG77x:PgL_",
    capabilities=["REAL_FASTMILE_UE3", "nokia_fastmile"],
)

#UE-4 CPE
_fastmile_appserver_4 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42769, 42869],
)

_fastmile_data_transfer_4 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_4,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile_4 = TafUeFastmile(
    com_port="10",
    ue_pc_address="10.0.176.59",
    root_password="rzx9+xmq3Rf_YUDK",
    ue_manage_ip="192.168.4.1",
    serial_number="LPL24180091A",
    data_transfer=[_fastmile_data_transfer_4],
    ue_pc_port=4158,
    version="Receiver 5G19-A",
    default_user_password="3wLx.NhsFwXyZK5z",
    capabilities=["REAL_FASTMILE_UE4", "nokia_fastmile"],
)

#UE-5 CPE
_fastmile_appserver_5 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42969, 42069],
)

_fastmile_data_transfer_5 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_5,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile_5 = TafUeFastmile(
    com_port="10",
    ue_pc_address="10.0.176.58",
    root_password="2d4ab6b2a864",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214004D9",
    data_transfer=[_fastmile_data_transfer_5],
    ue_pc_port=5158,
    version="3.2",
    default_user_password="Hp@9wYs2d%t7",
    capabilities=["REAL_FASTMILE_UE5", "nokia_fastmile"],
)

# SIGSPARK
_appserver_ip_addr1 = "10.57.191.195"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=42169,
)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.204.205", username="spark", password="spark"
)

_IMSI_1 = "262033100010730"
_IMSI_3 = "262033100012812"
_IMSI_5 = "262033032996906"
_IMSI_7 = "262033100011505"

_spark_server_dir = "C:\Program Files (x86)\Spark1.1.2011.2\Bin\Spark.exe"

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239004",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239004",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_3,
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239004",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_5,
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239004",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_7,
)

#MTP8850
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5",
    address="10.57.191.249",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45001,45023,45024],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata1", apnName="dxdata1", apnType=["DEFAULT"]
)

_MTPx85 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.233", username="nokia5G", password="noki@123"
    ),
    ue_pc_address="10.0.176.233",
    proxy_mngr_port="9955",
    serial_number="69fab98e",
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
    capabilities=["REAL_UE", "qualcomm"],
)

##DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.211.149", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = TopYoung(addr="10.71.196.14", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.211.149")

##CU

_cu = CU(
    backhaul_site_oam_ip="10.71.211.149",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.149", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.149", username="Nemuadmin", password="nemuuser"
    ),
)

##classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=169, global_bts_id=169)

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.41", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_iperf_details = _iperf

_appserver = AppServer(_iperf_details)

##cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_AEQY_eCPRI"

tl = TestLine(
    test_pc=_host,
    ues=[_fastmile_1,_fastmile_2,_fastmile_3,_fastmile_4,_fastmile_5,_sigspark_1,_sigspark_3,_sigspark_5,_sigspark_7,_MTPx85],
    gnbs=[_classical_bts],
    appserver=_appserver,
    attenuator=[_attenuator],
    mcses=[_hbte],
    tl_cloud_topology=_tl_cloud_topology,
)
