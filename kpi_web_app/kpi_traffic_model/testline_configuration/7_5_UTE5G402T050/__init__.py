import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)

__maintainer__ = "Cui Lingxue"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.171", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# #DU
_lmp_connection = SshServiceDetails(
    addr="10.71.210.2", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, f1_m_ip_addr="10.71.210.2")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.210.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.2", username="Nemuadmin", password="nemuuser"
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10155, global_bts_id=10155)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1)
_mme = MME(oam_ssh_connection_details=_mme_oam_ssh_connection_details, s1=_s1_address)
_real_4g_core_details = RealCore4GDetails(mme=_mme)

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.110.66.198")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=_real_4g_core_details,
    five_g=_real_5g_core_details,
    mcc="310",
    mnc="260",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    core=_realcore,
)
