# ##########################################################################################
#
#    7_20_UTESRANCLASSSV118_1  -  IV_PS_8_1  -  CV8_1
#
#    2026-01-12 11:30:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "Abderrahmane NEZROUk"
__team__ = "MN RAN RD VRF NPS 2"
__email__ = "abderrahmane.nezrouk@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import Connection, TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, FPFH, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.testline import TestLine
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Android, TafUeAndroid
from taf.config.testline.attenuator import AttenuationPort, Hytem
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline import PDNAndroidDetails, TafUeDataTransferProtocol
from taf.config.testline.nms import NetAct, NMS
# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]
_du1_pdu = FPFH(addr="10.0.117.92", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_ru1_pdu_gnb = FPFH(addr="10.28.1.85", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.28.1.86", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.28.1.87", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_rmod_gnb_5 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[3], radio_type="AHFII", ru_hw_group="NR_RADIO", serial_number="BL2222N4081"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[2], radio_type="AHLOA", ru_hw_group="NR_RADIO", serial_number="K9183926110"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2], radio_type="AHLOA", ru_hw_group="NR_RADIO", serial_number="K9183926255"
)
_rmod_gnb_6 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[3], radio_type="AHFII", ru_hw_group="NR_RADIO", serial_number="BL2222N407Z"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2], radio_type="AHLOA", ru_hw_group="NR_RADIO", serial_number="K9182044775"
)
_rmod_gnb_9 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1], radio_type="AEHC", ru_hw_group="NR_RADIO", serial_number="L1202707642"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[3], radio_type="AHFII", ru_hw_group="NR_RADIO", serial_number="BL2222N4082"
)
_rmod_gnb_8 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[1], radio_type="AEHC", ru_hw_group="NR_RADIO", serial_number="L1203007303"
)
_rmod_gnb_7 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[1], radio_type="AEHC", ru_hw_group="NR_RADIO", serial_number="L1202707624"
)
_fsp_gnb_3 = CapacityUnit(
    addr="192.168.253.44",
    hardware_type="ABIO",
    hardware_version="104",
    product_code="475266A.104",
    rus=[_rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6],
    serial_number="L1220808972",
)
_fsp_gnb_2 = CapacityUnit(
    addr="192.168.253.40",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_1, _rmod_gnb_3, _rmod_gnb_2],
    serial_number="L1223901091",
)
_fsp_gnb_1 = CapacityUnit(
    addr="192.168.253.36",
    hardware_type="ABIP",
    hardware_version="102",
    product_code="475792A.102",
    rus=[_rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9],
    serial_number="L1241104157",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_3, _fsp_gnb_2, _fsp_gnb_1],
    hardware_type="ASIL",
    hardware_version="474767A.103",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu.pdu_ports[1],
    serial_number="L1243200173",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23174, instance_id=23174)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.14.49.254/0"), v4="10.14.48.86", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.86", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.86", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.102.249/29", vlan_id="4001"),
    x2c=NetworkAddress(v4="10.0.102.249/29", vlan_id="4001"),
    x2u=NetworkAddress(v4="10.0.102.249/29", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23174, instance_id=23174)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_3],
    serial_number="L1173711185",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_1, _rmod_gnb_2],
    serial_number="L1173711195",
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_5, _rmod_gnb_6, _rmod_gnb_4],
    serial_number="L1173708791",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_2, _fsp_enb_1, _fsp_enb_3],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu.pdu_ports[2],
    serial_number="L1211107788",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22392,
    instance_id=22392,
    oam_ip=NetworkAddress(v4="10.14.48.84"),
    rms=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_5, _rmod_gnb_6, _rmod_gnb_4],
    system_module=_smod_enb_1,
)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.21", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.22", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
]
_app_server_1 = TafUeAppServer(app_server_name="APP_1",
    address="10.0.106.248",
    user="ran5g",
    password="nokia2018",
    bind_interface_ip=" 10.11.70.155",
    expected_prompt="ran5g@traffic100g-3"
    )

