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
from taf.config.testline.ue import Prisma
from taf.config.testline.ue import TM500
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb
from taf.config.testline.nms import Netact

__maintainer__ = "Hongyan Yuan"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com"

## common
__all__ = ["tl"]
# __all__ = ['tl']

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.102", username="ute", password="ute "
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="192.168.129.211",
    mcc="440",
    mnc="10",
    tac="61",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.248.151", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# # #Prisma
# _airmosaic_ssh = SshServiceDetails(addr='10.57.234.94', username='nokia', password='nokia123')
# _airmosaic_harness = HttpConnectionDetails(addr='10.57.234.94', port=8090)
# _lsu_uu_ssh = SshServiceDetails(addr='10.57.234.91', username='user', password='user')
# _tstm_uu_ssh = SshServiceDetails(addr='10.57.234.91', username='user', password='user')
#
#
# _prisma = Prisma(airmosaic_ssh_connection_details=_airmosaic_ssh,
#                     airmosaic_harness_connection_details=_airmosaic_harness,
#                     lsu_uu_ssh_connection_details=_lsu_uu_ssh,
#                     tstm_uu_ssh_connection_details=_tstm_uu_ssh
#                     )
#
# RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.114", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.89.37", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.68.87.116", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[1],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.89.36", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = FACOM(addr="10.68.87.114", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])


##CU
_cu = CU(
    backhaul_site_oam_ip="10.68.89.36",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.36", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1900, global_bts_id=1)

_netact = Netact("10.107.178.212")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    # ues=[_prisma],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)

PARAMS_TO_MODIFY_TL = [
    dict(
        value="10.68.89.36",
        dist_name="MRBTS-1969/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="27",
        dist_name="MRBTS-1969/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.68.89.33",
        dist_name="MRBTS-1969/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        p_name="gateway",
    ),
]

## parameters with new values
