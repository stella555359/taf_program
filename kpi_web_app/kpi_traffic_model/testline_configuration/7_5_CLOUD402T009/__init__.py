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
from taf.config.testline.pdu import HBTE
from taf.config.testline.ue import Prisma
from taf.config.testline.ue import TM500
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb
from taf.config.testline.nms import Netact

__maintainer__ = "Weng Hongyang"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com"

## common
__all__ = ["tl"]
# __all__ = ['tl']

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.109", username="ute", password="ute "
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="192.168.129.211",
    mcc="311",
    mnc="489",
    tac="61",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.240.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

##Cobham
# _tm500 = TM500(
#     tma_host=SshServiceDetails(addr='10.57.249.59', username='TL3', password='nokia123'),
#     tma_command_port='5030',
#     pdu_port=None)

##RealEnb
_real_enb_pdu = HBTE(addr="10.57.241.131", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.234.201", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.68.87.10", port_numbers=[6])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.5", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type="AEQN",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.57.241.171", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])


##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.237.94",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.237.94", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.237.94", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

_netact = Netact("10.106.161.40")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)


## parameters with new values
# Below6G
