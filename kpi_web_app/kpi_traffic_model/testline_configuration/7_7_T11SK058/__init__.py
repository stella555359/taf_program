# Generated with TL configuration generator at 2025-10-21_08:29:36

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
    port_numbers=[1, 2, 3, 4],  # update port_no
    addr="FPFH-ZI12-46-P11.p11-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_gnb_ru_pdu_1 = FPFH(
    port_numbers=[3, 4],
    addr="FPFH-ZI12-34-P11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_ru_pdu_2 = FPFH( #aqqF
    port_numbers=[1, 2, 3],
    addr="fpfh-ZI11-01-p06.p06-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_ru_pdu_3 = FPFH(
    port_numbers=[4, 5, 6], #azna
    addr="fpfh-zi10-01-p06.p06-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_ru_pdu_4 = FPFH(
    port_numbers=[3],
    addr="fpfh-zk04-25-p11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------HPE_CONFIGURATION------------------------


_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",  # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[11],  # update port_no
    addr="ZK04.mgt.ska-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------


_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK058-1.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK058-2.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 81058
_gnb_0_global_bts_id = 81058

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_secondary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0_secondary.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.255.50.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.82.30.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.82.30.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.82.30.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.82.30.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.82.30.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.82.28.58/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    ru_hw_group="AQQF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQF",
    serial_number="K9234728704",
    product_code="475922A.101",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_2, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AQQF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQF",
    serial_number="K9234728724",
    product_code="475922A.101",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_2, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AZNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AZNA",
    serial_number="EA203554836",
    product_code="473914A.203",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_3, port_no=5
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AQQF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQF",
    serial_number="K9234728707",
    product_code="475922A.101",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_2, port_no=1
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="FRGT",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FRGT",
    serial_number="F7173619160",
    product_code="472810A.102",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_1, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="ARDB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="ARDB",
    serial_number="L1194805088",
    product_code="475122A.101",
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AREA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AREA",
    serial_number="EA223060836",
    product_code="474198A.101",
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AWKUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AWKUC",
    serial_number="AH251102437",
    product_code="476239A.103",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=11
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AZNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AZNA",
    serial_number="EA204352021",
    product_code="473914A.203",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_3, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AWKUD",
    serial_number="AH244716944",
    product_code="476240A.102",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_4, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AZNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AZNA",
    serial_number="6Q174625271",
    product_code="473914A.102",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_1, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_11 = RU(
    ru_hw_group="AZNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AZNA",
    serial_number="6Q190504268",
    product_code="473914A.102",
    pdu_port=PduPort(
        pdu=_gnb_ru_pdu_3, port_no=6
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH215140160",
    product_code="475266A.103",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_9],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.46",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH214748337",
    product_code="475266A.103",
    slot_id=SlotId.B6,
    rus=[_gnb_0_radio_unit_7],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="6Q184857123",
    product_code="473096A.103",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_10, _gnb_0_radio_unit_11],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233201702",
    product_code="475792A.102",
    slot_id=SlotId.B4,
    rus=[
        _gnb_0_radio_unit_0,
        _gnb_0_radio_unit_1,
        _gnb_0_radio_unit_3,
        _gnb_0_radio_unit_4,
        _gnb_0_radio_unit_6,
    ],
)

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="6Q174825200",
    product_code="473096A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_2, _gnb_0_radio_unit_8],
)

_gnb_0_capacity_unit_5 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="EA194751603",
    product_code="473096A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_4, _gnb_0_radio_unit_5, _gnb_0_radio_unit_6],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_3,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233302539",
    mac_addr="28:74:f5:09:fd:48",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_2,
        _gnb_0_capacity_unit_4,
        _gnb_0_capacity_unit_5,
    ],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1213300054",
    mac_addr="28:74:f5:09:fd:48",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=1
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0, _gnb_0_common_unit_1],
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

_test_pc_gnb_0_secondary.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[1],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_set_abstract_lib_config_env("ue.yaml")

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ASIMR_ABIA3L_ABIO2R_ABIPR_AREA_FRGT_ARDB_3xAQQF_4xAZNA_AWKUC_AWKUD",
)

__all__ = ["tl"]
