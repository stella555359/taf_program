# Generated with TL configuration generator at 2025-10-08_13:48:46

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
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.lmi import SerialOverTcp, Remote
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_fpfh1_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zk05-46-p11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_fpfh2_pdu = FPFH(
    port_numbers=[2, 3, 4],
    addr="fpfh-zk05-39-p11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK072.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 81072
_gnb_0_global_bts_id = 81072

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_secondary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.119",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.82.28.72/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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

_asmr_user = "serviceuser"
_asmr_pass = "tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ="
_aewb_user = "serviceuser"
_aewb_pass = "wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ="


_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_aewb_user, password=_aewb_pass
    ),
    radio_type="AEWB",
    serial_number="AH220602883",
    product_code="474609A.105",
    pdu_port=PduPort(pdu=_fpfh1_pdu, port_no=2),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AWGUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_asmr_user, password=_asmr_pass
    ),
    radio_type="AWGUD",
    serial_number="AH242500719",
    product_code="475947A.103",
    pdu_port=PduPort(pdu=_fpfh1_pdu, port_no=3),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AWGUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_asmr_user, password=_asmr_pass
    ),
    radio_type="AWGUD",
    serial_number="AH242500723",
    product_code="475947A.103",
    pdu_port=PduPort(pdu=_fpfh1_pdu, port_no=4),
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AWGUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_asmr_user, password=_asmr_pass
    ),
    radio_type="AWGUD",
    serial_number="AH242500722",
    product_code="475947A.103",
    pdu_port=PduPort(pdu=_fpfh1_pdu, port_no=5),
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AWEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_asmr_user, password=_asmr_pass
    ),
    radio_type="AWEWB",
    serial_number="AH223904624",
    product_code="475171A.103",
    pdu_port=PduPort(pdu=_fpfh2_pdu, port_no=2),
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AWEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_asmr_user, password=_asmr_pass
    ),
    radio_type="AWEWB",
    serial_number="AH223904633",
    product_code="475171A.103",
    pdu_port=PduPort(pdu=_fpfh2_pdu, port_no=3),
)
_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AWEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username=_asmr_user, password=_asmr_pass
    ),
    radio_type="AWEWB",
    serial_number="AH223904622",
    product_code="475171A.103",
    pdu_port=PduPort(pdu=_fpfh2_pdu, port_no=4),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230606002",
    product_code="475266A.105",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613315",
    product_code="475266A.105",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1214610574",
    product_code="475266A.104",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_4, _gnb_0_radio_unit_5],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1214610574",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_6],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
    ],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1223402808",
    mac_addr="60:8f:a4:b7:e9:76",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_fpfh1_pdu, port_no=1),
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_3],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1223402808",
    mac_addr="60:8f:a4:b7:e9:76",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_fpfh1_pdu, port_no=6),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0, _gnb_0_common_unit_1],
    product_code="473098A",
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
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASILL_ABIOB1B2_AEWB_SA_3xAWGUD_NSA_ASOF_AHEH",
    pdus=[_fpfh1_pdu],
)

__all__ = ["tl"]
