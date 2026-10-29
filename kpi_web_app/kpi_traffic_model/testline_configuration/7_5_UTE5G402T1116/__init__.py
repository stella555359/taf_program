import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Airphone, Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.attenuator import HBTE
from taf.config.testline.appserver import AppServer

__maintainer__ = "LU Ming"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "ming.lu@nokia-sbell.com"

## common
__all__ = ["tl"]

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.27", username="ute", password="iW_K#8.ute%A10h0m0ra"
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


# 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[1],
)

# RealEnb
_real_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)


##5GRU for classicalBTS
_ru_pdu = PBHBTE(addr="10.101.45.6", port_numbers=[6])
_ru2_pdu = PBHBTE(addr="10.101.45.5", port_numbers=[4])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type="AHCA",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.2.3.4", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.2.3.4", username="user", password="pass"),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type="AHFB",
)


_attenuator_RU1 = HBTE(
    ip_addr="10.101.48.209",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_RU2 = HBTE(
    ip_addr="10.101.48.207",
    port=5000,
    attenuation_port_numbers=[5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.48.196", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = PBHBTE(addr="10.101.45.6", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru, _ru2], f1_m_ip_addr="192.168.255.129")


##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.48.196",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.196", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10037", global_bts_id="10037"
)


# UE-MTK
_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34",
    username="cmw_sg1",
    password="Noki_sg1@123!",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=51000,
)

_appserver = AppServer(_iperf_details_on_appserver)
_mtk_host_ssh = SshServiceDetails(
    addr="10.101.47.32", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=51000,
)


# CI_Detail_UE_Type='MTK'
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    # imei="887233895987381",
    #    imsi="460028001006223",
    imei="887239672658343",
    imsi="460023100008483",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_mtk],
    tl_cloud_topology=_tl_cloud_topology,
    attenuators=[_attenuator_RU1, _attenuator_RU2],
    # attenuator=_attenuator_RU2,
    appserver=_appserver,
)
