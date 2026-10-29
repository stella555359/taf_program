# ##########################################################################################
#
#    7_20_UTE5GCLASSSV045  -  IV_PS_045  -  CV045
#
#    2023-12-17 22:12:20.454778:
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

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["INIT_CONFIG_FILE_PATH"] = cfg_dir
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(cfg_dir, "ue_config.yaml")

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(
    addr="10.0.117.116", login="admin", password="admin", port_numbers=[2]
)
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.145", login="admin", password="admin", port_numbers=[1]
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193601318",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1],
    serial_number="L1204109019",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIL",
    hardware_version="474767A.101",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu", port=22
    ),
    pdu_port=_du1_pdu_gnb.pdu_ports[2],
    serial_number="L1203805920",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23123, instance_id=45)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"),
        v4="10.14.48.45",
        vlan_id="1000",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.45", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.45", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.6.66/24", vlan_id="4001"),
    x2c=NetworkAddress(v4="10.28.6.65/24", vlan_id="4001"),
    x2u=NetworkAddress(v4="10.28.6.66/24", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23123, instance_id=45)

_du1_pdu_enb = FPFH(
    addr="10.0.117.117", login="admin", password="admin", port_numbers=[5]
)

_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="",
    product_code="",
    rus=[],
    serial_number="",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    pdu_port=_du1_pdu_enb.pdu_ports[5],
    serial_number="",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22150,
    instance_id=22150,
    oam_ip=NetworkAddress(v4="10.14.48.231"),
    rms=[],
    system_module=_smod_enb_1,
)

_lte_enb = RealEnb(
    system_module=Airscale(
        common_units=[
            CommonUnit(
                hardware_type="ASIA",
                lmp_connection=SshServiceDetails(
                    addr="10.14.48.231",
                    username="toor4nsn",
                    password="oZPS0POrRieRtu",
                ),
                capacity_units=[
                    CapacityUnit(
                        addr="192.168.253.20",
                        hardware_type="ABIA",
                    )
                ],
            )
        ]
    ),
    rms=[
        RU(
            ru_hw_group="LTE_RADIO",
            radio_type="FHEB",
        )
    ],
    instance_id=22150,
    global_bts_id=22150,
    oam_ip=NetworkAddress(
        v4="10.14.48.231",
        routing=RoutingInformation(
            gateway="10.14.48.231",
            ip_prefix_length=23,
        ),
    ),
    x2_link_addr=NetworkAddress(v4="10.28.11.45"),
)
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
        addr="10.0.108.105", password="uteUTE!", port=22, username="ute"
    ),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _du1_pdu_enb,
]

_android_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.96.83", username="cv5g2_5", password="M!k@el5G", port=9090
    ),
    serial_number="5ee10cbc",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="/cygdrive/c/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="xxxxxx",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.14.42.85", username="ran5g", password="nokia2018"
        ),
        network_interface_address="10.11.70.27",
        iperf_path=None,
    ),
)


tl = TestLine(
    gnbs=[_gnb_sbts_1],
    enbs=[_enb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_NSA_ASIL_ABIO_AEQN_UTECA",
    ues=[_android_ue1],
)
