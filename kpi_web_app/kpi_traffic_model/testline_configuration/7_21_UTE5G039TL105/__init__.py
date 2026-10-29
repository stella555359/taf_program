__maintainer__ = "NSB 5G SC SYSTEM"
__team__ = "NSB 5G SC SYSTEM"
__email__ = "nj-nm-systemteam@LIST.NOKIA.COM"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.150", username="ute", password="uteUTE!"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.30.32",
        v6="2a00:8a00:8001:2::F5",
        vlan_id=30,
        routing_v4=RoutingInformation(gateway="10.66.30.1", ip_prefix_length=24),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:8001:2::F1", ip_prefix_length=124
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=559),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=559),
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=559),
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=559),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.152", username="ute", password="uteUTE!"
            ),
        ),
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_instance_id = 39105
_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=_instance_id, global_bts_id=39105)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.150",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/iphy/latest",
    cfg_filename="sim_ipv4_DM.cfg",
)

_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.30.1.10"))

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIBR_ABILB4_APHA_AWHQK",
)

__all__ = ["tl"]
