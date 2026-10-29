import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import TopYoung,FACOM
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import (
    EPCSim,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer

# from taf.config.testline.attenuator import HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdn import PDN, PDPTypes


__maintainer__ = "Guorong Song"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "guorong.song@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.54", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.53", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.221.135", username="haijtest", password="Nokia@12345"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.108.221.135", username="haijtest", password="Nokia@12345"
)

# 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[1])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[1],
)

# #RealEnb
_real_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = TopYoung(addr="10.71.197.59", port_numbers=[5])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[5],
    radio_type="AHFB",
)

_ru_2_pdu = TopYoung(addr="10.71.197.59", port_numbers=[6])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[6],
    radio_type="AHFB",
)

_ru_3_pdu = PBHBTE(addr="10.71.197.48", port_numbers=[2])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type="AWHQN",
)

_ru_4_pdu = PBHBTE(addr="10.71.197.58", port_numbers=[3])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_4_pdu.pdu_ports[3],
    radio_type="AHEGG",
)

_ru_5_pdu = PBHBTE(addr="10.71.197.47", port_numbers=[4])

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_5_pdu.pdu_ports[4],
    radio_type="AWHQN",
)
# _ru_2_pdu = FACOM(addr="10.57.249.6", port_numbers=[1])
#
# _ru_2 = RU(
#     ru_hw_group="hw_group",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="1.1.1.1", username="user", password="pass"
#     ),
#     lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
#     pdu_port=_ru_2_pdu.pdu_ports[1],
#     radio_type="AEHC",
# )

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")
_capacity_unit1 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = PBHBTE(addr="10.71.197.58", port_numbers=[1])
_gnb_pdu1 = PBHBTE(addr="10.71.197.56", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu1.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])
_airscale2 = Airscale(common_units=[_common_unit_1])

_du = DU(airscale=_airscale, rus=[_ru_1,_ru_2,_ru_4], f1_m_ip_addr="10.71.215.105")
_du2 = DU(airscale=_airscale2, rus=[_ru_3,_ru_5], f1_m_ip_addr="10.71.215.105")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.215.105",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.105", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.105", username="Nemuadmin", password="nemuuser"
    ),
)

_cu2 = CU(
    backhaul_site_oam_ip="192.168.255.119",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.119", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"
# classicalbts
# _classical_bts = ClassicalBts(dus=[_du], cu=_cu)
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11110", global_bts_id="11110"
)
_classical_bts2 = ClassicalBts(
    dus=[_du2], cu=_cu2, instance_id="11110", global_bts_id="11110"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.218.95", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.163.50", username="nokia", password="nokia123"
    addr="10.71.219.233",
    username="cmw_sg1",
    password="cm@1",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.233",
    iperf_path="iperf",
    port=51017,
)

_ue0 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="L8K5T19925005753",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Users/nokia5g/AppData/Local/Programs/Python/Python310",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100008480",
    # serial_com='12',
    # reset_interface='no',
    # enable_disable_cfun='yes',
    # processes_to_kill=['ttermpro', 'ATCom'],
    # ue_class = 'QualcommNoLicenseUe',
    # turn_off_on_firewall='yes',
    # diag_com='10',
    # iperf_directory ='adb shell /data/iperf'
)

# # for MTK UE, just a placeholder for now, TL config not supported yet.
# _mtk_appserver_ssh = SshServiceDetails(addr='10.110.149.24', username='srn', password='Nokia@123')  # wap1
# _iperf_details_on_appserver=IperfDataTransferDetails(
#     ssh_connection_details=_mtk_appserver_ssh,
#     network_interface_address='10.110.149.24',
#     iperf_path='iperf')
#
# _appserver = AppServer(_iperf_details_on_appserver)
# _mtk_host_ssh = SshServiceDetails(addr='10.57.130.109', username='nokia5G', password='noki@123')
# _iperf_details_on_mtk = IperfDataTransferDetails(
#     ssh_connection_details=_mtk_host_ssh,
#     network_interface_address="10.57.130.109",
#     iperf_path='iperf',
#     port=51201)
#
#
# _mtk_pdu = FACOM(addr='10.57.152.210', port_numbers=[2]).pdu_ports[2]
#
# _mtk = MediaTek(ssh_connection_details=_mtk_host_ssh,
#                    server_dir='c:/pyro_server',
#                    server_port=8080,
#                    edb_file_path=_db_file_path,
#                    imei='262032001000310',
#                    imsi='262032001000310',
#                    apn_url='wap1.nokia.com',
#                    iperf_details=_iperf_details_on_mtk,
#                    capabilities=['REAL_MEDIATEK_UE'])
# _mtk.inject_file = "C:/MTK_TA/sa_test_7880.tcl"
#
# _mtk.pdu = _mtk_pdu
# # DL server for 2PDU data transfer
# _wap1server = SshServiceDetails(addr='10.110.149.24', username='srn', password='Nokia@123')
# _wap2server = SshServiceDetails(addr='10.57.153.46', username='srn', password='Nokia@123')
# _mtk.wapserver = [_wap1server, _wap2server]

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, _host2],
    gnbs=[_classical_bts,_classical_bts2],
    core=_epc_sim,
    # enbs=[_lte_real_enb],
    ues=[_ue0],
    # appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
