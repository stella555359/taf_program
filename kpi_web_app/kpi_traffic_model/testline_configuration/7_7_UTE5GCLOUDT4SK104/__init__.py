# Generated with TL configuration generator at 2023-07-24_16:43:03

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Lukasz Skoczylas"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "lukasz.skoczylas@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu, FPFH, HPE
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------
_fpfh_1 = FPFH(
    port_numbers=[4],
    addr="fpfh-zb08-46-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_hpe_ac_pdu = HPE(
    addr="zb08.mgt.ska-lab.nsn-rdnet.net",
    port_numbers=[2],
    snmp_user=_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2c_ip = NetworkAddress(
    v4="10.84.148.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.190.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.148.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.84.190.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.148.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.255.22.104/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK104.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_instance_id = 77104
_gnb_global_bts_id = 77104

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_gnb_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    f1m=_gnb_f1m_ip,
    f1c=_gnb_f1c_ip,
    f1u=_gnb_f1u_ip,
    x2c=_gnb_x2c_ip,
    x2u=_gnb_x2u_ip,
    s1c=_gnb_s1c_ip,
    s1u=_gnb_s1u_ip,
    xnc=_gnb_xnc_ip,
    xnu=_gnb_xnu_ip,
    ngc=_gnb_ngc_ip,
    ngu=_gnb_ngu_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1215106441",
    product_code="475266A.103",
    # slot_id=SlotId.B4
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    hardware_type="ASIL",
    hardware_version="A.102",
    serial_number="L1214908894",
    mac_addr="",
    pdu_port=PduPort(pdu=_fpfh_1, port_no=4),
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="APHA",
    serial_number="NH203500496",
    product_code="474657A.102",
    pdu_port=PduPort(pdu=_hpe_ac_pdu, port_no=2),
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0],
    oam_ip=_gnb_oam_ip,
    f1_m_ip_addr=_gnb_f1m_ip,
    f1_c_ip_addr=_gnb_f1c_ip,
    f1_u_ip_addr=_gnb_f1u_ip,
    f1_m_cu=_gnb_f1m_ip,
    f1_c_cu=_gnb_f1c_ip,
    f1_u_cu=_gnb_f1u_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

emssim_config = {"host_for_emssim": "10.84.183.157", "ipsec_oam_ip": "172.40.1.2"}
# ------------------------TL_CONFIGURATION------------------------
_test_pc_gnb_main.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASILR_ABIOB4_APHA_1xAHFIH",
)

tl.emssim_config = emssim_config

__all__ = ["tl"]
