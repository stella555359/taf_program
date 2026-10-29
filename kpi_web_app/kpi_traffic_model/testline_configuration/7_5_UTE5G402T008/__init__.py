import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Prisma, MediaTek
from taf.config.testline.ue import Android
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "JIANHUA ZHU"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "jianhua.1.zhu@nokia-sbell.com"


## common
# __all__ = ["tl"]
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.117", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)


##GNB1
##5GRU for TL08 classicalBTS
_ru_1_pdu = PBHBTE(addr="10.101.45.75", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type="AEQQ",
)


# #DU for TL08 classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = PBHBTE(addr="10.101.45.74", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_1], f1_m_ip_addr="10.101.49.190")


##CU for TL08 classicalBTS
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.190", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.190", username="Nemuadmin", password="nemuuser"
    ),
)

## TL08 classicalBTS
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="1908", global_bts_id="1908"
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.42", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki@123"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51205,
)
# CI_Detail_UE_Type = "Huawei Honor 30s"
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="QKXUT20519006740",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["cell_Mapping: [1]", "huawei"],
    imsi="460023032996639",
)

# for Honor UL traffic
_appserver = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="QKXUT20519006740",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023032996639",
    capabilities=["huawei"],
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.34",
    user="cmw_sg1",
    password="Noki_sg1@123!",
    bind_interface_ip="10.57.163.34",
    expected_prompt="[cmw_sg1@smw_sg1 ~]$ ",
    binary_path="/home/cmw_sg1/taf_debug/iperf",
    ports=[53318, 54318],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="3",
    ue_pc_address="10.57.195.117",
    root_password="6bba79d25322",
    ue_manage_ip="10.101.49.172",
    serial_number="LPL2214005CE",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    # ues=[_prisma],
    ues=[_fastmile_1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
