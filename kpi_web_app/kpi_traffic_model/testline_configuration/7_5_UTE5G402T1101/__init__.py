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
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
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

from taf.config.testline.attenuator import TopYoung, AttenuationPort, HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdn import PDN, PDPTypes


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
        addr="10.57.167.166", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)
_pdns = [PDN(PDPTypes.IPV4V6.value, "wap1.nokia.com")]
# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="262", mnc="03", pdns=_pdns)
# 4GRU for RealEnb
_ru_enb_pdu = FACOM(addr="10.57.241.218", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[1],
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.155", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.236.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_attenuator1 = HBTE(
    ip_addr="10.101.36.53",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator2 = HBTE(
    ip_addr="10.101.36.52",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru1_pdu = PBHBTE(addr="10.68.87.19", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type="AWHHJ",
)

_ru2_pdu = PBHBTE(addr="10.68.87.19", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.6",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type="AWHHJ",
)

_ru3_pdu = PBHBTE(addr="10.68.87.19", port_numbers=[4])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.10",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type="AWHHJ",
)

_ru4_pdu = PBHBTE(addr="10.68.87.12", port_numbers=[5])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.154",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
    pdu_port=_ru4_pdu.pdu_ports[5],
    radio_type="AVQL",
)

_ru5_pdu = PBHBTE(addr="10.68.87.10", port_numbers=[6])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.158",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    attenuation_ports=[
        _attenuator2.attenuator_ports[1],
        _attenuator2.attenuator_ports[2],
        _attenuator2.attenuator_ports[3],
        _attenuator2.attenuator_ports[4],
    ],
    pdu_port=_ru5_pdu.pdu_ports[6],
    radio_type="AVQE",
)

_ru6_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[8])

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.162",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    attenuation_ports=[
        _attenuator2.attenuator_ports[9],
        _attenuator2.attenuator_ports[10],
        _attenuator2.attenuator_ports[11],
        _attenuator2.attenuator_ports[12],
    ],
    pdu_port=_ru6_pdu.pdu_ports[8],
    radio_type="AWPQZ",
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

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = PBHBTE(addr="10.68.87.21", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6], f1_m_ip_addr="10.101.52.98")


##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.52.98",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.98", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"
# classicalbts
# _classical_bts = ClassicalBts(dus=[_du], cu=_cu)
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11112", global_bts_id="11112"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.164", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki_sg1@123!"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51040,
)

_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9YS0220108006550",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100007892",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34",
    username="cmw_sg1",
    password="Noki_sg1@123!",
    port=51040,
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=51040,
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 51040

# CI_Detail_UE_Type='Huawei Honor 30s'
_ue0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.53", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20903003352",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_HONOR30s", "huawei"],
    imsi="460028001006161",
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
    gnbs=[_classical_bts],
    core=_epc_sim,
    # enbs=[_lte_real_enb],
    ues=[_sigspark],
    appserver=_appserver,
    attenuator=[_attenuator1, _attenuator2],
    tl_cloud_topology=_tl_cloud_topology,
)
