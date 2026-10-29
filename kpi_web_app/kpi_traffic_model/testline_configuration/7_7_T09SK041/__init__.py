# Generated with TL configuration generator at 2025-10-14_06:44:32

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
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
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.lmi import SerialOverTcp, Remote 
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],         # update port_no
    addr="fpfh-he05-46-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_bts_pdu_2 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],         # update port_no
    addr="fpfh-he04-46-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T09SK041.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_0_instance_id = 80041
_gnb_0_global_bts_id = 80041

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_x2c_ip = NetworkAddress(
    v4="10.255.34.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.84.140.41/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_0 = CU(
    backhaul_site_oam_ip=_gnb_0_oam_ip,
    oam_ssh_connection_details=_gnb_0_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_0_oam_http_connection,
    f1m=_gnb_0_f1m_ip,
    f1c=_gnb_0_f1c_ip,
    f1u=_gnb_0_f1u_ip,
    x2c=_gnb_0_x2c_ip,
    x2u=_gnb_0_x2u_ip,
    s1c=_gnb_0_s1c_ip,
    s1u=_gnb_0_s1u_ip,
    xnc=_gnb_0_xnc_ip,
    xnu=_gnb_0_xnu_ip,
    ngc=_gnb_0_ngc_ip,
    ngu=_gnb_0_ngu_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AHPMDK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHPMDK",
    serial_number="L1252300134",
    product_code="476714A.X21",
    pdu_port=PduPort(
        pdu=_bts_pdu_2, port_no=4
    ),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHPMDK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHPMDK",
    serial_number="L1252300136",
    product_code="476714A.X21",
    pdu_port=PduPort(
        pdu=_bts_pdu_2, port_no=5
    ),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="DH202590302",
    product_code="473096A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1233005557",
    product_code="476397A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233304606",
    mac_addr="28:74:f5:0a:22:51",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=5
    ),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="473098A",
)

_du_gnb_0 = DU(
    airscale=_gnb_0_airscale, 
    oam_ip=_gnb_0_oam_ip,
    f1_m_ip_addr=_gnb_0_f1m_ip,
    f1_c_ip_addr=_gnb_0_f1c_ip,
    f1_u_ip_addr=_gnb_0_f1u_ip,
    f1_m_cu=_gnb_0_f1m_ip,
    f1_c_cu=_gnb_0_f1c_ip,
    f1_u_cu=_gnb_0_f1u_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_7_7_T09SK041",
)

__all__ = ["tl"]