# Generated with TL configuration generator at 2022-10-11_14:06:21

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
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
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort
from taf.config.testline.ue import MediaTek
from taf.config.testline.attenuator import JFW
import os
import yaml

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
    v4="10.255.20.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.22.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.148.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.22.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.148.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.255.22.86/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK086.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77086
_gnb_global_bts_id = 77086

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
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

gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="A.102",
    serial_number="L1213805968",
    product_code="474824A.102",
    slot_id=SlotId.B3,
)

gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="AH185100979",
    product_code="473096A.103",
    slot_id=SlotId.B2,
)

gnb_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="K9181626380",
    product_code="473096A.103",
    slot_id=SlotId.B1,
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1201106414",
    mac_addr="00:77:e4:07:3e:c1",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="AHEJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="umniedziala"
    ),
    radio_type="AHEJ",
    serial_number="EB192761051",
    product_code="474513A.102",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="FHFB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.128", username="root", password="umniedziala"
    ),
    radio_type="FHFB",
    serial_number="K9193742092",
    product_code="473042A.202",
)

gnb_radio_unit_2 = RU(
    ru_hw_group="ARDA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    radio_type="ARDA",
    serial_number="K9203309864",
    product_code="474840A.101",
)

gnb_radio_unit_3 = RU(
    ru_hw_group="ARDA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="root", password="umniedziala"
    ),
    radio_type="ARDA",
    serial_number="K9223348219",
    product_code="474840A.101",
)

gnb_radio_unit_4 = RU(
    ru_hw_group="FHFB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.130", username="root", password="umniedziala"
    ),
    radio_type="FHFB",
    serial_number="K9193742090",
    product_code="473042A.202",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[
        gnb_radio_unit_0,
        gnb_radio_unit_1,
        gnb_radio_unit_2,
        gnb_radio_unit_3,
        gnb_radio_unit_4,
    ],
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

# -------------------------UE_PC-----------------------------------

_appserver_ssh = SshServiceDetails(addr="10.84.168.121", username="5g", password="5g")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.84.169.61",
)

_elt_path = "/cygdrive/c/Mediatek/ELT"

_mtk = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="plkr-ska-008.p04.ska-lab.nsn-rdnet.net",
        username="pzkrk",
        password="NokiaBts2003",
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="351901032120325",
    apn_url="5gsakrk",
    serial_number="lepin",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE"],
)

# ------------------------Attenuator------------------------------

_attenuator = JFW(
    ip_addr="10.255.13.182",
    port=3001,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="50PA-628",
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    attenuator=[_attenuator],
)

__all__ = ["tl"]
