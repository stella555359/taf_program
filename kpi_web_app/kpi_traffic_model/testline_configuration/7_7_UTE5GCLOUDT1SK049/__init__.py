# Generated with TL configuration generator at 2025-08-05_15:21:14

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
from taf.config.testline.lmi import SerialOverTcp, Remote, LMI, SerialOverHost, Local

import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


# ------------------------GNB0_PDU_CONFIGURATION------------------------


_gnb_0_bts_pdu = FPFH(
    port_numbers=[3],  # update port_no
    addr="fpfh-zg17-48-p01.p01-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",  # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_gnb_0_ru_pdu = HPE(
    port_numbers=[2, 3, 4],  # update port_no
    addr="zg17.mgt.ska-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK049.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 76049
_gnb_0_global_bts_id = 76049

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.164.49/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.84.169.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.164.49/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.84.169.0"),
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
    v4="10.84.150.49/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.84.169.0"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.6.49/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.84.169.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.8.49/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.84.169.0"),
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

_awguc_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.100.1",
    username="rfsw",
    password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y=",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AWGUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWGUC",
    serial_number="AH242011029",  # AH242500681 AH242011029
    product_code="475946A.103",
    pdu_port=PduPort(
        pdu=_gnb_0_ru_pdu, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.10.124"), port=2001)]
    ),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AWGUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWGUC",
    serial_number="AH214214383",  # AH214700900, AH214214383
    product_code="475946A.101",
    pdu_port=PduPort(
        pdu=_gnb_0_ru_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.10.122"), port=2001)]
    ),
    # lmi=SerialOverHost(
    #     host=TestPc(
    #         default_ssh_connection_details=SshServiceDetails(
    #             addr="plkr-tp-ue29.intra.noklab.net",
    #             username="noklab\plkrsg09",
    #             password="ssp123!!Macro",
    #         )
    #     ),
    #     uart_mapping=[Local(port="COM55")],
    # ),
    # lmp_connection=_awguc_ssh_lmp_connection,
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AWGUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWGUC",
    serial_number="AH242011003",  # AH242500666, AH242011003
    product_code="475946A.103",
    pdu_port=PduPort(
        pdu=_gnb_0_ru_pdu, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.10.123"), port=2001)]
    ),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH214748384",
    product_code="475266A.103",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH222046110",
    product_code="475266A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_2],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH220745482",
    product_code="475266A.103",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_1],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406270",
    mac_addr="28:74:f5:0b:5b:6",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_gnb_0_bts_pdu, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------------enb_0_PDU_CONFIGURATION------------------------

_enb_0_bts_pdu = FPFH(
    port_numbers=[2],  # update port_no
    addr="fpfh-zh17-48-p01.p01-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_enb_0_ru_pdu = FPFH(
    port_numbers=[2],  # update port_no
    addr="fpfh-zh17-22-p01.p01-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)
# ------------------------ENB0_CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK056.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_0_instance_id = 76056
_enb_0_global_bts_id = 76056

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.84.164.56/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.44.201.68"),
    vlan_id=504,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.84.164.56/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.44.201.68"),
    vlan_id=504,
)

_enb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_enb_0_oam_http_connection = HttpConnectionDetails(
    addr=_enb_0_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_enb_0 = CU(
    backhaul_site_oam_ip=_enb_0_oam_ip,
    oam_ssh_connection_details=_enb_0_primary_ssh_lmp_connection,
    oam_http_connection_details=_enb_0_oam_http_connection,
    f1m=_enb_0_f1m_ip,
    f1c=_enb_0_f1c_ip,
    f1u=_enb_0_f1u_ip,
    x2c=_enb_0_x2c_ip,
    x2u=_enb_0_x2u_ip,
    s1c=_enb_0_s1c_ip,
    s1u=_enb_0_s1u_ip,
    xnc=_enb_0_xnc_ip,
    xnu=_enb_0_xnu_ip,
    ngc=_enb_0_ngc_ip,
    ngu=_enb_0_ngu_ip,
    instance_id=_enb_0_instance_id,
    global_bts_id=_enb_0_global_bts_id,
)

_enb_0_radio_unit_0 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL1923V0A75",
    product_code="474216A.101",
    pdu_port=PduPort(
        pdu=_enb_0_ru_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="EA185183624",
    product_code="473096A.103",
    slot_id=SlotId.B4,
    rus=[_enb_0_radio_unit_0],
)

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.204",
    serial_number="DH210566396",
    mac_addr="00:77:e4:49:51:7",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(
        pdu=_enb_0_bts_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_0_airscale = Airscale(
    common_units=[_enb_0_common_unit_0],
    product_code="473098A",
)

_du_enb_0 = DU(
    airscale=_enb_0_airscale,
    oam_ip=_enb_0_oam_ip,
    f1_m_ip_addr=_enb_0_f1m_ip,
    f1_c_ip_addr=_enb_0_f1c_ip,
    f1_u_ip_addr=_enb_0_f1u_ip,
    f1_m_cu=_enb_0_f1m_ip,
    f1_c_cu=_enb_0_f1c_ip,
    f1_u_cu=_enb_0_f1u_ip,
    instance_id=_enb_0_instance_id,
    global_bts_id=_enb_0_global_bts_id,
)

_enb_0 = ClassicalBts(
    cu=_cu_enb_0,
    dus=[_du_enb_0],
    instance_id=_enb_0_instance_id,
    global_bts_id=_enb_0_global_bts_id,
)

_test_pc_enb_0.connections = [
    Connection(
        device=_enb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------
_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    # pdus=[_gnb_0_bts_pdu, _gnb_0_ru_pdu, _enb_0_bts_pdu, _enb_0_ru_pdu],
    # gnbs=[_gnb_0, _enb_0],
    # test_pcs=[_test_pc_gnb_0, _test_pc_enb_0],
    pdus=[_gnb_0_bts_pdu, _gnb_0_ru_pdu],
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIML_ABIOB1B2B3_AWGUC",
)

__all__ = ["tl"]
