__maintainer__ = "Min Juan"
__team__ = "MG_5G_NJN_UUF_PET"
__email__ = "I_5GASIR_UUF_PET@internal.nsn.com"
__owner_email__ = "juan.min@nokia-sbell.com"
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

# from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
import os
import yaml

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.14.32", username="ute", password="Nokia666@ute!"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.30.1.21",
        vlan_id=0,
        routing=RoutingInformation(gateway="172.31.1.22", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.21", vlan_id=0),
    x2u=NetworkAddress(v4="172.30.1.21", vlan_id=0),
    s1c=NetworkAddress(v4="172.30.1.21", vlan_id=0),
    s1u=NetworkAddress(v4="172.30.1.21", vlan_id=0),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIP", hardware_version="X13"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIL",
    hardware_version="A103",
)

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="root",
            password="",
            proxy=SshServiceDetails(
                addr="10.66.31.236", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

_ru_3 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="rfsw",
            password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
            proxy=SshServiceDetails(addr="10.66.31.237", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

_ru_2 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="root",
            password="",
            proxy=SshServiceDetails(addr="10.66.31.238", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3], f1_m_ip_addr="192.168.255.129")

_instance_id =37420
_bts = ClassicalBts(cu=_cu, dus=[_du], instance_id=_instance_id, global_bts_id=37420)

_epcsim = EPCSim(
    mme_ip="172.30.1.22",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.234",
        username="ute",
        password="ute",
    ),
    dir_path="/opt/iphy",
    cfg_filename="sim_ipv4_nsa4g_qt.cfg",
)

lteenb = RealEnb(
    # system_module=_real_enb,
    x2_link_addr=NetworkAddress(v4="192.168.255.129"),
    instance_id=374201,
    global_bts_id=37420,
)
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[lteenb],
    ues=[],
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIL_ABIP_multiRRH",
)
__all__ = ["tl"]
