__maintainer__ = "SHI Kun"
__team__ = "Nanjing ET"
__email__ = "I_NJ_SC_SYSTEM_VERF@internal.nsn.com"
__owner_email__ = "kun.shi@nokia-sbell.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio, SC4GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.13.135", username="ute", password="ute"
    )
)

_du_enb_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ASOE", hardware_version="A102"
)

_du_enb_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.13.135", username="ute", password="ute"),
)
_eNB_common_unit = CommonUnit(
    lmp_connection=_du_enb_lmp_connection,
    capacity_units=[_du_enb_capacity_unit],
    hardware_type="ASOE",
    hardware_version="A102",
)
_real_enb = Airscale(common_units=[_eNB_common_unit])
_enb_shub_1 = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="80.80.80.13", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    )
)
_enb = RealEnb(
    system_module=_real_enb,
    rms=[_enb_shub_1],
    oam_ip=NetworkAddress(
        v4="172.31.1.35",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="172.31.1.1/24"),
    ),
    instance_id=466,
    global_bts_id=466,
)

_core = EPCSim(
    mme_ip="172.31.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.13.135", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="cn.cfg",
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=None,
    enbs=[_enb],
    ues=None,
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASOE_APHG*9_AWHENHD*9",
)

__all__ = ["tl"]
