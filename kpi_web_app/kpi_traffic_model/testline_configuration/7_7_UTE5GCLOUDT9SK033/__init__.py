__maintainer__ = "Barbara Wozniak"
__team__ = "5G_PZ_MMW_KRK_2_SG"
__email__ = "barbara.wozniak@nokia.com"

from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails
)
from taf.config.testline.testline import TestLine
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import NMS, NetAct
from taf.config.testline.enb import (
    NetworkAddress,
    RealEnb,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RUExtension, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN



_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(                            # the information of the SSH connection to the VM
    addr="7-7-UTE5GCLOUDT9SK033.p09.ska-lab.nsn-rdnet.net",                                 # should be set to the DNS address
    username="ute",
    password="ute",
)
_gnb_oam_ip = NetworkAddress(
    v4="10.84.140.33",
)
_gnb_instance_id = 78333
_gnb_global_bts_id = 78333
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.49")
_gnb_ru_hw_group = "AWEUA"
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
_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    x2u=_gnb_oam_ip,
    s1u=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)  # replace if other than default
_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details
_abil_master_gnb = CapacityUnit(addr="fsp1_c")  # 192.168.253.20
_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)
_ru_ext0 = RUExtension(
    radio_type="FA3UA", serial_number="YK202100166", product_code="475001A.101"
)
_ru_ext1 = RUExtension(
    radio_type="FA3UA", serial_number="202100152", product_code="475001A.101"
)
_ru_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(pdu=ATEN(addr="10.255.10.152", port_numbers=[8]), port_no=8),          # contact the TL owner or lab service to retrieve information
    ru_extensions=[_ru_ext0, _ru_ext1],
)
_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])
_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_gnb])
_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)


_nms = NMS(
    netact=NetAct(
        ssh_connections_info=SshServiceDetails(
            addr="10.43.48.76",
            username="omc",
            password="Medsql!_1893",
        ),
        https_main_info=HttpConnectionDetails(
            addr="srnclab1044lbwas.srnblr.nsn-rdnet.net",
        ),
    ),
)

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    nms=_nms
)

tl = TestlineWrapper(tl)

__all__ = ["tl"]
