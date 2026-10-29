# Generated with TL configuration generator at 2023-12-18_12:50:45

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
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
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

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config

# ------------------------PDU_CONFIGURATION------------------------

_pdu_1 = FPFH(
    port_numbers=[5, 6],
    addr="fpfh-zf17-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu_2 = FPFH(
    port_numbers=[1, 2, 3, 6],
    addr="fpfh-zf17-34-p01.p01-leg.ska-lab.nsn-rdnet.net",
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
    port_numbers=[999],         # update port_no
    addr="FQDN HPE address",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_1_CONFIGURATION------------------------

_gnb_1_oam_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2c_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_x2u_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1u_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_xnc_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_xnu_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_ngc_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_1_ngu_ip = NetworkAddress(
    v4="10.84.142.59/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

# ------------------------GNB_2_CONFIGURATION------------------------

_gnb_2_oam_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_f1m_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_x2c_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_x2u_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_s1u_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_xnc_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_xnu_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_ngc_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_2_ngu_ip = NetworkAddress(
    v4="10.84.142.60/23",
    routing_v4=RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT9SK059-1.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_1_instance_id = 80059
_gnb_1_global_bts_id = 80059

_test_pc_gnb_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT9SK059-2.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_2_instance_id = 80060
_gnb_2_global_bts_id = 80060

_default_gnb_1_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_default_gnb_2_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_2.default_ssh_connection_details,
)

_default_oam_2_http_connection = HttpConnectionDetails(
    addr=_gnb_2_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_oam_ip,
    oam_ssh_connection_details=_default_gnb_1_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    f1m=_gnb_1_f1m_ip,
    f1c=_gnb_1_f1c_ip,
    f1u=_gnb_1_f1u_ip,
    x2c=_gnb_1_x2c_ip,
    x2u=_gnb_1_x2u_ip,
    s1c=_gnb_1_s1c_ip,
    s1u=_gnb_1_s1u_ip,
    xnc=_gnb_1_xnc_ip,
    xnu=_gnb_1_xnu_ip,
    ngc=_gnb_1_ngc_ip,
    ngu=_gnb_1_ngu_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_gnb_1_radio_unit_0 = RU(
     ru_hw_group="AZQS",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AZQS",
     serial_number="1M213113961",
     product_code="475664A.101",
     pdu_port=_pdu_2.pdu_ports[2],)

_gnb_1_radio_unit_1 = RU(
     ru_hw_group="AHEH",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHEH",
     serial_number="EA222750817",
     product_code="474253A.101",
     pdu_port=_pdu_2.pdu_ports[6],)

_gnb_1_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1215008552",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_1_radio_unit_1],
    )

_gnb_1_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1215106446",
    product_code="475266A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_1_radio_unit_0],
    )

_gnb_1_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_1_ssh_lmp_connection,
    capacity_units=[_gnb_1_capacity_unit_0, _gnb_1_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1190817416",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=_pdu_1.pdu_ports[5])

_airscale_gnb_1 = Airscale(
    common_units=[_gnb_1_common_unit_0],
    product_code="473098A",
    )

_du_gnb_1 = DU(
    airscale=_airscale_gnb_1,
    rus=[_gnb_1_radio_unit_0, _gnb_1_radio_unit_1],
    oam_ip=_gnb_1_oam_ip,
    f1_m_ip_addr=_gnb_1_f1m_ip,
    f1_c_ip_addr=_gnb_1_f1c_ip,
    f1_u_ip_addr=_gnb_1_f1u_ip,
    f1_m_cu=_gnb_1_f1m_ip,
    f1_c_cu=_gnb_1_f1c_ip,
    f1_u_cu=_gnb_1_f1u_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
    )

_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_cu_gnb_2 = CU(
    backhaul_site_oam_ip=_gnb_2_oam_ip,
    oam_ssh_connection_details=_default_gnb_2_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_2_http_connection,
    f1m=_gnb_2_f1m_ip,
    f1c=_gnb_2_f1c_ip,
    f1u=_gnb_2_f1u_ip,
    x2c=_gnb_2_x2c_ip,
    x2u=_gnb_2_x2u_ip,
    s1c=_gnb_2_s1c_ip,
    s1u=_gnb_2_s1u_ip,
    xnc=_gnb_2_xnc_ip,
    xnu=_gnb_2_xnu_ip,
    ngc=_gnb_2_ngc_ip,
    ngu=_gnb_2_ngu_ip,
    instance_id=_gnb_2_instance_id,
    global_bts_id=_gnb_2_global_bts_id,
)

_gnb_2_radio_unit_0 = RU(
     ru_hw_group="AZQO",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AZQO",
     serial_number="1M203309912",
     product_code="475288A.102",
     pdu_port=_pdu_2.pdu_ports[1],)

_gnb_2_radio_unit_1 = RU(
     ru_hw_group="AHPE",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHPE",
     serial_number="1M222012021",
     product_code="475208A.101",
     pdu_port=_pdu_2.pdu_ports[3])

_gnb_2_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1215008559",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_2_radio_unit_1],
    )

_gnb_2_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.102",
    serial_number="L1210302277",
    product_code="475266A.102",
    slot_id=SlotId.B5,
    rus=[_gnb_2_radio_unit_0],
    )

_gnb_2_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_2_ssh_lmp_connection,
    capacity_units=[_gnb_2_capacity_unit_0, _gnb_2_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1190817412",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=_pdu_1.pdu_ports[6],)

_airscale_gnb_2 = Airscale(
    common_units=[_gnb_2_common_unit_0],
    product_code="473098A",
    )

_du_gnb_2 = DU(
    airscale=_airscale_gnb_2,
    rus=[_gnb_2_radio_unit_0, _gnb_2_radio_unit_1],
    oam_ip=_gnb_2_oam_ip,
    f1_m_ip_addr=_gnb_2_f1m_ip,
    f1_c_ip_addr=_gnb_2_f1c_ip,
    f1_u_ip_addr=_gnb_2_f1u_ip,
    f1_m_cu=_gnb_2_f1m_ip,
    f1_c_cu=_gnb_2_f1c_ip,
    f1_u_cu=_gnb_2_f1u_ip,
    instance_id=_gnb_2_instance_id,
    global_bts_id=_gnb_2_global_bts_id,
    )

_gnb_2 = ClassicalBts(
    cu=_cu_gnb_2,
    dus=[_du_gnb_2],
    instance_id=_gnb_2_instance_id,
    global_bts_id=_gnb_2_global_bts_id,
)

_test_pc_gnb_1.connections = [
    Connection(
        device=_gnb_1.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_test_pc_gnb_2.connections = [
    Connection(
        device=_gnb_2.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------
_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_1,
    gnbs=[_gnb_1, _gnb_2],
    pdus=[_pdu_1, _pdu_2],
    test_pcs=[_test_pc_gnb_1, _test_pc_gnb_2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_MULTIGNB_SA_ASIBL_2xABIOB1B2_ASIBR_2xABIOB4B5_AHEH_AHPE_AZQO_AZQS",
)

__all__ = ["tl"]
