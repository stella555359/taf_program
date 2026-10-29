# ##########################################################################################
#
#    7_20_UTE5GCLASSSV397  -  IV_PS_397  -  CV397 + CV398 for mobility purpose
#
#    2021-02-15 08:30:33     Creatiion
#    2021-03-25 10:22:00     Update version 03
#
# ##########################################################################################

__maintainer__ = "MN 5G&SC Pz 5G I&V 1 NPS 4 SG"
__team__ = "MN 5G&SC Pz 5G I&V 1 NPS 4 SG"
__email__ = "Tarek.Saket@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import FPFH, ATEN, PduPort
from taf.config.testline.attenuator import AttenuationPort, Hytem, RadioRack
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline.enb import RealEnb
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android

from collections import OrderedDict

_gnb_397_instance_id = 397
_gnb_397_global_bts_id = 23348
_gnb_397_du_common_unit_hardwarde_type = "ASIB/ABIO"
_gnb_397_ru_hw_group = "AEHC"
_gnb_398_instance_id = 398
_gnb_398_global_bts_id = 23347
_gnb_398_du_common_unit_hardwarde_type = "ASIB/ABIO"
_gnb_398_ru_hw_group = "AEHC"
_gnb_373_instance_id = 373
_gnb_373_global_bts_id = 23140
_gnb_373_du_common_unit_hardwarde_type = "ASIL/ABIO"
_gnb_373_ru_hw_group = "AEHC"


# eNB_397 digital port 5, gNB digital port 6
_pdu_397_1 = FPFH(
    port_numbers=[5, 6], addr="10.0.116.117", login="admin", password="admin"
)
# eNB_gNB_397_RU_1 rfsharing
_pdu_397_2 = FPFH(port_numbers=[2], addr="10.28.1.93", login="admin", password="admin")
# eNB_gNB_397_RU_2 rfsharing
_pdu_397_3 = FPFH(port_numbers=[6], addr="10.28.1.96", login="admin", password="admin")

# eNB_398 digital port 1, gNB digital port 2
_pdu_398_1 = FPFH(
    port_numbers=[1, 2], addr="10.0.116.118", login="admin", password="admin"
)
# eNB_398_RU_1 port 1
_pdu_398_2 = FPFH(port_numbers=[1], addr="10.28.1.97", login="admin", password="admin")
# gNB_398_RU_1 port 2
_pdu_398_3 = FPFH(port_numbers=[2], addr="10.28.1.98", login="admin", password="admin")

# gNB_373_RU_1 port 2
_pdu_373_4 = FPFH(port_numbers=[2], addr="10.28.1.98", login="admin", password="admin")

# gNB digital port 3
_pdu_373_1 = ATEN(addr="10.14.62.244", port_numbers=[3], model="ATEN")

tl_name = "7_20_UTE5GCLASSSV397"
__all__ = ["tl"]

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)


# ENB 397 SECTION
# ----------------------------------------------------------------------

# VM UTE
_ute_vm_397_s4G = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="ute"
    )
)

_du_enb_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIC", hardware_version="A102"
)

_du_enb_lmp_connection = SshServiceDetails(
    # addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    addr="10.0.114.51",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_eNB_common_unit_397 = CommonUnit(
    lmp_connection=_du_enb_lmp_connection,
    capacity_units=[_du_enb_capacity_unit],
    pdu_port=_pdu_397_1.pdu_ports[5],
    hardware_type="ASIB",
    hardware_version="A102",
)

_real_enb_397 = Airscale(common_units=[_eNB_common_unit_397])

_lte_real_enb_397_s4G = RealEnb(
    airscale=_real_enb_397, oam_ip="10.0.114.51", instance_id=22357, global_bts_id=22357
)


# GNB 397 SECTION
# ------------------------------------------------------------------------

# VM UTE
_ute_vm_397_m5G = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.90", username="ute", password="ute"
    )
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_397_2.pdu_ports[2],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.6", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.4", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_397_3.pdu_ports[6],
)

_du0_capacity_unit_R_0 = CapacityUnit(addr="192.168.255.22")

_du0_master_capacity_unit_R_0 = CapacityUnit(addr="fsp5_a")

_du0_slave_capacity_unit_R_0 = CapacityUnit(addr="fsp5_b")

_du0_fpga_capacity_unit_R_0 = CapacityUnit(addr="fsp5_c")

_common_unit_397_0_R = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_R_0,
        _du0_master_capacity_unit_R_0,
        _du0_slave_capacity_unit_R_0,
        _du0_fpga_capacity_unit_R_0,
    ],
    pdu_port=_pdu_397_1.pdu_ports[6],
)

_airscale_397 = Airscale(common_units=[_common_unit_397_0_R])

_du_397_0 = DU(airscale=_airscale_397, rus=[_ru1, _ru2])

_cu_397 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.0.114.50",
        vlan_id=1005,
        routing_v4=RoutingInformation(gateway="10.0.115.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.114.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.114.50", username="Nemuadmin", password="nemuuser"
    ),
    s1u=NetworkAddress(
        v4="10.0.112.242",
        vlan_id=4005,
        routing_v4=RoutingInformation(gateway="10.0.112.246", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.0.112.242",
        vlan_id=4005,
        routing_v4=RoutingInformation(gateway="10.0.112.246", ip_prefix_length=29),
    ),
    x2c=NetworkAddress(
        v4="10.0.112.241",
        vlan_id=4005,
        routing_v4=RoutingInformation(gateway="10.0.112.246", ip_prefix_length=29),
    ),
)

_cbts_397_m5G = ClassicalBts(
    cu=_cu_397,
    dus=[_du_397_0],
    instance_id=_gnb_397_instance_id,
    global_bts_id=_gnb_397_global_bts_id,
)


