import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.ue import Android
from taf.config.testline.gnb.du import DU
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import RoutingInformation

__maintainer__ = "Tashia Tan"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "tashia.tan@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.6", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# _pdu_1 = TopYoung(addr="10.71.196.213", port_numbers=[7])

_fsp_1 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="475266A.104",
    serial_number="	L1214610638",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    # pdu_port=_pdu_1.pdu_ports[7],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="EA220250538",
)

# _ru_pdu_1 = TopYoung(addr="10.71.196.211", port_numbers=[4])
# _ru_pdu_2 = TopYoung(addr="10.71.196.212", port_numbers=[6])
# _ru_pdu_3 = TopYoung(addr="10.71.196.212", port_numbers=[4])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AWPQZ,
    serial_number="EB2248R0451",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.253.", port=2323
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    #    pdu_port=_ru_pdu_1.pdu_ports[4],
)
_rmod_2 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AWPQZ,
    serial_number="EB2248R0448",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.253.", port=2323
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    #    pdu_port=_ru_pdu_2.pdu_ports[6],
)


_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55310
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.247",
    iperf_path="iperf",
    port=55585,
)


_appserver = AppServer(_iperf)


# for FastMile CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55310, 55585],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)


_fastmile_1 = TafUeFastmile(
    com_port="17",
    ue_pc_address="10.0.176.19",
    root_password="6cba5e32bf95",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL22140054C",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)


##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.71.213.236",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.236", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.236", username="Nemuadmin", password="nemuuser"
    ),
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.213.236", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.22")

# _gnb_pdu = _pdu_1

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    #    pdu_port=_gnb_pdu.pdu_ports[7],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_rmod_1, _rmod_2], f1_m_ip_addr="10.71.213.236")


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB_ABIOB_AWPQZ"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="1964", global_bts_id="1964"
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    airscale=_airscale,
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.71.213.236"),
    instance_id=1964,
    global_bts_id=1964,
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    ues=[_fastmile_1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIB_ABIOB_AWPQZ",
)
