# ##########################################################################################
#
#    7_20_UTE5GCLASSSV066  -  IV_PS_066  -  CV066
#
#    2023-12-04 22:11:53
#    __init__.py generator (version 1.0 of 21/09/2023).
#
# ##########################################################################################

__maintainer__ = "A NEZROUK"
__team__ = "MN RAN Pz NPS SG2"
__email__ = "Abderrahmane.nezrouk@nokia.com"

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
from taf.config.testline.core import RealCore4G
from taf.config.testline.testline import TestLine
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Prisma
from taf.config.testline.ue import Android
from collections import OrderedDict
from taf.config.testline.gnb.du import Cablink, Endpoint

# ##############################################################################
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ##############################################################################

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))
cfg_dir = os.path.dirname(os.path.abspath(__file__))
__all__ = ["tl"]

_du1_pdu_gnb = FPFH(
    addr="10.0.117.83", login="admin", password="admin", port_numbers=[4]
)
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.146",
    login="admin",
    password="admin",
    port_numbers=[1, 2, 3, 4, 5, 6],
)
_ru2_pdu_gnb = FPFH(
    addr="10.0.117.146",
    login="admin",
    password="admin",
    port_numbers=[1, 2, 3, 4, 5, 6],
)
_ru3_pdu_gnb = FPFH(
    addr="10.0.117.147",
    login="admin",
    password="admin",
    port_numbers=[1, 2, 3, 4, 5, 6],
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193501015",
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193400563",
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV194100647",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1204104644",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        password="oZPS0POrRieRtu",
        port=22,
        username="toor4nsn",
    ),
    pdu_port=_du1_pdu_gnb.pdu_ports[4],
    serial_number="DH201860957",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(
    airscale=_smod_gnb_1,
    global_bts_id=23131,
    instance_id=66,
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"),
        v4="10.14.48.66",
        vlan_id="1000",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.66", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.66", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.6.130/29", vlan_id="4002"),
    x2c=NetworkAddress(v4="10.28.6.129/29", vlan_id="4002"),
    x2u=NetworkAddress(v4="10.28.6.130/29", vlan_id="4002"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23131, instance_id=66)
_airmosaic_ssh = SshServiceDetails(
    addr="10.0.100.201", username="localuser", password="10c@1user"
)
_airmosaic_harness = HttpConnectionDetails(addr="10.0.100.201", port=8090)
_lsu_uu_ssh = SshServiceDetails(addr="10.14.58.103", username="user", password="user")
_tstm_uu_ssh = SshServiceDetails(addr="10.14.58.103", username="user", password="user")

_ue_host_iperf_ssh = SshServiceDetails(
    addr="10.14.59.168", username="ftp", password="ftp"
)
# UE0, DL Port (1st UE)
_ue0_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.203",
    iperf_path=None,
    port="34203",
    ports=[],
    iperf_bind_ue_ip="",
)
_ue0 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue0_host_iperf_details,
)
# UE1, DL Port (2nd UE)
_ue1_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.204",
    iperf_path=None,
    port="34204",
    ports=[],
    iperf_bind_ue_ip="192.168.203.204",
)
_ue1 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue1_host_iperf_details,
)
# UE2, DL Port (3th UE)
_ue2_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.205",
    iperf_path=None,
    port="34205",
    ports=[],
    iperf_bind_ue_ip="192.168.203.205",
)
_ue2 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue2_host_iperf_details,
)
# UE3, DL Port (4th UE)
_ue3_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.206",
    iperf_path=None,
    port="34206",
    ports=[],
    iperf_bind_ue_ip="192.168.203.206",
)
_ue3 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue3_host_iperf_details,
)
# UE4, DL Port (5th UE)
_ue4_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.207",
    iperf_path=None,
    port="34207",
    ports=[],
    iperf_bind_ue_ip="192.168.203.207",
)
_ue4 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue4_host_iperf_details,
)
# UE5, DL Port (6th UE)
_ue5_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.208",
    iperf_path=None,
    port="34208",
    ports=[],
    iperf_bind_ue_ip="192.168.203.208",
)
_ue5 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue5_host_iperf_details,
)
# UE6, DL Port (7th UE)
_ue6_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.209",
    iperf_path=None,
    port="34209",
    ports=[],
    iperf_bind_ue_ip="192.168.203.209",
)
_ue6 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue6_host_iperf_details,
)
# UE7, DL Port (8th UE)
_ue7_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.210",
    iperf_path=None,
    port="34210",
    ports=[],
    iperf_bind_ue_ip="192.168.203.210",
)
_ue7 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue7_host_iperf_details,
)
# UE8, DL Port (9th UE)
_ue8_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.211",
    iperf_path=None,
    port="34211",
    ports=[],
    iperf_bind_ue_ip="192.168.203.211",
)
_ue8 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue8_host_iperf_details,
)
# UE9, DL Port (10th UE)
_ue9_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.212",
    iperf_path=None,
    port="34212",
    ports=[],
    iperf_bind_ue_ip="192.168.203.212",
)
_ue9 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue9_host_iperf_details,
)
# UE10, DL Port (11th UE)
_ue10_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.70.0.213",
    iperf_path=None,
    port="34213",
    ports=[],
    iperf_bind_ue_ip="192.168.203.213",
)
_ue10 = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue10_host_iperf_details,
)
_realcore = RealCore4G(mcc="540", mnc="1")

# Appserver / UL ports
_appserver_ssh = AppServer(
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.14.42.92", username="ran5g", password="nokia2018Ne!"
        ),
        network_interface_address="10.11.70.16",
        iperf_path=None,
        port="33203",
    )
)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            device=_gnb_sbts_1.dus[0].airscale.common_units[0],
            interface="eth1",
            interface_type="lmp",
        ),
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.112",
        password="uteUTE!",
        port=22,
        username="ute",
    ),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSA_ASIB_ABIO_3xAEQN_UTECA"
tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    appserver=_appserver_ssh,
    ues=[_ue0, _ue1, _ue2, _ue3, _ue4, _ue5, _ue6, _ue7, _ue8, _ue9, _ue10],
    tl_cloud_topology=_tl_cloud_topology,
)
