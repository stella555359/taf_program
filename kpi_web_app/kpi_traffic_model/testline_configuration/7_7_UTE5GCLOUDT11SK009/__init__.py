# Generated with TL configuration generator at 2023-08-18_10:45:40

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
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
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, SlotId, TRSInterfaces
from taf.config.testline.pdu import PduPort, Pdu
import os
import yaml

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
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
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.82.30.9/23",
    routing_v4=RoutingInformation(gateway="10.82.31.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK009.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_gnb_instance_id = 81009
_gnb_global_bts_id = 81009

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4.split("/")[0],
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
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1194909405",
    product_code="474020A.102",
    # slot_id=SlotId.B3
    )

gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1212903716",
    product_code="474020B.102",
    # slot_id=SlotId.B1
    )

gnb_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1212903726",
    product_code="474020B.102",
    # slot_id=SlotId.B2
    )

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH223342648",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

gnb_radio_unit_1 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

gnb_radio_unit_2 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

gnb_radio_unit_3 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

gnb_radio_unit_4 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

gnb_radio_unit_5 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

gnb_radio_unit_6 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="",
     serial_number="",
     product_code="",
)

_airscale_gnb = Airscale(
    common_units=[gnb_common_unit_0],
    product_code="473098A"
    )

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1, gnb_radio_unit_2, gnb_radio_unit_3, gnb_radio_unit_4, gnb_radio_unit_5, gnb_radio_unit_6],
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


# ------------------------UE_SETTINGS------------------------------


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
    gnbs=[_gnb],

    test_pcs=[_test_pc_gnb],

)

__all__ = ["tl"]
