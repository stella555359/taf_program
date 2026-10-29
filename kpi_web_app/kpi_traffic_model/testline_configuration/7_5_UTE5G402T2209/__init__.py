import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

# from taf.config.testline.attenuator import HBTE
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

__maintainer__ = "Kong Xiangli"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "xiangli.kong@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.9", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="200",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_12341"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

## 4GRU for RealEnb
# _ru_enb_pdu = TopYoung(addr="10.101.45.85", port_numbers=[4])
#
# _ru_enb = RadioModule(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="usr", password="psswd"
#    ),
#    pdu_port=_ru_enb_pdu.pdu_ports[4],
# )
#
## #RealEnb
# _real_enb_pdu = TopYoung(addr="10.101.45.86", port_numbers=[4])
#
#
# _common_unit_2 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.101.49.235", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
#    pdu_port=_real_enb_pdu.pdu_ports[4],
# )
#
# _real_enb = Airscale(common_units=[_common_unit_2])
#
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.71.197.57", port_numbers=[8])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[8],
    radio_type="AWPQZ",
)

_ru_2_pdu = HBTE(addr="10.71.197.49", port_numbers=[8])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[8],
    radio_type="AWPQZ",
)

_ru_3_pdu = TopYoung(addr="10.71.197.59", port_numbers=[4])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[4],
    radio_type="AHFB",
)

_ru_4_pdu = HBTE(addr="10.71.197.49", port_numbers=[6])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_4_pdu.pdu_ports[6],
    radio_type="AWHQX",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = TopYoung(addr="10.71.197.59", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4],
    f1_m_ip_addr="10.71.215.108",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.215.108",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.108", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.108", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11119", global_bts_id="11119"
)


# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki_sg1@123!", port="51100"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="/usr/bin/iperf",
    port="52204",
)

_appserver = AppServer(_iperf_details_on_appserver)
# CI_Detail_UE_Type='MTK'
_ue_host_ssh = SshServiceDetails(
    addr="10.71.218.206", username="nokia5G", password="noki@123"
)

_iperf_details_on_MTK = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="10.71.218.206",
    iperf_path="/data/local/tmp/iperf",
    port="52209",
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="460023100010662",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_MTK,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    # enbs=[_lte_real_enb],
    ues=[_mtk],
    # ues=[_fastmile_1, _fastmile_2],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
