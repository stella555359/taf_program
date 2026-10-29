# Generated with TL configuration generator at 2025-10-16_12:05:29

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Dominik Wieczorek"
__team__ = "MN_RAN_VRF_KRK_T07"
__email__ = "dominik.wieczorek@nokia.com"

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
from taf.config.testline.nms import NMS, NetAct

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config
    
# ------------------------PDU_CONFIGURATION------------------------

_pdu_1 = FPFH(
    addr="fpfh-zc12-03-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[1, 2, 3, 4, 5, 6],
)

_pdu_2 = FPFH(
    addr="fpfh-zc12-46-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[1, 2, 3, 4, 5, 6],
)

_asik_pdu_port = PduPort(pdu=_pdu_1, port_no=1)
_ru0_pdu_port = PduPort(pdu=_pdu_1, port_no=2)
_ru1_pdu_port = PduPort(pdu=_pdu_1, port_no=3)
_ru2_pdu_port = PduPort(pdu=_pdu_1, port_no=4)
_ru3_pdu_port = PduPort(pdu=_pdu_2, port_no=1)
_enb_pdu_port = PduPort(pdu=_pdu_1, port_no=5)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T09SK145-1.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 80145
_gnb_0_global_bts_id = 80145

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.140.145/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.140.145/23",
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
    v4="10.84.142.145/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.34.145/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.36.145/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
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
    v4="10.255.36.145/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
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
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL2106G10I6",
    product_code="474331A.101",
    pdu_port=_ru1_pdu_port,
    lmi=SerialOverTcp(uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-ZC12-02-P09.p09-leg.ska-lab.nsn-rdnet.net"), port=5001)])
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="K9191330681",
    product_code="474331A.101",
    pdu_port=_ru0_pdu_port,
    lmi=SerialOverTcp(uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-ZC12-01-P09.p09-leg.ska-lab.nsn-rdnet.net"), port=5001)])
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL1930G11JG",
    product_code="474331A.101",
    pdu_port=_ru3_pdu_port,
    lmi=SerialOverTcp(uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-ZC12-04-P09.p09-leg.ska-lab.nsn-rdnet.net"), port=5001)])
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1190604812",
    product_code="474020A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_2],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0],
    hardware_type="ASIK",
    hardware_version="A.102",
    serial_number="L1204106509",
    mac_addr="00:77:e4:1b:96:43",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=_asik_pdu_port,
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

# ------------------------ENB0_CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T09SK145-2.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_0_instance_id = 80025
_enb_0_global_bts_id = 80025

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.84.140.25/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_enb_0_f1m_ip = NetworkAddress(
    v4="10.84.140.25/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_enb_0_radio_unit_0 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2146V0QE5",
    product_code="474216A.101",
    pdu_port=_ru2_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_enb_0_radio_unit_1 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL2106G10I6",
    product_code="474331A.101",
    #pdu_port=_ru1_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_enb_0_radio_unit_2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="K9191330681",
    product_code="474331A.101",
    #pdu_port=_ru0_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="B.101",
    serial_number="L1223310038",
    product_code="475266B.101",
    slot_id=SlotId.B4,
    rus=[_enb_0_radio_unit_0],
)

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1192904072",
    mac_addr="78:f9:b4:aa:c9:cb",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=_enb_pdu_port
)

_enb_0_airscale = Airscale(
    common_units=[_enb_0_common_unit_0],
    product_code="473098A",
)

_enb_0 = RealEnb(
    x2_link_addr=_enb_0_oam_ip,
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

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# ------------------------TL_CONFIGURATION------------------------
# =========== Active MantaRay =============
_nms = NMS(
    netact=NetAct(
        ssh_connections_info=SshServiceDetails(
            addr="10.63.2.155",
            username="omc",
            password="Medsql!_1893",
        ),
        https_main_info=HttpConnectionDetails(
            addr="srnclab1052lbwas.srnblr.nsn-rdnet.net",
        ),
    ),
)
# =========== Active MantaRay =============

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_enb_0],
    nms=_nms,
    ues=[_ue_config],
    test_pcs=[_test_pc_gnb_0, _test_pc_enb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIK_ABIL_AHLOA_SFP+QSFP_ENB",
)
tl.netact_dn = "PLMN-PLMN/MRBTS-80145"
tl.working_set = "CNI130136-9SK145"

__all__ = ["tl"]
