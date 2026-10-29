__maintainer__ = "Venkata Rajesh"
__team__ = "I_MN_ECE_BLR_RD_TST_SQD_ELECTRON_GMS "
__email__ = "I_MN_ECE_BLR_RD_TST_SQD_ELECTRON@internal.nsn.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import Android, Airphone, AirphoneCloud
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline import RealEnb, LTEEmuEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.145", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip="10.41.170.155",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.155", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.41.170.155", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="10.41.170.155", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A101",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale)

_bts = ClassicalBts(cu=_cu, dus=[_du])

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.145", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS",
    cfg_filename="config_crt.cfg",
    mme_ip="10.0.1.131",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=22222,
    egate_port=20000,
)

_lteenb = RealEnb(airscale=_du, x2_link_addr="10.10.40.10")

_l3 = SshServiceDetails(
    addr="10.41.170.156", username="toor4nsn", password="oZPS0POrRieRtu"
)

_l2 = SshServiceDetails(
    addr="10.41.170.156", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lteSim = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.145", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS",
    cfg_filename="config_crt.cfg",
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.41.170.156", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_l1 = Airscale(common_units=[_common_unit_1])

_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.156", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.41.170.156"),
)

_airphone = Airphone(
    egate=_lteSim.default_ssh_connection_details,
    l3_ssh_connection_details=_l3,
    l2_ssh_connection_details=_l2,
    l1=_l1,
    airphone_cloud=_airphone_cloud,
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[_lteenb],
    ues=[_airphone],
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIK_ABIL_AEUA_cOAM",
)

__all__ = ["tl"]
