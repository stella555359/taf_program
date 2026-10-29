__maintainer__ = 'Dawid Chuchnowski'
__team__ = 'VRF KRK 6'
__email__ = 'OO_MN_RAN_RD_VRF_KRK_6_52554177@internal.nsn.com'
__owner_email__ = 'dawid.chuchnowski@nokia.com'

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (SshServiceDetails, HttpConnectionDetails)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Connection, Simulator
from taf.config.testline.pdu import FPFH

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
_pdu = FPFH(
     port_numbers=[1, 2, 3, 4, 5, 6],
     addr="fpfh-wb02-1.macro-leg.krk-lab.nsn-rdnet.net",
     login="admin",
     password="admin",
)

_pdus = [_pdu]

_bts1_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129', username='toor4nsn', password='oZPS0POrRieRtu'
    ),
    hardware_type='ASIL',
    capacity_units=[
        CapacityUnit(addr="192.168.253.20", hardware_type='ABIO')],
    pdu_port=_pdus[0].pdu_ports[6],
)

_bts1_airscale1 = Airscale(common_units=[_bts1_common_unit1])

_bts1_cu = CU(backhaul_site_oam_ip='192.168.255.129',
              oam_ssh_connection_details=SshServiceDetails(
                  addr='192.168.255.129', username='toor4nsn', password='oZPS0POrRieRtu'),
              oam_http_connection_details=HttpConnectionDetails(
                  addr='192.168.255.129', username='Nemuadmin', password='nemuuser', port=443),
              x2c=NetworkAddress(v4='10.0.1.1', vlan_id=1157),
              x2u=NetworkAddress(v4='10.0.1.1', vlan_id=1157),
              s1u=NetworkAddress(v4='10.0.1.1', vlan_id=1157),
              )

_bts1_du = DU(_bts1_airscale1)

_bts1 = ClassicalBts(cu=_bts1_cu, dus=[_bts1_du])

_sim_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.200.1",
        username="toor4nsn",
        password="oZPS0POrRieRtu"
    ),
    hardware_type='ASIL',
    capacity_units=[
        CapacityUnit(addr='192.168.253.84', hardware_type='ABIO')],
    pdu_port=_pdus[0].pdu_ports[5],
)
_sim_airscale1 = Airscale(common_units=[_sim_common_unit1])
_sim1 = Simulator(l1=_sim_airscale1)

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr='10.89.45.18',
        username='ute',
        password='ute', ),
    connections=[
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_bts1.dus[0].airscale.common_units[0],
        ),
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_sim1,
        )
    ]
)

tl = TestLine(
    test_pc=_test_pc1,
    gnbs=[_bts1],
    tl_cloud_topology="CLOUD_LO_SIM_LO",
    ues=[_sim1],
    pdus=[_pdus],
)
__all__ = ["tl"]
