# ##########################################################################################
#
#    iv_ps337  -  IV_PS_337  -  CV337
#
#    2025-06-10 09:55
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "Abderrahmane NEZROUk"
__team__ = "MN RAN RD VRF NPS 1"
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
from taf.config.testline.flexi import Flexi
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import RealCore4G
from taf.config.testline.testline import TestLine
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Android
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline import PDNAndroidDetails, TafUeDataTransferProtocol
from taf.config.testline.ue import Android, TafUeAndroid


# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(addr="10.0.117.149", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.117.184", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.185", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_rmod_gnb_4 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[5], radio_type="AVQE", ru_hw_group="NR_RADIO", serial_number="L1233108187"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4], radio_type="AVQE", ru_hw_group="NR_RADIO", serial_number="L1242504680"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4], radio_type="AVQE", ru_hw_group="NR_RADIO", serial_number="L1242504679"
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[],
    hardware_type="ASOG",
    hardware_version="476254A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[2],
    serial_number="L1243405084",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=337, instance_id=337)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="1None"), v4="10.14.48.34", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.34", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.34", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.112.218/29", vlan_id="4005"),
    x2c=NetworkAddress(v4="10.0.112.217/29", vlan_id="4005"),
    x2u=NetworkAddress(v4="10.0.112.217/29", vlan_id="4005"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=337, instance_id=337)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.113", password="uteUTE!", port=22, username="ute"
    ),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb]

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
        addr="10.0.96.55", username="frps-ssdc", password="Pass4diskc!22"
    ),
    ue_pc_address="10.0.96.55",
    serial_number="a6efe740",
    ue_pc_port="8080",
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
        addr="10.0.96.55", username="frps-ssdc", password="Pass4diskc!22"
    ),
    ue_pc_address="10.0.96.55",
    serial_number="519f111b",
    ue_pc_port="8080",
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

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASOG_3xAVQE_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    ues=[_android_1, _android_2],
    tl_cloud_topology=_tl_cloud_topology,
)
