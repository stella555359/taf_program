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
        addr="10.66.19.101", username="ute", password="uteUTE!"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.32.1.70",
        vlan_id=201,
        routing=RoutingInformation(gateway="172.32.1.71", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="172.32.1.70", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.32.1.70", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.32.1.70", vlan_id=201),
    x2u=NetworkAddress(v4="172.32.1.70", vlan_id=201),
    s1c=NetworkAddress(v4="172.32.1.70", vlan_id=201),
    s1u=NetworkAddress(v4="172.32.1.70", vlan_id=201),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="101"
)

_capacity_unit_2 = CapacityUnit(
    addr="fsp2_c", hardware_type="ABIL", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_2],
    hardware_type="ASIK",
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
                addr="10.66.19.103", username="ute", password="ute"
            ),
        ),
        # telnet_connection_details=TelnetConnectionDetails(
        #     addr='tty-server',
        #     username='toor4nsn',
        #     password='oZPS0POrRieRtu'
        # )
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(
    #     pdu=Pdu(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

_ru_2 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.19.104", username="ute", password="ute"
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

_du = DU(airscale=_airscale, rus=[_ru, _ru_2])

_instance_id = 1900
cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=_instance_id, global_bts_id=1)

_epcsim = EPCSim(
    mme_ip="172.32.1.71",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=663,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.19.101",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/iphy/EPC_Sim",
    cfg_filename="sim_ipv4.cfg",
)

lteenb = RealEnb(airscale=_du, x2_link_addr=NetworkAddress(v4="172.32.1.60"))

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[cbts],
    enbs=[lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKL_ABILB1B2_2xAWHHC_ENB",
)
__all__ = ["tl"]
