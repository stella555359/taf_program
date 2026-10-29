import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.connection_details import (   
    SshServiceDetails, 
    HttpConnectionDetails,
##    BmcConnectionDetails,
##    OpenStackConnectionDetails,
##    IperfDataTransferDetails,
)

# from taf.config.testline.attenuator import HBTE
##from taf.config.testline.appserver import AppServer
##from taf.config.testline import LicenseKeeper

__maintainer__ = "Liu Tiffany"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "tiffany.liu@nokia-sbell.com"
# _db_file_path = 'D:/MTK/SW/42p1/MDDB_MT6297_S00_VMOLY_W19_42_P1.EDB'

# _db_file_path = 'D:/MTK/SW/W19.43.P3/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB'
# _db_file_path = 'C:/tl201pc/VMOLY.W19.43.p3/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB'
# _db_file_path = 'C:/tl201pc/Build20191227/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB'

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.68", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.69", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
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


# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.101.45.10", port_numbers=[6])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[6],
)

# #RealEnb
_real_enb_pdu = TopYoung(addr="10.101.45.2", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.201", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.101.45.3", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="root", password="none"),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type="AHLOA",
)

_ru_2_pdu = HBTE(addr="10.101.45.3", port_numbers=[3])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="root", password="none"),
    pdu_port=_ru_2_pdu.pdu_ports[3],
    radio_type="AHLOA",
)

_ru_3_pdu = HBTE(addr="10.101.45.3", port_numbers=[5])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="root", password="none"),
    pdu_port=_ru_3_pdu.pdu_ports[5],
    radio_type="AHLOA",
)

_ru_4_pdu = HBTE(addr="10.101.45.4", port_numbers=[4])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="root", password="none"),
    pdu_port=_ru_4_pdu.pdu_ports[4],
    radio_type="AHFIB",
)

_ru_5_pdu = HBTE(addr="10.101.45.4", port_numbers=[2])

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="root", password="none"),
    pdu_port=_ru_5_pdu.pdu_ports[2],
    radio_type="AHFIB",
)

_ru_6_pdu = HBTE(addr="10.101.45.4", port_numbers=[1])

_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="root", password="none"),
    pdu_port=_ru_6_pdu.pdu_ports[1],
    radio_type="AZQS",
)

_ru_8_pdu = HBTE(addr="10.101.45.4", port_numbers=[1])

_ru_8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="),
    pdu_port=_ru_8_pdu.pdu_ports[1],
    radio_type="AEHC",
)

_ru_9_pdu = HBTE(addr="10.101.45.4", port_numbers=[1])

_ru_9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="),
    pdu_port=_ru_9_pdu.pdu_ports[1],
    radio_type="AEHC",
)

_ru_10_pdu = HBTE(addr="10.101.45.4", port_numbers=[1])

_ru_10 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="),
    pdu_port=_ru_10_pdu.pdu_ports[1],
    radio_type="AEHC",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.101.45.10", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_8, _ru_9, _ru_10],
    f1_m_ip_addr="10.101.48.201",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.48.201",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.201", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.201", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10541", global_bts_id="10541"
)

_2_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10541", global_bts_id="10541"
)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.34",
    user="cmw_sg1",
    password="Noki_sg1@123!",
    bind_interface_ip="10.57.163.34",
    expected_prompt="[cmw_sg1@smw_sg1 ~]$ ",
    binary_path="/home/cmw_sg1/taf_debug/iperf",
    ports=[51318, 52318],
)
_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)
_fastmile_1 = TafUeFastmile(
    com_port="33",
    ue_pc_address="10.101.47.91",
    root_password="d5da66f2833b",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214005FA",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)
# SIGSPARK
##_ue_host_ssh = SshServiceDetails(
##    addr="10.101.47.91", username="nokia5G", password="noki@123"
##)

##_spark_appserver_ssh = SshServiceDetails(
##    addr="10.57.163.34", username="cmw_sg1", password="Noki_sg1@123!"
##)
##_iperf_details_on_appserver = IperfDataTransferDetails(
##    ssh_connection_details=_spark_appserver_ssh,
##    network_interface_address="10.57.163.34",
##    iperf_path="iperf",
##    port=10000,
##)
# spark license
##_licensekeeper = LicenseKeeper(username="shuhui.lou@nokia-sbell.com", password="123456")
# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
##_sigspark = Android(
##    ssh_connection_details=_ue_host_ssh,
##    serial_number="9YS0220414000564",
##    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
##    python_path="C:/Python27",
##    iperf_details=_iperf_details_on_appserver,
##    imsi="460023100010697",
##    capabilities=["huawei_sigspark"],
##    licensekeeper=_licensekeeper,
##)


tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, _host_2],
    gnbs=[_classical_bts, _2_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
#    ues=[_sigspark],
    ues=[_fastmile_1],
    tl_cloud_topology=_tl_cloud_topology,
)
