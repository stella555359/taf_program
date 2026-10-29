# ##########################################################################################
#
#    7_20_UTE5GCLASSSV753-  IV_PS_753  -  CV753
#
#    2021-10-15 14:35:48.905000:
#
#
# ##########################################################################################

__maintainer__ = "Abderrahmane NEZROUK"
__team__ = "MN 5G&SC Pz 5G I&V x NPS x SG"
__email__ = "abderrahmane.nezrouk@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU, RealEnb
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import NetworkAddress
from taf.config.testline import RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore4G
from taf.config.testline.testline import TestLine

from collections import OrderedDict

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.100.185", username="localuser", password="10c@1user"
    )
)

# VM UTE
_vm_ute = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.102", username="ute", password="uteUte!"
    )
)

_du0_pdu = ATEN(addr="10.14.33.47", port_numbers=[1])

_ru0 = RU(
    ru_hw_group="NR_RADIO",
    radio_type="AEUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIL")

_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1a")

_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1b")

_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1c")

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_L_0,
        _du0_master_capacity_unit_L_0,
        _du0_slave_capacity_unit_L_0,
        _du0_fpga_capacity_unit_L_0,
    ],
    pdu_port=_du0_pdu.pdu_ports[1],
    hardware_type="ASIk",
)

_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(airscale=_airscale, rus=[_ru0], instance_id=753, global_bts_id=1)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.48.222",
        vlan_id=1000,
        routing_v4=RoutingInformation(gateway="10.28.6.206", ip_prefix_length=32),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_lte_enb = RealEnb(
    airscale=Airscale(
        common_units=[
            CommonUnit(
                hardware_type="ASIA",
                lmp_connection=SshServiceDetails(
                    addr="192.168.225.129",
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
        )
    ],
    oam_ip=NetworkAddress(v4="10.14.49.107"),
)
_realcore = RealCore4G(mcc="540", mnc="1")
_pdus = [_du0_pdu]

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QCT_FSETO_ASIKL_ABILB4_AEUB_ENB"

tl = TestLine(
    test_pc=_test_vm,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    enbs=[_lte_enb],
    pdus=_pdus,
)