# ENB 398 SECTION
# ----------------------------------------------------------------------

# VM UTE
_ute_vm_398_s4G = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.3", username="ute", password="ute"
    )
)

_du_enb_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIA", hardware_version="A104"
)

_du_enb_lmp_connection = SshServiceDetails(
    # addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    addr="10.0.114.49",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_eNB_common_unit = CommonUnit(
    lmp_connection=_du_enb_lmp_connection,
    capacity_units=[_du_enb_capacity_unit],
    pdu_port=_pdu_398_1.pdu_ports[1],
    hardware_type="ASIA",
    hardware_version="A203",
)

_real_enb_398 = Airscale(common_units=[_eNB_common_unit])

_lte_real_enb_398_s4G = RealEnb(
    airscale=_real_enb_398, oam_ip="10.0.114.49", instance_id=1, global_bts_id=22356
)


# GNB 398 SECTION
# ------------------------------------------------------------------------

# VM UTE
_ute_vm_398_s5G = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.91", username="ute", password="ute"
    )
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="root"
    ),
    pdu_port=_pdu_398_3.pdu_ports[2],
)

_du1_capacity_unit_R_0 = CapacityUnit(addr="192.168.255.22")

_du1_master_capacity_unit_R_0 = CapacityUnit(addr="fsp5_a")

_du1_slave_capacity_unit_R_0 = CapacityUnit(addr="fsp5_b")

_du1_fpga_capacity_unit_R_0 = CapacityUnit(addr="fsp5_c")

_common_unit_398_0_R = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du1_capacity_unit_R_0,
        _du1_master_capacity_unit_R_0,
        _du1_slave_capacity_unit_R_0,
        _du1_fpga_capacity_unit_R_0,
    ],
    pdu_port=_pdu_398_1.pdu_ports[2],
)

_airscale_398 = Airscale(common_units=[_common_unit_398_0_R])

_du_398_0 = DU(airscale=_airscale_398, rus=[_ru3])

_cu_398 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.0.114.48",
        vlan_id=1005,
        routing_v4=RoutingInformation(gateway="10.0.115.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.114.48", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.114.48", username="Nemuadmin", password="nemuuser"
    ),
    s1u=NetworkAddress(
        v4="10.0.113.2",
        vlan_id=4006,
        routing_v4=RoutingInformation(gateway="10.0.113.6", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.0.113.2",
        vlan_id=4006,
        routing_v4=RoutingInformation(gateway="10.0.113.6", ip_prefix_length=29),
    ),
    x2c=NetworkAddress(
        v4="10.0.113.1",
        vlan_id=4006,
        routing_v4=RoutingInformation(gateway="10.0.113.6", ip_prefix_length=29),
    ),
)

_cbts_398_s5G = ClassicalBts(
    cu=_cu_398,
    dus=[_du_398_0],
    instance_id=_gnb_398_instance_id,
    global_bts_id=_gnb_398_global_bts_id,
)


# GNB 373 SECTION
# ------------------------------------------------------------------------

# VM UTE
_ute_vm_373_s5G = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.6", username="ute", password="ute"
    )
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="root"
    ),
    pdu_port=_pdu_373_4.pdu_ports[2],
)

_du2_capacity_unit_R_0 = CapacityUnit(addr="192.168.255.22")

_du2_master_capacity_unit_R_0 = CapacityUnit(addr="fsp5_a")

_du2_slave_capacity_unit_R_0 = CapacityUnit(addr="fsp5_b")

_du2_fpga_capacity_unit_R_0 = CapacityUnit(addr="fsp5_c")

_common_unit_373_0_R = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du2_capacity_unit_R_0,
        _du2_master_capacity_unit_R_0,
        _du2_slave_capacity_unit_R_0,
        _du2_fpga_capacity_unit_R_0,
    ],
    pdu_port=_pdu_373_1.pdu_ports[3],
)
_airscale_373 = Airscale(common_units=[_common_unit_373_0_R])

_du_373_0 = DU(airscale=_airscale_373, rus=[_ru4])

_cu_373 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.48.211",
        vlan_id=1000,
        routing_v4=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.211", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.211", username="Nemuadmin", password="nemuuser"
    ),
    s1u=NetworkAddress(
        v4="10.28.6.177",
        vlan_id=4003,
        routing_v4=RoutingInformation(gateway="10.28.6.182", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.28.6.177",
        vlan_id=4003,
        routing_v4=RoutingInformation(gateway="10.28.6.182", ip_prefix_length=29),
    ),
    x2c=NetworkAddress(
        v4="10.28.6.178",
        vlan_id=4003,
        routing_v4=RoutingInformation(gateway="10.28.6.182", ip_prefix_length=29),
    ),
)

_cbts_373_s5G = ClassicalBts(
    cu=_cu_373,
    dus=[_du_373_0],
    instance_id=_gnb_373_instance_id,
    global_bts_id=_gnb_373_global_bts_id,
)


# Core network
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr=None, username=None, password=None
)
_n2_address = NetworkAddress(v4="10.55.192.6")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf, tac=8103)
_realcore = RealCore(mcc=540, mnc=1, five_g=_real_5g_core_details)


_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABI0B1_AEHC_ENB"

tl = TestLine(
    test_pc=_ute_vm_397_m5G,
    test_pcs=[_ute_vm_397_m5G, _ute_vm_398_s5G, _ute_vm_397_s4G, _ute_vm_398_s4G],
    enbs=[_lte_real_enb_397_s4G, _lte_real_enb_398_s4G],
    gnbs=[_cbts_397_m5G, _cbts_398_s5G, _cbts_373_s5G],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
)
