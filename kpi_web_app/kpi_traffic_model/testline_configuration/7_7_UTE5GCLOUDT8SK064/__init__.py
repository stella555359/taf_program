__maintainer__ = "MN RAN Pz KRK 2 SG"
__team__ = "MN RAN Pz KRK 2 SG"
__email__ = "I_SC_KRK_PROD_3XV_SG@internal.nsn.com"


from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN, HPE
from taf.config.testline.pdu import FPFH

# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-CLOUDT8SK064.p08.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_oam_backhaul_ip = NetworkAddress(v4="10.84.160.3")
_gnb_instance_id = 78160
_gnb_global_bts_id = 78160

_gnb_pdu = FPFH(
    port_numbers=[5],
    addr="FPFH-ZM03-29-P08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru0_ip = NetworkAddress(v4="172.16.10.49")
_gnb_ru1_ip = NetworkAddress(v4="172.16.10.113")
_gnb_ru2_ip = NetworkAddress(v4="172.16.10.177")
_gnb_ru_hw_group = "AWEUA"

_gnb_oam_ip = NetworkAddress(
    v4="10.84.160.3",
    vlan_id=507,
)

_gnb_x2c = NetworkAddress(
    v4="10.84.154.60",
    vlan_id=504,
)

_gnb_x2u = NetworkAddress(
    v4="10.255.28.60",
    vlan_id=505,
)

_gnb_s1u = NetworkAddress(
    v4="10.255.30.60",
    vlan_id=506,
)


# eNB deleted from configuration because it's fzp
# VM address: 7-7-UTE5GCLOUDT1SK009.p01.ska-lab.nsn-rdnet.net
# eNB backhaul: 10.84.164.9

##############################################################

# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)
##############################################################


# Important!: check and change below if other than default #

# Test PCs
_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_backhaul_ip,
    x2c=_gnb_x2c,
    x2u=_gnb_x2u,
    s1u=_gnb_s1u,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)

_cu_gnb.sync = NetworkAddress(v6="", v4="10.84.160.3", vlan_id=100)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIL", hardware_version=""  # fsp1_c
)
_abil_slave_gnb = CapacityUnit(
    addr="192.168.253.26", hardware_type="ABIL", hardware_version=""  # fsp2_c
)
_abil_loner_gnb = CapacityUnit(
    addr="192.168.253.30", hardware_type="ABIL", hardware_version=""  # fsp3_c
)

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb, _abil_slave_gnb, _abil_loner_gnb],
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=5),
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)

_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_ru_0_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru0_ip.v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=HPE(
            addr="zm03.mgt.ska-lab.nsn-rdnet.net",
            port_numbers=[20],
            snmp_user=_snmp_user,
        ),
        port_no=20,
    ),
)

_ru_1_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru1_ip.v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=HPE(
            addr="zm03.mgt.ska-lab.nsn-rdnet.net",
            port_numbers=[19],
            snmp_user=_snmp_user,
        ),
        port_no=19,
    ),
)

_ru_2_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru2_ip.v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=HPE(
            addr="zm03.mgt.ska-lab.nsn-rdnet.net",
            port_numbers=[18],
            snmp_user=_snmp_user,
        ),
        port_no=18,
    ),
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_0_gnb, _ru_1_gnb, _ru_2_gnb])

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

##############################################################


# Testline

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="test",
)

__all__ = ["tl"]
