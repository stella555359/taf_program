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
from taf.config.testline import NetAct

__maintainer__ = "STEVEN WU"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "steven.wu@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.159", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

##5GRU for classicalBTS
_ru_1_pdu = FPFH(port_numbers=[3], addr="10.68.87.28", login="admin", password="admin")
_ru_2_pdu = PBHBTE(port_numbers=[1], addr="10.68.87.23")
_ru_3_pdu = PBHBTE(port_numbers=[4], addr="10.68.87.12")


_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type="AVQQB",
)
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type="AVNB",
)
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[4],
    radio_type="AVQC",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = FPFH(port_numbers=[1], addr="10.68.87.26", login="admin", password="admin")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru_1,
		_ru_2,
        _ru_3,
    ],
    f1_m_ip_addr="10.68.88.42",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.42",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.42", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.42", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "BTS_CLASSICAL_ASIM_ABIP"
# classicalbts
# _classical_bts = ClassicalBts(dus=[_du], cu=_cu)
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="37588", global_bts_id="37588"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.112", username="mn5gran", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.191.243", username="vrf4_sg1", password="vrf4@sg1"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.243",
    iperf_path="iperf",
    port=10000,
)




# #######Netact########
_netact_ssh_han5 = SshServiceDetails('10.107.183.26', 'omc', password='Nokia123!')
_netact_http_han5 = HttpConnectionDetails('https://han5lbwas.han5.srnhz.nsn-rdnet.net/', 'omc', password='Nokia123!')
_netact_han5 = NetAct(_netact_ssh_han5, _netact_http_han5)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact_han5,
)