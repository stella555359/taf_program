__maintainer__ = "Andrzej Pencak"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "andrzej.pencak@nokia.com"

import os
import yaml
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline import NetworkAddress, RU
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, SlotId
from taf.config.testline.pdu import PduPort, ATEN, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek, Android, TafUeAndroid
from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.appserver import TafUeAppServer


_attenuator = RadioRack(
    ip_addr="10.255.27.152",
    port="50000",
    attenuation_port_numbers=[1, 2, 3, 4],
)

_gnb_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg14-26-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_pdus = [_gnb_pdu]

# gNBs configuration

_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK118-1.p08.ska-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_gnb_2_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK118-2.p08.ska-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_1_bc_ip = NetworkAddress(v4="10.84.152.118")
_gnb_2_bc_ip = NetworkAddress(v4="10.84.152.119")

_default_ssh_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1_default_ssh_connection_details,
)

_default_ssh_lmp_connection_2 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_2_default_ssh_connection_details,
)

_default_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_bc_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_default_gnb_2_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_2_bc_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

# CUs
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_bc_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection_1,
    oam_http_connection_details=_default_gnb_1_oam_http_connection,
)

_cu_gnb_2 = CU(
    backhaul_site_oam_ip=_gnb_2_bc_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection_2,
    oam_http_connection_details=_default_gnb_2_oam_http_connection,
)

_ru_gnb_1 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="asmr",
    ),
    radio_type="AEQE",
    serial_number="1M223812820",
    product_code="474750A.102",
    pdu_port=_gnb_pdu.pdu_ports[2]
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABI0",
    hardware_version="A.104",
    serial_number="L1215008561",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_ru_gnb_1],
    )

_du_common_unit_gnb_1 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection_1,
    capacity_units=[_gnb_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="102",
    pdu_port=_gnb_pdu.pdu_ports[3]
)

_ru_gnb_2 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="asmr",
    ),
    radio_type="AEQE",
    serial_number="1M223712379",
    product_code="474750A.102",
    pdu_port=_gnb_pdu.pdu_ports[1]
)

_gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203611756",
    product_code="474020B.102",
    slot_id=SlotId.B4,
    rus=[_ru_gnb_2],
    )

_du_common_unit_gnb_2 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection_2,
    capacity_units=[_gnb_capacity_unit_2],
    hardware_type="ASIL",
    hardware_version="102",
    pdu_port=_gnb_pdu.pdu_ports[4]
)


_airscale_gnb_1 = Airscale(common_units=[_du_common_unit_gnb_1])
_airscale_gnb_2 = Airscale(common_units=[_du_common_unit_gnb_2])

_du_gnb_1 = DU(airscale=_airscale_gnb_1)
_du_gnb_2 = DU(airscale=_airscale_gnb_2)


# gNBs configuration
_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id="79118",
    global_bts_id="79118",
)

_gnb_2 = ClassicalBts(
    cu=_cu_gnb_2,
    dus=[_du_gnb_2],
    instance_id="79119",
    global_bts_id="79119",
)

# AppServer
_appserver_ssh = SshServiceDetails(addr="10.84.168.120", username="5g", password="5g")
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh, #????
    network_interface_address="10.84.169.60",
    iperf_path="/usr/bin/iperf",  # no iperf3
    ports=[2123, 2124], #??????
)

_appserver = AppServer(_iperf_details_on_appserver)

# Test PCs configuration (VMs)
_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK118-1.p08.ska-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_gnb_2_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK118-2.p08.ska-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details,
)

_test_pc_gnb_2 = TestPc(
    default_ssh_connection_details=_test_pc_gnb_2_default_ssh_connection_details,
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
# # UE-PC connection
_ue23_pc_ssh = SshServiceDetails("PLKR-UEPC-ZG14A.intra.noklab.net", "noklab\pzkrk", password="NokiaBts2003")


# QC UE
_android_iperf = IperfDataTransferDetails(_appserver_ssh, '40.1.1.254', None)

_taf_appserv = TafUeAppServer(
    app_server_name="SKA-HC14-15-AppServer",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g"
)

_taf_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_taf_appserv,
    binary_path='/data/data/com.nokia.android.application/',
    interval=1,
    # interface_name='5gsakrk2/rmnet_data1',
    server_close_delay=50
)

_taf_data_transfer = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_taf_appserv,
    binary_path='/data/data/com.nokia.android.application/',
    interval=1,
    # interface_name='5gsakrk2/rmnet_data0',
    server_close_delay=50
)

#------------------------UE_SETTINGS------------------------------

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue.yaml")


# TL configuration
tl = TestLine(
    test_pc=_test_pc_gnb_1,
    gnbs=[_gnb_1, _gnb_2],
    test_pcs=[_test_pc_gnb_1, _test_pc_gnb_2],
    attenuators=[_attenuator],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_2XSAMSUNG_SA_ASILLR_ABILB1B4_2XAEQE",
    appserver=_appserver,
    pdus=_pdus
)

__all__ = ["tl"]
