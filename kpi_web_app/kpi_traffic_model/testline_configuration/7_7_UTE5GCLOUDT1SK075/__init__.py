# Generated with TL configuration generator at 2023-01-26_12:23:48

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
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, ATEN, FPFH, HPE
from taf.config.testline.pdu import PduPort, Pdu
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# ------------------------GNB_CONFIGURATION------------------------


_gnb_oam_ip = NetworkAddress(
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
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

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK075.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 76075
_gnb_global_bts_id = 76075

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
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
    addr="192.168.253.24",
    hardware_type="ABIO",
    hardware_version="A.102",
    serial_number="L1211110923",
    product_code="475266A.102",
    # slot_id=SlotId.B2
)

gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203290579",
    product_code="473096A.105",
    # slot_id=SlotId.B1
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1213609064",
    mac_addr="",
    pdu_port=PduPort(
        pdu=FPFH(
            port_numbers=[5],
            addr="fpfh-zc03-48-p01.p01-leg.ska-lab.nsn-rdnet.net",
            login="admin",
            password="admin",
        ),
        port_no=5,
    ),
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

gnb_radio_unit_0 = RU(
    ru_hw_group="AEWD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="l/yVyoAz8UicxCwrUj7r5uawuzTkoqmu2isWJ1jft0A=",
    ),
    pdu_port=PduPort(
        pdu=FPFH(
            port_numbers=[6],
            addr="fpfh-zc03-48-p01.p01-leg.ska-lab.nsn-rdnet.net",
            login="admin",
            password="admin",
        ),
        port_no=6,
    ),
    radio_type="AEWD",
    serial_number="AH195002822",
    product_code="474612A.102",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="AEWD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="l/yVyoAz8UicxCwrUj7r5uawuzTkoqmu2isWJ1jft0A=",
    ),
    pdu_port=PduPort(
        pdu=HPE(
            addr="zc03.mgt.ska-lab.nsn-rdnet.net",
            port_numbers=[6],
            snmp_user=_snmp_user,
        ),
        port_no=6,
    ),
    radio_type="AEWD",
    serial_number="AH202600007",
    product_code="474612A.102",
)

gnb_radio_unit_2 = RU(
    ru_hw_group="AHIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHIB",
    serial_number="AH222704056",
    product_code="474050A.103",
    pdu_port=PduPort(
        pdu=FPFH(
            addr="fpfh-zd03-48-p01.p01-leg.ska-lab.nsn-rdnet.net",
            port_numbers=[2],
            login="admin",
            password="admin",
        ),
        port_no=2,
    ),
)

gnb_radio_unit_3 = RU(
    ru_hw_group="AEWD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="l/yVyoAz8UicxCwrUj7r5uawuzTkoqmu2isWJ1jft0A=",
    ),
    pdu_port=PduPort(
        pdu=FPFH(
            port_numbers=[4],
            addr="fpfh-zc03-20-p01.p01-leg.ska-lab.nsn-rdnet.net",
            login="admin",
            password="admin",
        ),
        port_no=4,
    ),
    radio_type="AEWD",
    serial_number="AH194601590",
    product_code="474612A.102",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1, gnb_radio_unit_2, gnb_radio_unit_3],
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

_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_classical_bts_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

# ------------------------ENB_CONFIGURATION------------------------


_enb_oam_ip = NetworkAddress(
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.164.75/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK075.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 76075
_enb_global_bts_id = 76075

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.24",
    hardware_type="ABIO",
    hardware_version="A.102",
    serial_number="L1211110923",
    product_code="475266A.102",
    # slot_id=SlotId.B2
)

enb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203290579",
    product_code="473096A.105",
    # slot_id=SlotId.B1
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0, enb_capacity_unit_1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1213609064",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

enb_radio_unit_0 = RU(
    ru_hw_group="AHIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHIB",
    serial_number="AH222704056",
    product_code="474050A.103",
)

enb_radio_unit_1 = RU(
    ru_hw_group="AEWD",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AEWD",
    serial_number="AH195002822",
    product_code="474612A.102",
)

enb_radio_unit_2 = RU(
    ru_hw_group="AEWD",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AEWD",
    serial_number="AH202600007",
    product_code="474612A.102",
)

enb_radio_unit_3 = RU(
    ru_hw_group="AEWD",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AEWD",
    serial_number="AH194601590",
    product_code="474612A.102",
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_lte_enb = RealEnb(
    rms=[enb_radio_unit_0, enb_radio_unit_1, enb_radio_unit_2, enb_radio_unit_3],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------------TL_CONFIGURATION------------------------

# Testline

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")
_test_pc_gnb_main.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]
tl = TestLine(
    test_pc=_test_pc_gnb_main,
    test_pcs=[_test_pc_gnb_main, _test_pc_enb],
    gnbs=[_classical_bts_gnb_main],
    enbs=[_lte_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASILL_ABIAB1_ABIOB2_2xAEWD",
)

__all__ = ["tl"]
