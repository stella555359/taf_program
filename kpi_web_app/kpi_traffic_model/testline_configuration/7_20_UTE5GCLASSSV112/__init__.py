# ##########################################################################################
#
#    7_20_UTE5GCLASSSV112  -  IV_PS_112  -  CV112
#
#    2023-12-17 22:17:09.437964:
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
from taf.config.testline.attenuator import AttenuationPort, Hytem, RadioRack
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
    addr="10.0.117.83", login="admin", password="admin", port_numbers=[4]
)
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.140", login="admin", password="admin", port_numbers=[1]
)
_ru2_pdu_gnb = FPFH(
    addr="10.0.117.140", login="admin", password="admin", port_numbers=[2]
)
_attenuator0 = Hytem(
    ip_addr="10.0.96.123", port=10001, attenuation_port_numbers=[0, 1, 2, 3, 4, 5, 6, 7]
)
_rmod_gnb_2 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="L1204708764",
    attenuation_ports=[
        _attenuator0.attenuator_ports[4],
        _attenuator0.attenuator_ports[5],
    ],
)
_rmod_gnb_1 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193301368",
    attenuation_ports=[
        _attenuator0.attenuator_ports[0],
        _attenuator0.attenuator_ports[1],
    ],
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1],
    serial_number="L1204109022",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_2],
    serial_number="L1204008468",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2],
    hardware_type="ASIM",
    hardware_version="475765A.Y13",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    pdu_port=_du1_pdu_gnb.pdu_ports[4],
    serial_number="L1223306795",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23152, instance_id=112)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"),
        v4="10.14.49.123",
        vlan_id="1000",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.123", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.123", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.11.66/29", vlan_id="4002"),
    x2c=NetworkAddress(v4="10.28.11.65/29", vlan_id="4002"),
    x2u=NetworkAddress(v4="10.28.11.66/29", vlan_id="4002"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23152, instance_id=112)


# CV189
_ru3_pdu_gnb = FPFH(
    addr="10.28.1.80", login="admin", password="admin", port_numbers=[4]
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193201178",
    attenuation_ports=[
        _attenuator0.attenuator_ports[2],
        _attenuator0.attenuator_ports[3],
    ],
)
_ru4_pdu_gnb = FPFH(
    addr="10.28.1.81", login="admin", password="admin", port_numbers=[3]
)
_rmod_gnb_4 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[3],
    ru_hw_group="NR_RADIO",
    radio_type="AHLOA",
    serial_number="K9182103377",
    attenuation_ports=[
        _attenuator0.attenuator_ports[6],
        _attenuator0.attenuator_ports[7],
    ],
)

# _du2_pdu_gnb = ATEN(addr="10.14.55.207", port_numbers=[4])
_du2_pdu_gnb = FPFH(addr="", login="admin", password="admin", port_numbers=[])
_du2_pdu_port = PduPort(pdu=_du2_pdu_gnb, port_no="4")

_du2_asik_master_L = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_asik_slave_L = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_capacity_unit_L_0 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1a", hardware_type="ABIO")
_du2_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1b", hardware_type="ABIO")
_du2_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1c", hardware_type="ABIO")
_du2_capacity_unit_L_1 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_master_capacity_unit_L_1 = CapacityUnit(addr="fsp-2a", hardware_type="ABIO")
_du2_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp-2b", hardware_type="ABIO")
_du2_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp-2c", hardware_type="ABIO")
_cu2 = CommonUnit(
    hardware_type="ASIB",
    lmp_connection=SshServiceDetails(
        addr="10.14.49.164", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du2_asik_master_L,
        _du2_asik_slave_L,
        _du2_capacity_unit_L_0,
        _du2_master_capacity_unit_L_0,
        _du2_slave_capacity_unit_L_0,
        _du2_fpga_capacity_unit_L_0,
        _du2_capacity_unit_L_1,
        _du2_master_capacity_unit_L_1,
        _du2_slave_capacity_unit_L_1,
        _du2_fpga_capacity_unit_L_1,
    ],
    pdu_port=_du2_pdu_port,
)
_airscale1 = Airscale(common_units=[_cu2])

_rus_cablink_du2 = [
    Cablink(
        source=Endpoint(unit=_du2_master_capacity_unit_L_0, label="SFP", port_id="1"),
        target=Endpoint(unit=_rmod_gnb_3, label="SFP", port_id="2"),
    ),
    Cablink(
        source=Endpoint(unit=_du2_master_capacity_unit_L_1, label="SFP", port_id="1"),
        target=Endpoint(unit=_rmod_gnb_4, label="SFP", port_id="1"),
    ),
]
_du2 = DU(
    airscale=_airscale1, rus=[_rmod_gnb_3, _rmod_gnb_4], cablinks=_rus_cablink_du2
)
_cu2 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.49.164",
        vlan_id=1000,
        routing_v4=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.164", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.164", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(v4="10.28.11.65", vlan_id=4003),
    x2u=NetworkAddress(v4="10.28.11.66", vlan_id=4003),
    s1u=NetworkAddress(v4="10.28.11.66", vlan_id=4003),
)
_gnb_sbts_2 = ClassicalBts(cu=_cu2, dus=[_du2], instance_id=189, global_bts_id=23212)
# end CV189

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
        addr="10.0.108.134",
        password="uteUTE!",
        port=22,
        username="ute",
    ),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _du2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
]

_android_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.96.49", username="cv5g2_5", password="M!k@el5G", port=9090
    ),
    serial_number="aea883c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="/cygdrive/c/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="D:/Qualcomm/Config/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.14.42.188", username="ran5g", password="nokia2018Ne!"
        ),
        network_interface_address="10.11.70.76",
        iperf_path=None,
    ),
)
_appserver_ssh = AppServer(
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.14.42.188", username="ran5g", password="nokia2018Ne!"
        ),
        network_interface_address="10.11.70.76",
        iperf_path=None,
    )
)
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIM_2xABIO_AEQN_AEHC_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1, _gnb_sbts_2],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver_ssh,
    attenuators=[_attenuator0],
    ues=[_android_ue1],
)
