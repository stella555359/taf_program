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

__maintainer__ = "Guo Wei"
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
__email__ = "wei.guo@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


##Test PC/UTE
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.139", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="270",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)


# ##Prisma
# _airmosaic_ssh = SshServiceDetails(addr='10.57.152.84', username='nokia', password='Tester123')
# _airmosaic_harness = HttpConnectionDetails(addr='10.57.152.84', port=8090)
# _lsu_uu_ssh = SshServiceDetails(addr='10.57.152.83', username='user', password='user')
# _tstm_uu_ssh = SshServiceDetails(addr='10.57.152.83', username='user', password='user')
#
#
# _prisma = Prisma(airmosaic_ssh_connection_details=_airmosaic_ssh,
#                     airmosaic_harness_connection_details=_airmosaic_harness,
#                     lsu_uu_ssh_connection_details=_lsu_uu_ssh,
#                     tstm_uu_ssh_connection_details=_tstm_uu_ssh
#                     )

##RealEnb
_real_enb_pdu = PBHBTE(addr="10.101.45.80", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.217", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

## 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="0.0.0.0", port_numbers=[2])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)


##GNB1
##5GRU for TL2201 classicalBTS
_ru_1_pdu = PBHBTE(addr="10.101.45.80", port_numbers=[6])
_ru_2_pdu = PBHBTE(addr="10.101.45.82", port_numbers=[1])
_ru_3_pdu = PBHBTE(addr="10.101.45.82", port_numbers=[4])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[6],
    radio_type="AWHQN",
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type="AWHQN",
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[4],
    radio_type="AWHQN",
)

# #DU for TL2201 classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = PBHBTE(addr="10.101.45.80", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.101.49.217")


##CU for TL202 classicalBTS
_cu = CU(
    backhaul_site_oam_ip="10.101.49.217",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.217", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.217", username="Nemuadmin", password="nemuuser"
    ),
)

## TL2201 classicalBTS
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="11107", global_bts_id="11107")


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

##SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.44", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki@123!"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51202,
)

##CI_Detail_UE_Type = "Huawei Honor 30s"
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="QKXUT20422012893",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["cell_Mapping: [1]", "huawei"],
    imsi="460028001006221",
)

##for Honor UL traffic
_appserver = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="QKXUT20422012893",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460028001006221",
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
    ue_pc_address="10.57.167.139",
    root_password="235a9fd2e7dc",
    ue_manage_ip="10.101.39.100",
    serial_number="LPL221400493",
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
    enbs=[_lte_real_enb],
    ues=[_fastmile_1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
