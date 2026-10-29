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
        addr="10.66.14.44", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.31.1.27",
        vlan_id=331,
        routing_v4=RoutingInformation(gateway="172.31.1.1/24"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="172.31.1.27", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.31.1.27", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.27", vlan_id=2731),
    x2u=NetworkAddress(v4="172.31.1.27", vlan_id=2731),
    s1c=NetworkAddress(v4="172.31.1.27", vlan_id=2731),
    s1u=NetworkAddress(v4="172.31.1.27", vlan_id=2731),
)
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="102"
)
_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    hardware_version="102",
)

_gnb_shub = SC5GRadio(
    ru_hw_group="ASIR-HUB:eCPRI",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.16.129", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(
    #     pdu=Pdu(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)


_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale, rus=[_gnb_shub])
_gnb = ClassicalBts(cu=_cu, dus=[_du], instance_id=124, global_bts_id=124)

_du_enb_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="A105"
)

_du_enb_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.16.119", username="ute", password="ute"),
)
_eNB_common_unit = CommonUnit(
    lmp_connection=_du_enb_lmp_connection,
    capacity_units=[_du_enb_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A102",
)
_real_enb = Airscale(common_units=[_eNB_common_unit])
_enb_shub = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="1.2.3.4", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    )
)
_enb = RealEnb(
    system_module=_real_enb,
    rms=[_enb_shub],
    oam_ip=NetworkAddress(
        v4="172.31.1.11",
        vlan_id=331,
        routing_v4=RoutingInformation(gateway="172.31.1.1/24"),
    ),
    instance_id=124,
    global_bts_id=1124,
)

_core = EPCSim(
    mme_ip="172.31.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.14.44", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="cn.cfg",
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_gnb],
    enbs=[_enb],
    ues=None,
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_APHG_AWHHIQB",
)

# add the configuration of EMSSIM
tl.emssim = {
    "host": _core.mme_ip,
    "server_port": "36" + str(_gnb.global_bts_id),
    "json_port": "40" + str(_gnb.global_bts_id),
    "user": "asir" + str(_gnb.global_bts_id),
    "bts_id": _gnb.global_bts_id,
    "manager_id": _gnb.global_bts_id,
}

__all__ = ["tl"]
