# Generated with TL configuration generator at 2023-12-13_15:08:35

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
    IperfDataTransferDetails,
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
from taf.config.testline import AppServer
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_gnb_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zb17-28-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin"
)

_enb_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zb17-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin"
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_ru_pdu = HPE(
    port_numbers=[3, 7, 14],
    addr="zb17.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_pdus = [_gnb_pdu, _enb_pdu, _ru_pdu]


# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.8/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.152.8/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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
    v4="10.84.152.8/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.152.8/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.152.8/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK008.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 79008
_gnb_global_bts_id = 79008

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

_gnb_radio_unit_0 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129',
        username='toor4nsn',
        password='oZPS0POrRieRtu',
        proxy=SshServiceDetails(
            addr='7-7-UTE5GCLOUDT8SK008-integration.p08.ska-lab.nsn-rdnet.net',
            username='ute',
            password='ute'
            )
        ),
     radio_type="APHA",
     serial_number="NH184306809",
     product_code="474657A.101",
     pdu_port=_ru_pdu.pdu_ports[7]
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129',
        username='toor4nsn',
        password='oZPS0POrRieRtu',
        proxy=SshServiceDetails(
            addr='7-7-UTE5GCLOUDT8SK008-integration.p08.ska-lab.nsn-rdnet.net',
            username='ute',
            password='ute'
            )
        ),
     radio_type="APHG",
     serial_number="NH225300337",
     product_code="475295A.101",
     pdu_port=_ru_pdu.pdu_ports[3]
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1201005373",
    product_code="474020A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_1],
    )

_gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="B.101",
    serial_number="L1200705463",
    product_code="474020B.101",
    slot_id=SlotId.B5,
    rus=[],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH223342379",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=_gnb_pdu.pdu_ports[2]
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="473098A",
    )

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

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb.connections = [
    Connection(
        device=_gnb.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.152.14/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.152.14/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK014.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
    # connections are not defined because we do not want to perform yaft by
    # CommonAgent (eNb is usually shared between many gNBs)
)

_enb_instance_id = 79014
_enb_global_bts_id = 79014

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

_enb_radio_unit_0 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129',
        username='toor4nsn',
        password='oZPS0POrRieRtu',
        proxy=SshServiceDetails(
            addr='7-7-UTE5GCLOUDT8SK008-integration.p08.ska-lab.nsn-rdnet.net',
            username='ute',
            password='ute'
            )
        ),
     radio_type="APHA",
     serial_number="NH191503748",
     product_code="474657A.101",
     pdu_port=_ru_pdu.pdu_ports[14]
)

_enb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-0a:~",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203791250",
    product_code="473096A.105",
    slot_id=SlotId.B1,
    rus=[_enb_radio_unit_0],
    )

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[_enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="EA190273903",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=_enb_pdu.pdu_ports[5]
)

_airscale_enb = Airscale(
    common_units=[_enb_common_unit_0],
    product_code="473098A",
    )

_enb = RealEnb(
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)


# ------------------------APP_SERVER------------------------------


_app_serv_iperf = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.84.168.120", username="5g", password="5g"
    ),
    network_interface_address="10.84.169.60",
    iperf_path="/usr/bin/iperf",
)

_appserver = AppServer(iperf_details=_app_serv_iperf)



# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIBR_ABILB1_ABILB2_APHG_APHA",
    pdus=_pdus,

)

__all__ = ["tl"]
