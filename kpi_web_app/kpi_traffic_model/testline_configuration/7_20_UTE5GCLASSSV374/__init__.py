# ##########################################################################################
#
#    7_20_UTE5GCLASSSV374  -  IV_PS_374  -  CV374
#
#    2023-12-17 22:24:48.328947:
#    __init__.py generator (version 2.0 of 02/12/2023).
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
from taf.config.testline.ue import Android
from collections import OrderedDict
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.attenuator import AttenuationPort, Hytem

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["INIT_CONFIG_FILE_PATH"] = cfg_dir
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(cfg_dir, "ue_config.yaml")

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(addr="10.0.96.4", login="admin", password="admin", port_numbers=[2])
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.159", login="admin", password="admin", port_numbers=[1]
)
_ru2_pdu_gnb = FPFH(
    addr="10.0.117.159", login="admin", password="admin", port_numbers=[2]
)
# _ru3_pdu_gnb = FPFH(addr="10.0.117.158", login="admin", password="admin", port_numbers=[2])

_attenuator0 = Hytem(
    ip_addr="10.0.96.122", port=10001, attenuation_port_numbers=[0, 1, 2, 3, 4, 5, 6, 7]
)

_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193501202",
    attenuation_ports=[
        _attenuator0.attenuator_ports[0],
        _attenuator0.attenuator_ports[1],
    ],
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193301303",
    attenuation_ports=[
        _attenuator0.attenuator_ports[2],
        _attenuator0.attenuator_ports[3],
    ],
)
# _rmod_gnb_3 = RU(
#     pdu_port=_ru3_pdu_gnb.pdu_ports[2], radio_type="AHLOA", ru_hw_group="NR_RADIO", serial_number="BL1933G10R0"
# )

_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="102",
    product_code="475266A.102",
    rus=[_rmod_gnb_1, _rmod_gnb_2],
    # rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1204705930",
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
    pdu_port=_du1_pdu_gnb.pdu_ports[2],
    serial_number="L1200806974",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23213, instance_id=374)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"),
        v4="10.14.49.156",
        vlan_id="1000",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.156", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.156", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.15.138/29", vlan_id="4001"),
    x2c=NetworkAddress(v4="10.28.15.137/29", vlan_id="4001"),
    x2u=NetworkAddress(v4="10.28.15.138/29", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23213, instance_id=374)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(
            device=_gnb_sbts_1.dus[0].airscale.common_units[0],
            interface="eth1",
            interface_type="lmp",
        ),
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.59",
        password="uteUTE!",
        port=22,
        username="ute",
    ),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb]
# _pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb]

_android_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.97.52", username="cv5g2_5", password="M!k@el5G", port=9090
    ),
    serial_number="ba459ba3",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="/cygdrive/c/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="xxxxxx",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.14.42.241", username="ran5g", password="nokia2018"
        ),
        network_interface_address="10.11.70.111",
        iperf_path=None,
    ),
)
_appserver_ssh = AppServer(
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.14.42.241", username="ran5g", password="nokia2018"
        ),
        network_interface_address="10.11.70.111",
        iperf_path=None,
    )
)
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIB_ABIO_2xAEQN_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver_ssh,
    attenuators=[_attenuator0],
    ues=[_android_ue1],
)
