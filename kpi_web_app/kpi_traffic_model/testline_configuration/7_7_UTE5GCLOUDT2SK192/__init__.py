# Generated with TL configuration generator at 2023-08-04_09:17:07

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
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
)
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.ue import Android, TafUeAndroid

# ------------------------GNB_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[3, 4],
    addr="fpfh-zh11-34-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",
}

_ru_pdu = HPE(
    port_numbers=[7, 9, 10],  # update port_no
    addr="zh11.mgt.ska-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

_gnb_oam_ip = NetworkAddress(
    v4="10.84.132.192/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.132.192/23",
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
    v4="10.84.132.192/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.132.192/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.132.192/23",
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

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK192.p02.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)


_gnb_instance_id = 78192
_gnb_global_bts_id = 78192

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


# gnb_radio_unit_0 = RU(
#     ru_hw_group="APHA",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     radio_type="APHA",
#     serial_number="NH193100259",
#     product_code="474657A.101",
# )

# gnb_radio_unit_1 = RU(
#     ru_hw_group="APHA",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     radio_type="APHA",
#     serial_number="NH193100187",
#     product_code="474657A.101",
# )

_ru_hub_0 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    radio_type="APHA",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="7-7-UTE5GCLOUDT1SK333.p01.ska-lab.nsn-rdnet.net",
                username="ute",
                password="ute",
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    serial_number="EA192472687",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=9),
)

_ru_hub_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    radio_type="APHA",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="7-7-UTE5GCLOUDT1SK444.p01.ska-lab.nsn-rdnet.net",
                username="ute",
                password="ute",
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    serial_number="EA192472687",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=10),
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1190102691",
    product_code="474020A.102",
    rus=[_ru_hub_0, _ru_hub_1],
    # slot_id=SlotId.B4
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    hardware_type="ASIK",
    hardware_version="A.102",
    serial_number="EA192472687",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    # rus=[_ru_hub_0, _ru_hub_1],
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

_enb_oam_ip = NetworkAddress(
    v4="10.84.164.191/23",
    routing_v4=RoutingInformation(gateway="10.84.164.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.164.191/23",
    routing_v4=RoutingInformation(gateway="10.84.164.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK191.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_enb_instance_id = 76191
_enb_global_bts_id = 76191

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="L1171719984",
    product_code="473096A.103",
    # slot_id=SlotId.B1
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.101",
    serial_number="L1201000264",
    mac_addr="",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=3),
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

enb_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="APHA",
    serial_number="BL2124V0EDJ",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=7),
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_enb = RealEnb(
    rms=[enb_radio_unit_0],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)


##### UE CONFIG

_appserver_ssh = SshServiceDetails(addr="10.84.168.120", username="5g", password="5g")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.84.169.60",
)

ue_ssh = SshServiceDetails(
    addr="plkr-sc5g-pc78.intra.noklab.net",
    username="pzkrk",
    password="NokiaBts2003",
)

ue1 = Android(
    ssh_connection_details=ue_ssh,
    serial_number="R3CR20KS4NA",
    server_dir="C:/pyro_server",
    python_path="C:/Users/pzkrk/AppData/Local/Programs/Python/Python36/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

#### TAF UE PROXY ANDROID CONFIG

_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.84.168.120",
    user="5g",
    password="5g",
    bind_interface_ip="10.84.169.60",
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf", app_server=_app_server_1, version=3
)

_android1 = TafUeAndroid(
    serial_number="R3CR20KS4NA",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    ue_pc_address="plkr-sc5g-pc78.intra.noklab.net",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=ue_ssh,
    ue_pc_port="80",
)

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb],
    ues=[_android1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_NSA_ABIL_ASIK_2xAPHA",
)

__all__ = ["tl"]
