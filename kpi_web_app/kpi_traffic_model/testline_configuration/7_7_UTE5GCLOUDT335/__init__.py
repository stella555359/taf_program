# Generated with TL configuration generator at 2024-04-19_10:08:31

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[2,3],         # update port_no
    addr="FPFH-BA02-43-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu = FPFH(
    port_numbers=[1,2,3,4,5],         # update port_no
    addr="FPFH-BA02-46-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT335.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 75335
_gnb_0_global_bts_id = 75335

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.83.183.85/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.83.183.85/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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
    v4="10.83.183.85/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.83.183.85/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.83.183.85/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_0_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
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
     ru_hw_group="AEQC",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.2",
        username="root",
        password="umniedziala",
     ),
     radio_type="AEQC",
     serial_number="1M214615347",
     product_code="475431A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
     ru_hw_group="AEQC",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.10",
        username="root",
        password="umniedziala",
     ),
     radio_type="AEQC",
     serial_number="1M214615285",
     product_code="475431A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=4),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
     ru_hw_group="AEQC",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.162",
        username="root",
        password="umniedziala",
     ),
     radio_type="AEQC",
     serial_number="1M202608989",
     product_code="475431A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_3 = RU(
     ru_hw_group="AHPMDB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.130",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHPMDB",
     serial_number="AS212619504",
     product_code="475000A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=1),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_4 = RU(
     ru_hw_group="AHPMDB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHPMDB",
     serial_number="AS220887234",
     product_code="475000A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=5),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_5 = RU(
     ru_hw_group="AHPMDB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.128",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHPMDB",
     serial_number="F7201905619",
     product_code="475000A.101",
     pdu_port=PduPort(pdu=_bts_pdu, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1213108470",
    product_code="475266A.104",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2],
    )

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1213108453",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_3, _gnb_0_radio_unit_4, _gnb_0_radio_unit_5],
    )

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH212766904",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1B2_3xAHPMDB_3xAQQC"
)

__all__ = ["tl"]