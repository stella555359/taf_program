import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE, FPFH
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim
from taf.config.testline import RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

__maintainer__ = "Frank Luo"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "frank.s.luo@nokia-sbell.com"
## common
__all__ = ["tl"]
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.58", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host_secondary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.221.135", username="haijtest", password="Nokia@12345"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.68.87.18", port_numbers=[6])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[6],
    radio_type="AHFII",
)

_ru_2_pdu = HBTE(addr="10.68.87.8", port_numbers=[6])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[6],
    radio_type="AHFII",
)

_ru_3_pdu = FPFH(addr="10.68.87.28", port_numbers=[2], login="admin", password="admin")
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type="AHFII",
)

_ru_4_pdu = HBTE(addr="10.68.87.10", port_numbers=[3])
_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_4_pdu.pdu_ports[3],
    radio_type="AHLOB",
)

_ru_5_pdu = HBTE(addr="10.68.87.10", port_numbers=[4])
_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_5_pdu.pdu_ports[4],
    radio_type="AHLOB",
)

_ru_6_pdu = FPFH(addr="10.68.87.30", port_numbers=[5], login="admin", password="admin")
_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_6_pdu.pdu_ports[5],
    radio_type="AVHA",
)

_ru_7_pdu = HBTE(addr="10.68.87.10", port_numbers=[5])
_ru_7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_7_pdu.pdu_ports[5],
    radio_type="AVHA",
)

_ru_8_pdu = HBTE(addr="10.68.87.8", port_numbers=[4])
_ru_8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_8_pdu.pdu_ports[4],
    radio_type="AVHA",
)

##DU for classicalBTS
_gnb_1_airscale_cu_lmp_left = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_gnb_1_airscale_cu_lmp_right = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_BBMOD_left_1 = CapacityUnit(addr="1.1.1.1", rus=[_ru_1])
_gnb_1_airscale_BBMOD_right_1 = CapacityUnit(addr="1.1.1.1", rus=[_ru_2])

_gnb_1_pdu_left = HBTE(addr="10.68.87.29", port_numbers=[3])
_gnb_1_pdu_right = HBTE(addr="10.68.87.13", port_numbers=[8])

_gnb_1_airscale_cu_left = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_left,
    capacity_units=[
        _gnb_1_airscale_BBMOD_left_1,
    ],
    pdu_port=_gnb_1_pdu_left.pdu_ports[3],
)

_gnb_1_airscale_cu_right = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_right,
    capacity_units=[_gnb_1_airscale_BBMOD_right_1],
    pdu_port=_gnb_1_pdu_right.pdu_ports[8],
)

_airscale = Airscale(common_units=[_gnb_1_airscale_cu_left, _gnb_1_airscale_cu_right])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8], f1_m_ip_addr="10.101.36.2")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.36.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.36.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.36.2", username="Nemuadmin", password="nemuuser"
    ),
)
##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="430", global_bts_id="430"
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, _host_secondary_core],
    gnbs=[_classical_bts],
    core=_epc_sim,
    tl_cloud_topology=_tl_cloud_topology,
)
