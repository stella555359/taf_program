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
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

# from taf.config.testline.attenuator import HBTE
from taf.config.testline.appserver import AppServer


__maintainer__ = "Liu Tiffany"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "tiffany.liu@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.66", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_host1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.67", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

# 4GRU for RealEnb1
_ru_enb_1_pdu = HBTE(addr="10.101.45.3", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb_1 = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_1_pdu.pdu_ports[1],
)
# 4GRU for RealEnb2
_ru_enb_2_pdu = HBTE(addr="10.101.45.3", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb_2 = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_2_pdu.pdu_ports[6],
)


# #RealEnb1
_real_enb_1_pdu = TopYoung(addr="10.101.45.2", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_1_pdu.pdu_ports[1],
)

_real_enb_1 = Airscale(common_units=[_common_unit_1])
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=_ru_enb_1)

# #RealEnb2
_real_enb_2_pdu = TopYoung(addr="10.101.45.2", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.204", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_2_pdu.pdu_ports[5],
)

_real_enb_2 = Airscale(common_units=[_common_unit_2])
_lte_real_enb_2 = RealEnb(airscale=_real_enb_2, rms=_ru_enb_2)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.101.45.3", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type="AHLOA",
)

_ru_2_pdu = HBTE(addr="10.101.45.3", port_numbers=[4])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[4],
    radio_type="AHLOA",
)

_ru_3_pdu = TopYoung(addr="10.101.45.5", port_numbers=[2])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type="AHLOA",
)
_ru_4_pdu = HBTE(addr="10.101.45.10", port_numbers=[4])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_4_pdu.pdu_ports[4],
    radio_type="AZQG",
)
_ru_5_pdu = HBTE(addr="10.101.45.3", port_numbers=[6])

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_5_pdu.pdu_ports[6],
    radio_type="AHEC",
)
_ru_6_pdu = TopYoung(addr="10.101.45.5", port_numbers=[3])

_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_6_pdu.pdu_ports[3],
    radio_type="AHCA",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = TopYoung(addr="10.101.45.2", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6],
    f1_m_ip_addr="10.101.48.199",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.48.199",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.199", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.199", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"
# classicalbts
# _classical_bts = ClassicalBts(dus=[_du], cu=_cu)
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10275", global_bts_id="10275"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.57.130.109", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki@123"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=10000,
)

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9YS0220108006550",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460028001006216",
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
    test_pcs=[_host, _host1],
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb_1,_lte_real_enb_2],
    ues=[_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
)
