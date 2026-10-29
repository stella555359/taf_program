# Generated with TL configuration generator at 2023-04-11_16:58:10

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline import (
    TafUeAppServer,
    TafUeDataTransferProtocol,
    TafUeAndroid,
    Android,
    Connection,
)

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
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
from taf.config.testline import Connection
from taf.config.testline.pdu import PduPort, Pdu, FPFH
from taf.config.testline.ue import Android
from taf.config.testline import JFW
import os
import yaml

# ------------------------GNB_CONFIGURATION------------------------

_pdu1 = FPFH(
    addr="fpfh-ze11-39-p04.p04-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1],
    login="admin",
    password="admin",
)

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.84.190.118/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_instance_id = 77118
_gnb_global_bts_id = 77118

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK118.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
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
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1201302427",
    product_code="474020B.102",
    # slot_id=SlotId.B1
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    pdu_port=_pdu1.pdu_ports[1],
    hardware_type="ASIK",
    hardware_version="A.102",
    serial_number="L1204810250",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu1.pdu_ports[1],
    radio_type="APHA",
    serial_number="NH224900148",
    product_code="474657A.103",
)

_ru_1 = SC5GRadio(
    ru_hw_group="APHA",
    radio_type="APHA",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="7-7-UTE5GCLOUDT4SK025.p04.ska-lab.nsn-rdnet.net",
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
    pdu_port=_pdu1.pdu_ports[1],
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_1],
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

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.190.117/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.190.117/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK117.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 77117
_enb_global_bts_id = 77117

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1170401188",
    product_code="473096A.103",
    # slot_id=SlotId.B4
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    pdu_port=_pdu1.pdu_ports[1],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="L1182807494",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

enb_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129", username="root", password="umniedziala"
    ),
    pdu_port=_pdu1.pdu_ports[1],
    radio_type="APHA",
    serial_number="NH223400196",
    product_code="474657A.102",
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

# ------------------TafUeAndroid--------------------

_realcore_appsrv = TafUeAppServer(
    app_server_name="realcore",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g",
)

_iperf_ue_sa = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_realcore_appsrv,
    # binary_path='/data/data/com.nokia.android.application/',
    interval=1,
    # server_close_delay=50
)

_android_ue_1 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.84.182.7",
        username="plkrsg4",
        password="Rz0dkiewk@2022",
    ),
    ue_pc_address="PLKR-UEPC-SG4-3.intra.noklab.net",
    serial_number="35ea0ce3",
    capabilities=["REAL_ANDROID_UE"],
    data_transfer=[_iperf_ue_sa],
    network_mode_switch_method="ADB",
)


# AppServer CONFIGURATION

_appserver_ssh = SshServiceDetails(addr="10.84.168.120", username="5g", password="5g")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.84.169.60",
)

# UE CONFIGURATION

_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.84.182.7", username="plkrsg4", password="Rz0dkiewk@2022"
    ),
    serial_number="35ea0ce3",
    server_dir="C:/pyro_server",
    iperf_directory="/data/data/com.nokia.android.application/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    pdu_port=_pdu1.pdu_ports[1],
)

# ATTENUATOR CONFIGURATION

_attenuator = JFW(
    ip_addr="10.255.13.82",
    port=3001,
    attenuation_port_numbers=range(1, 12),
)


_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK118.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_gnb.dus[0].airscale.common_units[0],
        ),
    ],
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    ues=[_android_ue_1],
    attenuator=_attenuator,
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIK_ABIL_APHA",
    pdus=[_pdu1],
)

__all__ = ["tl"]
