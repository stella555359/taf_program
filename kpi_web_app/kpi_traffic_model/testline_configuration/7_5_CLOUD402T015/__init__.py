import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

__maintainer__ = "Haibao Wang"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com"

__all__ = ["tl"]

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.246.3", username="root", password="uteadmin"
    )
)

_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.240.211", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/latest/",
    cfg_filename="eNB_WMP_new.cfg",
)

_ru1_pdu = FACOM(addr="1.1.1.1", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="AEQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[1],
)

_ru2_pdu = FACOM(addr="2.2.2.2", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="FRIJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru2_pdu.pdu_ports[1],
)

_lmp_connection = SshServiceDetails(
    addr="10.57.246.18", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="3.3.3.3", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2])

_cu = CU(
    backhaul_site_oam_ip="10.57.246.18",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.246.18", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.246.18", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

##RealEnb
_real_enb_pdu = FACOM(addr="4.4.4.4", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.243.243", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

_tl_cloud_topology = "CLASSICAL_5G"

_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.246.89",
        username="5G",
        password="5g",
    ),
    tma_command_port=5030,
    pdu_port=None,
)

tl = TestLine(
    test_pc=_host,
    core=_epc_sim,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_tm500],
    tl_cloud_topology=_tl_cloud_topology,
)
