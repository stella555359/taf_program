# Generated with TL configuration generator at 2023-06-20_14:13:45

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "David Jollivet"
__team__ = "RAN PZ NPS SG01"
__email__ = "david.jollivet@nokia.com"

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

# --- UE ---

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.14.48.173/23",
    routing_v4=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=1000,
) 

_gnb_f1m_ip = NetworkAddress(
    v4="10.14.48.173/23",
    routing_v4=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=1000,
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
    v6="2a00:8a00:40ff:c000:2:11:3002:5/112",
    routing_v6=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=3500,
) 

_gnb_x2u_ip = NetworkAddress(
    v6="2a00:8a00:40ff:c000:2:11:3002:9/112",
    routing_v6=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=3500,
) 

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_s1u_ip = NetworkAddress(
    v6="2a00:8a00:40ff:c000:2:11:3002:4/112",
    routing_v6=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=3500,
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
        addr="10.14.39.229",
        username="localuser",
        password="1user")
)

_gnb_instance_id = 2173
_gnb_global_bts_id = 22380

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
    addr="root@fct-4a:~",
    hardware_type="ABIO",
    hardware_version="B.101",
    serial_number="L1223901074",
    product_code="475266B.101",
    # slot_id=SlotId.B5
    )

gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="B.101",
    serial_number="L1223901059",
    product_code="475266B.101",
    # slot_id=SlotId.B4
    )

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1200900061",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

gnb_radio_unit_0 = RU(
     ru_hw_group="AZHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="root",
        password="umniedziala"),
     radio_type="AZHA",
     serial_number="6Q190128953",
     product_code="473941A.101",
)

gnb_radio_unit_1 = RU(
     ru_hw_group="AZQO",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ="),
     radio_type="AZQO",
     serial_number="1M203917126",
     product_code="475288A.102",
)

_airscale_gnb = Airscale(
    common_units=[gnb_common_unit_0],
    product_code="473098A"
    )

_du_gnb = DU(
    airscale=_airscale_gnb, 
    rus=[gnb_radio_unit_0, gnb_radio_unit_1],
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
    v4="10.14.48.173/23",
    routing_v4=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=1000,
) 

_enb_f1m_ip = NetworkAddress(
    v4="10.14.48.173/23",
    routing_v4=RoutingInformation(gateway="10.14.49.254", destIpAddr="0.0.0.0"),
    vlan_id=1000,
) 

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.39.229",
        username="localuser",
        password="10c@1user")
)

_enb_instance_id = 2173
_enb_global_bts_id = 22379

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIO",
    hardware_version="B.101",
    serial_number="L1223901059",
    product_code="475266B.101",
    # slot_id=SlotId.B4
    )

enb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="B.101",
    serial_number="L1223901074",
    product_code="475266B.101",
    # slot_id=SlotId.B5
    )

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0, enb_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1200900061",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

enb_radio_unit_0 = RU(
     ru_hw_group="AZQO",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.2",
        username="root",
        password="umniedziala"),
     radio_type="AZQO",
     serial_number="1M203917126",
     product_code="475288A.102",
)

enb_radio_unit_1 = RU(
     ru_hw_group="AZHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="root",
        password="umniedziala"),
     radio_type="AZHA",
     serial_number="6Q190128953",
     product_code="473941A.101",
)

_airscale_enb = Airscale(
    common_units=[enb_common_unit_0],
    product_code="473098A"
    )

_enb = RealEnb(
    rms=[enb_radio_unit_0, enb_radio_unit_1],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# --- TRS addition ---

switchdict_ptp_1 = {
        'TorSwitch_type':'TPS',
        'TorSwitch_addr':'10.5.117.101',
        'TorSwitch_login':'admin',
        'TorSwitch_passwd':'Admin@TPS24',
        'TorSwitch_port':'port10',
        }

switchdict_synce_1 = {
        'TorSwitch_type':'TPS',
        'TorSwitch_addr':'10.5.117.101',
        'TorSwitch_login':'admin',
        'TorSwitch_passwd':'Admin@TPS24',
        'TorSwitch_port':'1/3/C9',
        }

switchdict_ptp = {
        '5G':switchdict_ptp_1,
        '4G':switchdict_ptp_1
        }

switchdict_synce = {
        '5G':switchdict_synce_1,
        '4G':switchdict_synce_1
        }

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIB_ABIO_ABIO_AZHA_AZQO",
)

__all__ = ["tl"]

tl.tl_ptp = switchdict_ptp
tl.tl_synce = switchdict_synce
