# Generated with TL configuration generator at 2025-07-28_13:15:18

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
from taf.config.testline.optical_switch import Leoni, SwitchChannel, SwitchModule
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.lmi import SerialOverTcp, Remote
import os
import yaml


# -------------------OPTICAL_SWITCH_CONFIGURATION------------------


_optical_switch = Leoni(addr='10.255.40.43', model='mol 5x(2x6)', port=10001)

_switch_module = SwitchModule(optical_switch=_optical_switch, module_no=5, channel_amount=6)
_switch_channel_1 = SwitchChannel(optical_switch=_optical_switch, switch_module=_switch_module, channel_no=1)
_switch_channel_2 = SwitchChannel(optical_switch=_optical_switch, switch_module=_switch_module, channel_no=2)


# ------------------------PDU_CONFIGURATION------------------------


_bts_pdu = FPFH(
    port_numbers=[4],
    addr="fpfh-za14-46-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu = FPFH(  # 2xAHPF
    port_numbers=[2, 3],
    addr="fpfh-za13-46-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_1 = FPFH(  # AZQP
    port_numbers=[1],
    addr="fpfh-za14-12-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(  # AZQS match
    port_numbers=[6],
    addr="fpfh-za14-34-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------


_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T9SK008.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 80008
_gnb_0_global_bts_id = 80008

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.140.8/23",
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
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.84.140.8/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
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
    ru_hw_group="AHPF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    radio_type="AHPF",
    serial_number="EA210951228",
    product_code="475798A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=2),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHPF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    radio_type="AHPF",
    serial_number="EA210951229",
    product_code="475798A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=3),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AZQP",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZQP",
    serial_number="1M203665282",
    product_code="475198A.102",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=1),
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AZQS",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZQS",
    optical_switch_channels=[
       _switch_channel_1,
       _switch_channel_2
     ],
    serial_number="1M231308378",
    product_code="475664A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=6),
)

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA213353842",
    mac_addr="78:f9:b4:dc:e6:7",
    # trs_connections=[TRSInterfaces.EIF1],
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
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

_gnb_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_7_7_T9SK008",
)

__all__ = ["tl"]
