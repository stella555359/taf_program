# This is for WMP + Classical GNB
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
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper


__maintainer__ = "Ren Biyao"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "binmei.ding@nokia-sbell.com"

# common
__all__ = ["tl"]

# SCF related configuration. Keep this part in this file temporary, will
# remove it when go to UTE
PARAMS_TO_MODIFY_SCF = [
    dict(value="HZ TL048 Classical", dist_name="MRBTS-1900", p_name="btsName"),
    dict(
        value="10.1.1.1",
        dist_name="MRBTS-1900/NRBTS-1/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="5G18A/5g_pid12_classical_eoc",
        dist_name="MRBTS-1900/EQM-1/APEQM-1",
        p_name="rapProfile",
    ),
    dict(
        value="10.2.2.1",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.4",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.5",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.5",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpPrefixLength",
    ),
    # This is used for ssh to ASIK
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),
    dict(
        value="true",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SECADM-1",
        p_name="actServiceAccountSsh",
    ),
]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.57.157.50",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10300,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="eNB_WMP_TL048_new.cfg",
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.57.241.168", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU------------------------------------
_ru_pdu = FACOM(addr="10.57.243.7", port_numbers=[2])

_ru = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type="AEQA",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.57.229.36", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.241.168", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])

# CU
_cu = CU(
    backhaul_site_oam_ip="10.57.229.36",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.229.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.229.36", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# UE part--------------------------------------------------------
_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.161.30",
        username="tester",
        password="nokia123",
        private_key="CNHZ5GRAN1070",
    ),
    tma_command_port=5030,
    pdu_port=None,
)

tl = TestLine(
    test_pc=_host,
    core=_epc_sim,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    ues=[_tm500],
    tl_cloud_topology=_tl_cloud_topology,
)
# old version keyword under robotws5g/resource compatibility workaround
tl = TestlineWrapper(tl)
