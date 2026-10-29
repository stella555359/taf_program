__maintainer__ = "Yang Zehong"
__team__ = "I_MN_5GSC_SW_ENG_1_CN_09_SG_GMS"
__email__ = "zehong.yang@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.appserver import AppServer
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Airphone, Prisma, TM500, Qualcomm
from taf.config.testline.pdu import FACOM
from taf.config.testline import DU
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.testline import TestLine


_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.130.194", username="nokia5G", password="noki@123"
    )
)

_lte = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.152.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.152.228", username="Nemuadmin", password="nemuuser"
    ),
)  # tl.core.default_ssh_connection_details.addr

_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.152.228", username="Nemuadmin", password="nemuuser"
    ),
    dir_path="/opt/iphy/latest/",
    cfg_filename="",
)

_appserver = AppServer(
    iperf_details=SshServiceDetails(addr="10.57.205.26", username="ute", password="ute")
)  # tl.appserver.iperf_details.password

_lmp_connection = SshServiceDetails(
    addr="10.57.152.244", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.251.231", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale)

_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.152.244", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.152.244", username="Nemuadmin", password="nemuuser"
    ),
)

_qualcomm = Qualcomm(
    serial_number="eea5f71d",
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.194", username="nokia5G", password="noki@123"
    ),
    com_port="smd11",
    qxdm_version="",
    ue_type="",
    heartbeat_port="",
    server_command_input_port="",
    server_qxdm_messages_port="",
    server_command_output_port="",
    message_stream_port="",
)  # tl.ues.ssh_connection_details.password

_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKA101_ABILA102_19A"

tl = TestLine(
    test_pc=_host,
    core=_lte,
    ues=[_qualcomm],
    gnbs=[_classical_bts],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)


#########DCAP###########
DCAP_IP = "10.57.208.11"
DCAP_USER = "dcapuser"
DCAP_PASSWD = "dcapuser123"
__all__ = ["tl"]