_app_server_2 = TafUeAppServer(app_server_name="APP_2",
    address="10.14.42.79",
    user="ran5g",
    password="nokia2018",
    bind_interface_ip=" 10.11.70.5",
    expected_prompt="ran5g@traffic-IV-PS106"
    )

_data_transfer_iperf = TafUeDataTransferProtocol(protocol_name="iperf",
                                                 app_server=_app_server_1,
                                                 interval=1,
                                                 binary_path="/data/data/com.nokia.android.application/iperf",
                                                 # interface_name="cischappe/rmnet_data0",
                                                 server_close_delay=50,
                                                 version=2,
                                                 )
_data_transfer_ping = TafUeDataTransferProtocol(protocol_name='ping',
                                                app_server=_app_server_2,
                                                interval=1)

_data_transfer_ftp = TafUeDataTransferProtocol(protocol_name='ftp',
                                               app_server=_app_server_1,
                                               interval=1)
_android_1 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.28.4.36", username="frps-ssdc", password="Pass4diskc!22"
    ),
    ue_pc_address="10.28.4.36",
    #R5CRC40HNRE
    serial_number="R5CRC2X2WCV",
    ue_pc_port="8080",
    # imsi="",
    # imei='35579646087648',
    voice_call_dialing_timeout="30",
    network_mode_switch_method="adb",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    qualcomm_prototype=False,
    airplane_mode_switcher_text="Airplane mode",
    airplane_mode_confirm_button_text='OK',
    capabilities=["REAL_ANDROID_UE_1", "REAL_UE"],
    processes_to_kill=['Vysor'],
)
_android_1.ue_type = "android"

_android_2 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.28.4.36", username="frps-ssdc", password="Pass4diskc!22"
    ),
    # c0972503
    ue_pc_address="10.28.4.36",
    serial_number="R5CT402XHBZ",
    ue_pc_port="8080",
    # imsi="",
    # imei='004403162101465',
    voice_call_dialing_timeout="30",
    network_mode_switch_method="adb",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    qualcomm_prototype=False,
    airplane_mode_switcher_text="Airplane mode",
    airplane_mode_confirm_button_text='OK',
    capabilities=["REAL_ANDROID_UE_2", "REAL_UE"],
    processes_to_kill=['Vysor'],
)
_android_2.ue_type = "android"

_android_3 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.28.4.36", username="frps-ssdc", password="Pass4diskc!22"
    ),
    ue_pc_address="10.28.4.36",
    serial_number="d94dfdb4",
    ue_pc_port="8080",
    # imsi="",
    imei='004403162101754',
    voice_call_dialing_timeout="30",
    network_mode_switch_method="adb",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    qualcomm_prototype=False,
    airplane_mode_switcher_text="Airplane mode",
    airplane_mode_confirm_button_text='OK',
    capabilities=["REAL_ANDROID_UE_3", "REAL_UE"],
    processes_to_kill=['Vysor'],
)
_android_3.ue_type = "android"
# NetAct Configuration
_nms_netact1028 = NMS(
    netact=NetAct(
        ssh_connections_info=SshServiceDetails(
            addr="10.41.148.135",
            username="omc",
            password="Medsql!_1893",
        ),
        https_main_info=HttpConnectionDetails(
            addr="srnclab1028lbwas.srnblr.nsn-rdnet.net",
        ),
    ),
)

netact_id = {
    "srnclab1028": {
        "node_ip": "10.41.148.135",
        "user": "omc",
        "password": "Medsql!_1893",
        "url": "https://srnclab1028lbwas.srnblr.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "Medsql!_1893",
        "mr": "MRC-COMMON/MR-COMMON/MRBTS-23174",
    },
}
_netact = NetAct(netact_id)
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSASA_ASIL_2xABIO_ABIP_3xAHFII_3xAHLOA_3xAEHC_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    ues=[_android_1, _android_2],
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1, _test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
