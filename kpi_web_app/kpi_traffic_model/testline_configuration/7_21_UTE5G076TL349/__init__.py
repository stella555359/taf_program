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
from taf.config.testline import SC5GRadio, SC4GRadio, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc_master = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.12.62", username="ute", password="ute"
    )
)

_test_pc_slave = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.12.64", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.31.1.39",
        vlan_id=331,
        routing_v4=RoutingInformation(gateway="172.31.1.1/24"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="172.31.1.39", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.31.1.39", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.39", vlan_id=1331),
    x2u=NetworkAddress(v4="172.31.1.39", vlan_id=1331),
    s1c=NetworkAddress(v4="172.31.1.39", vlan_id=1331),
    s1u=NetworkAddress(v4="172.31.1.39", vlan_id=1331),
)
_lmp_connection_master = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit_master = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)
_common_unit_master = CommonUnit(
    lmp_connection=_lmp_connection_master,
    capacity_units=[_capacity_unit_master],
    hardware_type="ASIL",
    hardware_version="102",
)
_lmp_connection_slave = SshServiceDetails(
    addr="192.168.255.119",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_slave.default_ssh_connection_details,
)
_capacity_unit_slave = CapacityUnit(
    addr="fsp5_k2d", hardware_type="ABIA", hardware_version="102"
)
_common_unit_slave = CommonUnit(
    lmp_connection=_lmp_connection_slave,
    capacity_units=[_capacity_unit_slave],
    hardware_type="ASIL",
    hardware_version="102",
)
_gnb_shub = SC5GRadio(
    ru_hw_group="ASIR-HUB:eCPRI",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.12.63", username="ute", password="ute"),
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
_enb_shub = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.12.105", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    )
)

_airscale_master = Airscale(common_units=[_common_unit_master])
_airscale_slave = Airscale(common_units=[_common_unit_slave])
_du = DU(airscale=_airscale_master, rus=[_gnb_shub])
_gnb = ClassicalBts(cu=_cu, dus=[_du], instance_id=349, global_bts_id=349)
_core = EPCSim(
    mme_ip="172.31.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.13.218", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="cn.cfg",
)
_enb = RealEnb(
    system_module=_airscale_slave,
    rms=[_enb_shub],
    instance_id=349,
    global_bts_id=100349,
)
tl = TestLine(
    test_pc=_test_pc_master,
    test_pcs=[_test_pc_master, _test_pc_slave],
    gnbs=[_gnb],
    enbs=[_enb],
    ues=None,
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIML_ABIPB1_ASIMR_ABIPB1_APHG_AWHHIQB_APHA_AHGEA",
)

tl.master_rat = "NR"  # RAT of master: NR or LTE
tl.master_fh = "ecpri"  # cpri or ecpri used in FH
tl.master_shub = "aphg"
# used ports of sHUB. Start form 0, 0 - 3: cpri, 4-5: ecpri
# the first item will be primary port to exchange C/M message
tl.ports_of_master_shub = (4,)
# prrh used by master shub, (prrh type, [prrh_port]), port will start from 1
tl.prrh_of_master_shub = ("AWHGEQK", [1])

tl.slave_rat = "LTE"  # RAT of master: NR or LTE
tl.slave_fh = "cpri"  # cpri or ecpri used in FH
tl.slave_shub = "apha"
# used ports of sHUB. Start form 0,
# the first item will be primary port to exchange C/M message
tl.ports_of_slave_shub = (0,)
# prrh used by slave shub,, (prrh type, [prrh_port]), port will start from 1
tl.prrh_of_slave_shub = ("AHGEA", [1])

__all__ = ["tl"]
