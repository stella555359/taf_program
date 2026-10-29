__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RoutingInformation, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, SlotId
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.enb import RealEnb

import os
import yaml

__all__ = ["tl"]

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK070.p08.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK069.p08.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.70/23",
    # routing_v4=RoutingInformation(gateway="10.84.165.254"),
)

_gnb_instance_id = 79070
_gnb_global_bts_id = 79070
_gnb_ru0_ip = NetworkAddress(v4="172.22.48.2")
_gnb_ru_hw_group = "AWEUA"

_gnb_pdu = FPFH(
    port_numbers=[2],
    addr="fpfh-za19-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_ru_pdu = HPE(
    port_numbers=[6],
    addr="za19.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)
_pdus = [_gnb_pdu, _ru_pdu]


# eNB BH: 10.84.164.55

##############################################################

# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="10.84.152.70",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_default_enb_http_connection = HttpConnectionDetails(
    addr="10.84.152.69",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

##############################################################


# Important!: check and change below if other than default #

# Test PCs
_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    x2u=_gnb_oam_ip,
    s1u=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)  # replace if other than default

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details
_f1_m_ip_addr = NetworkAddress(
    v4="10.84.164.52",
    vlan_id=504,
    routing_v4=RoutingInformation(gateway="10.84.165.254"),
)

_ru_0_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUA",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=6),
    serial_number="AH205100797",
)

_abio_master_gnb = CapacityUnit(addr="192.168.253.23", hardware_type="ABIO", rus=[_ru_0_gnb])

_du_common_unit_gnb = CommonUnit(
    pdu_port=_gnb_pdu.pdu_ports[2],
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abio_master_gnb],
    hardware_type="ASIL",
    hardware_version="103",
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(
    airscale=_airscale_gnb,
    f1_m_ip_addr=_f1_m_ip_addr,
)

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

# ------------------------ENB0_CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK069.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_enb_0_instance_id = 76069
_enb_0_global_bts_id = 76069

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.84.152.69/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.84.152.69/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_0_radio_unit_0 = RU(
     ru_hw_group="AHFIB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHFIB",
     serial_number="BL2120V0COQ",
     product_code="474216A.101",
     # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203290566",
    product_code="473096A.105",
    slot_id=SlotId.B4,
    rus=[_enb_0_radio_unit_0],
    )

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="DH202863935",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    # pdu_port=PduPort(pdu=_bts_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_0_airscale = Airscale(
    common_units=[_enb_0_common_unit_0],
    product_code="473098A",
    )

_enb_0 = RealEnb(
    x2_link_addr=_default_enb_http_connection,
    instance_id=_enb_0_instance_id,
    global_bts_id=_enb_0_global_bts_id,
    system_module=_enb_0_airscale,
    oam_ip=_enb_0_oam_ip,
)

_test_pc_enb_0.connections = [
    Connection(
        device=_enb_0.system_module.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

###########################################################################################################

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

_ue_pc_ssh = SshServiceDetails(
    addr="PLKR-SC5G-PC41.p08.ska-lab.nsn-rdnet.net", username="user-lab0", password="Bts2003"
)


_test_pc_gnb_main.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_appserver_ssh = SshServiceDetails(addr="10.84.168.121", username="5g", password="5g")

_android_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.84.169.61",
    iperf_path="/data/data/com.nokia.android.application/iperf",
)

# Testline -> remember to add # enbs=[_enb_0] for EDA testing

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    pdus=_pdus,
    gnbs=[_gnb_main],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_7_7_T8SK070",
)

