# Generated with TL configuration generator at 2024-07-04_08:27:53

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
    port_numbers=[2],         # update port_no
    addr="fpfh-ze18-46-p01.p01-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[2, 13, 14, 15],         # update port_no
    addr="ze18.mgt.ska-lab.nsn-rdnet.net",    # update address
    snmp_user=_hpe_snmp_user,
)


# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK128.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 76128
_gnb_0_global_bts_id = 76128

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.150.128/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.150.128/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
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
    v4="10.84.150.128/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.84.150.128/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.84.150.128/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
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
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH222200467",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=14),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH213100529",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=15),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH213100459",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=13),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_3 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH204500485",
     product_code="475295A.X21B",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA220250535",
    mac_addr="",
    # trs_connections=[],
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale = Airscale(
    core_units=[_gnb_0_core_unit_0],
    product_code="N/A",
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

_gnb_main = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.164.130/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.164.130/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK130.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 76130
_enb_global_bts_id = 76130

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="EA194950753",
    product_code="473096A.104",
    # slot_id=SlotId.B4
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="6Q174315977",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

enb_radio_unit_0 = RU(
    ru_hw_group="AHFIA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHFIA",
    serial_number="K9183020508",
    product_code="473967A.101",
)

enb_radio_unit_1 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHCA",
    serial_number="AS212504931",
    product_code="473966B.101",
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="N/A")

_bts_enb = RealEnb(
    rms=[enb_radio_unit_0, enb_radio_unit_1],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)


# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue_config = _set_abstract_lib_config_env("ue.yaml")


# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb_main],
    enbs=[_bts_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASOE_APHG_AWHGEQH_ENB_ANDROID"
)

__all__ = ["tl"]
