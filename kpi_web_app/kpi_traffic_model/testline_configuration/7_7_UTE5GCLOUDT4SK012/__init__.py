# Generated with TL configuration generator at 2022-04-11_11:20:52

__maintainer__ = "Adrianna Piotrowska"
__team__ = "MN RAN Pz KRK 7 SG"
__email__ = "I_5G_PZ_MMW_KRK_7SG_TEST@internal.nsn.com"
__owner_email__ = "adrianna.piotrowska@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline import Android, RealEnb
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.nms import NMS, NetAct
from taf.config.testline.pdu import FPFH, PduPort
from taf.config.testline.lmi import SerialOverTcp, Remote
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.12/24",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.83.160.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.12",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.83.160.0"),
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
    v4="10.84.190.12",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.83.160.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.190.12",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.83.160.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.190.12",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.83.160.0"),
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

_gnb_pdu = FPFH(
    addr="fpfh-za11-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_enb_pdu = FPFH(
    addr="fpfh-zb11-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_ru_pdu = FPFH(
    addr="fpfh-za14-46-p09.p09-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK012.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77012
_gnb_global_bts_id = 77012

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="10.84.190.12",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
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

_ru_pdu_port = PduPort(pdu=_ru_pdu, port_no=2)
_common_unit_pdu_port_enb = PduPort(pdu=_enb_pdu, port_no=2)

_radio_unit_0 = RU(
    ru_hw_group="AWEUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="rfsw", password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y="
    ),
    radio_type="AWEUB",
    serial_number="AH211400481",
    product_code="475167A.102",
    pdu_port=_ru_pdu_port,
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-ZA11-04-P04.p04-leg.ska-lab.nsn-rdnet.net"), port=5001)]
    )
)

_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1214902979",
    product_code="475266A.103",
    slot_id=SlotId.B1,
    rus=[_radio_unit_0],
)

_capacity_unit_0_enb = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="EA200750486 ",
    product_code="474020A.102",
    slot_id=SlotId.B1,
)

_common_unit_pdu_port = PduPort(pdu=_gnb_pdu, port_no=3)

_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1214405432",
    mac_addr="00:77:e4:9f:99:d2",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=_common_unit_pdu_port,
)

_airscale_gnb = Airscale(common_units=[_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
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

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_common_unit_enb = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[_capacity_unit_0_enb],
    hardware_type="ASIK",
    hardware_version="A.101",
    serial_number="L1193703760",
    pdu_port=_common_unit_pdu_port_enb,
)

_smod_enb = Airscale(common_units=[_common_unit_enb])

_enb = RealEnb(
    oam_ip=NetworkAddress(
        v4="10.84.190.28",
    ),
    system_module=_smod_enb,
)

_nms = NMS(
    netact=NetAct(
        ssh_connections_info=SshServiceDetails(
            addr="10.41.148.15",
            username="omc",
            password="Medsql!_1893",
        ),
        https_main_info=HttpConnectionDetails(
            addr="srnclab1025lbwas.srnblr.nsn-rdnet.net",
        ),
    ),
)
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
    test_pcs=[_test_pc_gnb_main],
    gnbs=[_gnb_main],
    enbs=[_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIB_ABIO_AWEUB_ENB_NETACT",
    pdus=[_gnb_pdu, _ru_pdu, _enb_pdu],
    nms=_nms,
)

__all__ = ["tl"]
