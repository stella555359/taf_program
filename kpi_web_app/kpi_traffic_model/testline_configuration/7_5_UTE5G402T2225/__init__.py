import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import TopYoung as PBTopYoung
from taf.config.testline.pdu import FPFH
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer


__maintainer__ = "Liu Geng"
__team__ = "RAN VRF HAZ4 T01"
__email__ = "geng.liu@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.59", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb_1
_ru_enb_1_pdu = PBHBTE(addr="10.68.87.18", port_numbers=[5])
_ru_enb_1 = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_1_pdu.pdu_ports[5],
)


# #RealEnb_1
_real_enb_1_pdu = PBHBTE(addr="10.68.87.21", port_numbers=[6])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_1_pdu.pdu_ports[6],
)
_real_enb_1 = Airscale(common_units=[_common_unit_2])
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=_ru_enb_1)



##5GRU for classicalBTS
_ru_1_pdu = PBHBTE(addr="10.101.45.3", port_numbers=[3])



_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type="AVHA",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = PBTopYoung(addr="10.101.45.2", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru_1,
    ],
    f1_m_ip_addr="10.101.48.216",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.48.216",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.216", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.216", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"
# classicalbts
# _classical_bts = ClassicalBts(dus=[_du], cu=_cu)
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="37590", global_bts_id="37590"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.57.130.109", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki@123"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=10000,
)



tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
