# Generated with TL configuration generator at 2022-08-24_09:23:29

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline import Connection
from taf.config.testline.pdu import PduPort, FPFH
import os
import yaml

# ------------------------GNB_CONFIGURATION------------------------

_pdu1 = FPFH(
    addr="fpfh-zm02-26-p08.p08-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1],
    login="admin",
    password="admin",
)

_pdu2 = FPFH(
    addr="fpfh-zm02-17-p08.p08-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1, 2],
    login="admin",
    password="admin",
)

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.152.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.152.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.152.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.152.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_instance_id = 79024
_gnb_global_bts_id = 79024

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK024.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="10.84.152.24",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
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

gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104810",
    product_code="475266A.101",
    slot_id=SlotId.B1,
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104655",
    product_code="475266A.101",
    slot_id=SlotId.B3,
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1],
    pdu_port=_pdu1.pdu_ports[1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1202703570",
    mac_addr="00:77:e4:11:32:75",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    pdu_port=_pdu2.pdu_ports[1],
    radio_type="AWEUA",
    serial_number="AH212500502",
    product_code="475166A.103",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    pdu_port=_pdu2.pdu_ports[2],
    radio_type="AWEUA",
    serial_number="YK201300001",
    product_code="475166A.X22",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1],
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

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.190.22/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.190.22/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK022.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 77022
_enb_global_bts_id = 77022

enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="K9173842031",
    product_code="473096A.103",
    slot_id=SlotId.B1,
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="L1174718544",
    mac_addr="48:ec:5b:00:a3:ef",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
)

enb_radio_unit_0 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.130", username="root", password="umniedziala"
    ),
    radio_type="AHCA",
    serial_number="AS193613325",
    product_code="473966A.101",
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_enb = RealEnb(
    rms=[enb_radio_unit_0],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK024.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_gnb.dus[0].airscale.common_units[0],
        ),
    ],
)
# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASILL_ABIOB1B3_2xAWEUA",
    pdus=[_pdu1],
)

__all__ = ["tl"]
