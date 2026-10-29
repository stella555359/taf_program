__maintainer__ = "Kamil Bielecki"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "kamil.bielecki@nokia.com"

import os

import yaml
from taf.config.testline import NetworkAddress, RU, RUExtension, RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.radio import RadioTypes
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.pdu import PduPort, HPE, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.lmi import SerialOverHost, Local


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


# Test PCs configuration (VMs)
_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK050.p08.ska-lab.nsn-rdnet.net", username="ute", password="uteUTE!"
)

_test_pc_gnb_2_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT8SK050-2.p08.ska-lab.nsn-rdnet.net", username="ute", password="UTE.debian12"
)

# gNBs configuration
_gnb_1_bc_ip = NetworkAddress(v4="10.84.152.50/23")

_gnb_2_bc_ip = NetworkAddress(v4="10.84.152.225/23")

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_ssh_lmp_connection_gnb2 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_ssh_connection_gnb1 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_ssh_connection_gnb2 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_ssh_lmp_connection_enb = SshServiceDetails(
    addr="10.84.152.45",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr="10.84.152.50", username="Nemuadmin", password="nemuuser", port=443
)

_default_gnb_2_oam_http_connection = HttpConnectionDetails(
    addr="10.84.152.225", username="Nemuadmin", password="nemuuser", port=443
)

# CU
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_bc_ip,
    oam_ssh_connection_details=_default_ssh_connection_gnb1,
    oam_http_connection_details=_default_gnb_1_oam_http_connection,
)

_cu_gnb_2 = CU(
    backhaul_site_oam_ip=_gnb_2_bc_ip,
    oam_ssh_connection_details=_default_ssh_connection_gnb2,
    oam_http_connection_details=_default_gnb_2_oam_http_connection,
)
# DUs
_du_lmp_connection_gnb_1 = _default_ssh_lmp_connection
_du_lmp_connection_gnb_1.proxy = _test_pc_gnb_1_default_ssh_connection_details

_du_lmp_connection_gnb_2 = _default_ssh_lmp_connection_gnb2
_du_lmp_connection_gnb_2.proxy = _test_pc_gnb_2_default_ssh_connection_details

_du_lmp_connection_enb_1 = _default_ssh_lmp_connection_enb
_du_lmp_connection_enb_1.proxy = _test_pc_gnb_1_default_ssh_connection_details

_asil_master_gnb = CapacityUnit(addr="fsp1_c",
                                hardware_type="ABIO")

_asil_master_enb = CapacityUnit(addr="root@fct-0a:~",
                                hardware_type="ABIA")

_snmp_user = {
    "userName": "user-lab0",
    "authKey": "NokiaBts2003",
    "privKey": "NokiaBts2003",
    "authProtocol": "MD5",
    "privProtocol": "AES",
}

_gnb_pdu = FPFH(
    port_numbers=[2],
    addr="fpfh-zg07-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_pdu_2 = FPFH(
    port_numbers=[1],
    addr="fpfh-zg07-28-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_enb_pdu = FPFH(
    port_numbers=[3],
    addr="fpfh-zh07-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_du_common_unit_gnb_1 = CommonUnit(
    pdu_port=_gnb_pdu.pdu_ports[2],
    lmp_connection=_du_lmp_connection_gnb_1,
    capacity_units=[_asil_master_gnb],
    hardware_type="ASIL",
    hardware_version="101",
)

_du_common_unit_gnb_2 = CommonUnit(
    pdu_port=_gnb_pdu_2.pdu_ports[1],
    lmp_connection=_du_lmp_connection_gnb_2,
    capacity_units=[],
    hardware_type="ASOE",
    hardware_version="103",
)

_du_common_unit_enb_1 = CommonUnit(
    pdu_port=_enb_pdu.pdu_ports[3],
    lmp_connection=_du_lmp_connection_enb_1,
    capacity_units=[_asil_master_enb],
    hardware_type="ASIL",
    hardware_version="101",
)

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details,
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(interface="eth1", device=_du_common_unit_gnb_1, interface_type="lmp"),
    ],
)

_pdu = HPE(
    addr="zg07.mgt.ska-lab.nsn-rdnet.net",
    port_numbers=[6],
    snmp_user=_snmp_user,
)

_ru_1 = RU(
    ru_hw_group="RF5.1",
    serial_number="AH205100740",
    radio_type=RadioTypes.AWEUC.value,
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    pdu_port=PduPort(pdu=_pdu, port_no=6),
)

_ru_2 = RU(
    ru_hw_group="RF5.1",
    serial_number="AH205100748",
    radio_type=RadioTypes.AWEUC.value,
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    pdu_port=PduPort(pdu=_pdu, port_no=6),
)

_airscale_gnb_1 = Airscale(common_units=[_du_common_unit_gnb_1])

_airscale_gnb_2 = Airscale(common_units=[_du_common_unit_gnb_2])

_airscale_enb_1 = Airscale(common_units=[_du_common_unit_enb_1])

_du_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_ru_1])

_du_gnb_2 = DU(airscale=_airscale_gnb_2, rus=[_ru_2])

_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id="79050",
    global_bts_id="79050",
)

_gnb_2 = ClassicalBts(
    cu=_cu_gnb_2,
    dus=[_du_gnb_2],
    instance_id="79225",
    global_bts_id="79225",
)

_enb = RealEnb(
    system_module=_airscale_enb_1,
    oam_ip=NetworkAddress(v4="10.84.152.45"),
    instance_id=79045,
    global_bts_id=79045,
    x2_link_addr=NetworkAddress(v4="10.84.152.45"),
)

_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_1,
    gnbs=[_gnb_1, _gnb_2],
    enbs=[_enb],
    pdus=[_pdu],
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASILL_ABIOB1_AWEUC",
)

__all__ = ["tl"]
