# Generated with TL configuration generator at 2023-10-31_11:07:08

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Szymon Mastalski"
__team__ = "MN_RAN_PZ_KRK_6"
__email__ = "szymon.mastalski@nokia.com"

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
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.airscale import Airscale, CommonUnit, CoreUnit, CapacityUnit, SlotId, TRSInterfaces
from taf.config.testline.pdu import PduPort, Pdu, FPFH
import os
import yaml

attenuator_ports = list(range(1, 257))
# ------------------------GNB_CONFIGURATION------------------------

_attenuator = RadioRack(
    ip_addr="10.255.40.78",
    port="50000",
    attenuation_port_numbers=attenuator_ports,
)


_gnb_oam_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1c_ip_1 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_f1u_ip_1 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2c_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip_1 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip_1 = NetworkAddress(
    v4="10.84.190.94/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)
_gnb_oam_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1c_ip_2 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_f1u_ip_2 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2c_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip_2 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip_2 = NetworkAddress(
    v4="10.84.190.97/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK094-1.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!")
)
_test_pc_gnb_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK094-2.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!")
)

_gnb_instance_id_1 = 77094
_gnb_global_bts_id_1 = 77094

_gnb_instance_id_2 = 77097
_gnb_global_bts_id_2 = 77097

_gnb_pdu1 = FPFH(
    port_numbers=[5,6],
    addr="fpfh-ze03-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_pdu2 = FPFH(
    port_numbers=[1,2,3,4],
    addr="fpfh-ze03-35-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdus = [_gnb_pdu1, _gnb_pdu2]
_default_gnb_ssh_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_default_gnb_ssh_lmp_connection_2 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_2.default_ssh_connection_details,
)

_default_oam_http_connection_1 = HttpConnectionDetails(
    addr=_gnb_oam_ip_1.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)
_default_oam_http_connection_2 = HttpConnectionDetails(
    addr=_gnb_oam_ip_2.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_oam_ip_1,
    oam_ssh_connection_details=_default_gnb_ssh_lmp_connection_1,
    oam_http_connection_details=_default_oam_http_connection_1,
    f1m=_gnb_f1m_ip_1,
    f1c=_gnb_f1c_ip_1,
    f1u=_gnb_f1u_ip_1,
    x2c=_gnb_x2c_ip_1,
    x2u=_gnb_x2u_ip_1,
    s1c=_gnb_s1c_ip_1,
    s1u=_gnb_s1u_ip_1,
    xnc=_gnb_xnc_ip_1,
    xnu=_gnb_xnu_ip_1,
    ngc=_gnb_ngc_ip_1,
    ngu=_gnb_ngu_ip_1,
    instance_id=_gnb_instance_id_1,
    global_bts_id=_gnb_global_bts_id_1,
)
_cu_gnb_2= CU(
    backhaul_site_oam_ip=_gnb_oam_ip_2,
    oam_ssh_connection_details=_default_gnb_ssh_lmp_connection_2,
    oam_http_connection_details=_default_oam_http_connection_2,
    f1m=_gnb_f1m_ip_2,
    f1c=_gnb_f1c_ip_2,
    f1u=_gnb_f1u_ip_2,
    x2c=_gnb_x2c_ip_2,
    x2u=_gnb_x2u_ip_2,
    s1c=_gnb_s1c_ip_2,
    s1u=_gnb_s1u_ip_2,
    xnc=_gnb_xnc_ip_2,
    xnu=_gnb_xnu_ip_2,
    ngc=_gnb_ngc_ip_2,
    ngu=_gnb_ngu_ip_2,
    instance_id=_gnb_instance_id_2,
    global_bts_id=_gnb_global_bts_id_2,
)

_gnb_radio_unit_2 = RU(
     ru_hw_group="AZQI",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="),
     radio_type="AZQI",
     serial_number="1M223205308",
     product_code="475243A.101",
     pdu_port=_gnb_pdu2.pdu_ports[4]
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="AHFII",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="),
     radio_type="AHFII",
     serial_number="BL2317N451U",
     product_code="475656A.101",
     pdu_port=_gnb_pdu2.pdu_ports[1]
)
_gnb_radio_unit_3 = RU(
     ru_hw_group="AKQJ",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="),
     radio_type="AKQJ",
     serial_number="1M222011920",
     product_code="475824A.101",
     pdu_port=_gnb_pdu2.pdu_ports[3]
)

_gnb_radio_unit_4 = RU(
     ru_hw_group="AZQS",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="),
     radio_type="AZQS",
     serial_number="1M222504398",
     product_code="475664A.101",
     pdu_port=_gnb_pdu2.pdu_ports[2]
)


_gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.102",
    serial_number="L1205102754",
    product_code="475266A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_1],
    )

_gnb_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204301233",
    product_code="475266A.101",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_2],
    )
_gnb_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1225109436",
    product_code="475266A.105",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_3, _gnb_radio_unit_4],
    )

_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection_1,
    capacity_units=[_gnb_capacity_unit_1, _gnb_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1203606148",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=_gnb_pdu1.pdu_ports[5]
)
_gnb_common_unit_2 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection_2,
    capacity_units=[_gnb_capacity_unit_3],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1200500391",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=_gnb_pdu1.pdu_ports[6]
)
_airscale_gnb_1 = Airscale(
    common_units=[_gnb_common_unit_1],
    product_code="473098A"
    )
_airscale_gnb_2 = Airscale(
    common_units=[_gnb_common_unit_2],
    product_code="473098A"
    )

_du_gnb_1 = DU(
    airscale=_airscale_gnb_1,
    oam_ip=_gnb_oam_ip_1,
    f1_m_ip_addr=_gnb_f1m_ip_1,
    f1_c_ip_addr=_gnb_f1c_ip_1,
    f1_u_ip_addr=_gnb_f1u_ip_1,
    f1_m_cu=_gnb_f1m_ip_1,
    f1_c_cu=_gnb_f1c_ip_1,
    f1_u_cu=_gnb_f1u_ip_1,
    instance_id=_gnb_instance_id_1,
    global_bts_id=_gnb_global_bts_id_1,
    )
_du_gnb_2 = DU(
    airscale=_airscale_gnb_2,
    oam_ip=_gnb_oam_ip_2,
    f1_m_ip_addr=_gnb_f1m_ip_2,
    f1_c_ip_addr=_gnb_f1c_ip_2,
    f1_u_ip_addr=_gnb_f1u_ip_2,
    f1_m_cu=_gnb_f1m_ip_2,
    f1_c_cu=_gnb_f1c_ip_2,
    f1_u_cu=_gnb_f1u_ip_2,
    instance_id=_gnb_instance_id_2,
    global_bts_id=_gnb_global_bts_id_2,
    )

_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id=_gnb_instance_id_1,
    global_bts_id=_gnb_global_bts_id_1,
)
_gnb_2 = ClassicalBts(
    cu=_cu_gnb_2,
    dus=[_du_gnb_2],
    instance_id=_gnb_instance_id_2,
    global_bts_id=_gnb_global_bts_id_2,
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

# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue = _set_abstract_lib_config_env("ue_config.yaml")
# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_1,
    gnbs=[_gnb_1,_gnb_2],
    pdus=[_pdus],
    attenuators=[_attenuator],
    test_pcs=[_test_pc_gnb_1,_test_pc_gnb_2],
    tl_cloud_topology='CLOUD_5G_CLASSICAL_QC_MULTIGNB_SA_ASIBL_2xABIOB1B2_ASIBR_1xABIOB4_AZQI_AHFII_AZQU_AZQS'
)

__all__ = ["tl"]
