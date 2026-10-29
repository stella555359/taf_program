# Generated with TL configuration generator at 2024-01-09_16:20:23

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "5G_PZ_MMW_KRK_8_SG"
__email__ = "I_MN_RAN_PZ_KRK_SG_8@internal.nsn.com"

import os

import yaml
from taf.config.testline import AppServer
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.radio import RU
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],  # update port_no
    addr="fpfh-zg03-24-p08.p08-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_bts_pdu2 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],  # update port_no
    addr="fpfh-zg03-48-p08.p08-leg.ska-lab.nsn-rdnet.net",  # update address
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
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9],  # update port_no
    addr="zg03.mgt.ska-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK013.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 78113
_gnb_0_global_bts_id = 78113

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.152.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.152.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
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
    v4="10.84.154.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.30.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=506,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.30.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=506,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.152.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=504,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.84.152.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=504,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.152.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
    vlan_id=504,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.84.152.13/23",
    routing_v4=RoutingInformation(gateway="10.255.31.254", destIpAddr="10.84.169.0"),
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
    ru_hw_group="AZQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZQU",
    serial_number="4H210730019",
    product_code="475665A.101",
    pdu_port=PduPort(
        pdu=_bts_pdu1, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUA",
    serial_number="AH204200496",
    product_code="475166A.103",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA220351093",
    product_code="473484A.101",
    pdu_port=PduPort(
        pdu=_bts_pdu2, port_no=1
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AWKUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AWKUA",
    serial_number="YK234900014",
    product_code="476237A.X21",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=6
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104652",
    product_code="475266A.101",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_2],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104654",
    product_code="475266A.101",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_1],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH221046321",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104654",
    product_code="475266A.101",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_3],
)
_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1213105583",
    mac_addr="00:77:e4:8e:3e:74",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu2, port_no=1
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

# ------------------------AppServer CONFIGURATION------------------------

_app_serv_iperf = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.84.168.121", username="5g", password="5g"
    ),
    network_interface_address="10.84.169.61",
    iperf_path="/data/data/com.nokia.android.application/",
)

_appserver = AppServer(iperf_details=_app_serv_iperf)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_yaml_config = _set_abstract_lib_config_env("ue.yaml")

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIL_ABIA_2xABIL_AHFB_AHFIB_AWEUA_AHLOA",
    appserver=_appserver,
)

__all__ = ["tl"]
