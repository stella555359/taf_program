__maintainer__ = "Wojciech Dudek"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"
__owner_email__ = "wojciech.1.dudek@nokia.com"

from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.ue import Android
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.178.196",  # VM-5G-7-7-CLOUDT288.sc5g.krk-lab.nsn-rdnet.net
        username="ute",
        password="ute",
    )
)

_ru_pdu = ATEN(addr="0.0.0.0", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)


_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.83.183.38",
        v6=None,
        vlan_id=None,
        routing=RoutingInformation(gateway="10.83.183.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.83.183.38",
        v6=None,
        vlan_id=None,
        routing=RoutingInformation(gateway="10.83.183.254", ip_prefix_length=23),
    ),
    x2u=NetworkAddress(
        v4="10.83.183.38",
        v6=None,
        vlan_id=None,
        routing=RoutingInformation(gateway="10.83.183.254", ip_prefix_length=23),
    ),
    s1u=NetworkAddress(
        v4="10.83.183.38",
        v6=None,
        vlan_id=None,
        routing=RoutingInformation(gateway="10.83.183.254", ip_prefix_length=23),
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A101B1"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3])

_bts = ClassicalBts(cu=_cu, dus=[_du], instance_id=288, global_bts_id=1)

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-cloudt288.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
    mme_ip="10.253.165.38",
    mcc=244,
    mnc=8,
    tac=8202,
    edaemon_port=12345,
    egate_port=60001,
)

_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="10.83.182.19"))

_ue_pc_ssh = SshServiceDetails("10.83.178.232", "user-lab0", password="Bts2003")

_iperf_pc_ssh = SshServiceDetails("10.83.178.196", "ute", password="ute")

_android_iperf = IperfDataTransferDetails(
    _iperf_pc_ssh, "40.1.1.254", "/data/data/com.magicandroidapps.iperf/bin/"
)

_android_ue = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="9025c4ad",  # Qualcomm 8150/SDX55
    server_dir="/cygdrive/c/pyro_server/ta_ue_plugin_android/ue",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_android_iperf,
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[_lteenb],
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIKL_ABILB1_AHCA_ENB",
    ues=[_android_ue],
)

__all__ = ["tl"]
