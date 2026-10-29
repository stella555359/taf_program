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
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid

__maintainer__ = "Lingxue Cui"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com>"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.42", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# AppServer info
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.57.191.194",
    user="vrf3_sg1",
    password="vrf3@sg1",
    ports=[41646, 41647],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    interface_name="rmnet_data0",
    bind_ue_ip="172.252.65.139",
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="wustatic", apnName="wustatic", apnType=["DEFAULT"]
)

# UE info
_android_1 = TafUeAndroid(
    serial_number="RFCW11V5LGD",
    capabilities=["REAL_UE","samsung_ue"],
    ue_pc_address="10.57.150.74",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.74", username="mn5gran", password="nokia123@"
    ),
    ue_pc_port="80",
    imei="350932551406465",
    imsi="262033100015387",
    pdns=[_pdn1],
    service_call_attach="17",
    service_call_detach="17",
    proxy_mngr_port="9955",
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.57.239.4",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[5, 6, 7, 8],
)

# 5GRU------------------------------------
_rmod_1_pdu = HBTE(addr="10.57.241.138", port_numbers=[5])
_rmod_2_pdu = HBTE(addr="10.57.241.138", port_numbers=[8])

_rmod_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="),
    pdu_port=_rmod_1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWMFIA,
    serial_number="YK234700036",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_rmod_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="rfsw", password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="rfsw",
                                     password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA="),
    pdu_port=_rmod_2_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWMFIA,
    serial_number="YK234500060",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.57.225.6", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="1.1.1.1", port_numbers=[1])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_rmod_1, _rmod_2], f1_m_ip_addr="10.57.225.6")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.57.225.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.6", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2123, global_bts_id=37162)

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
_n2_address = NetworkAddress(v4="10.110.133.68")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=_real_4g_core_details,
    five_g=_real_5g_core_details,
    mcc="262",
    mnc="3",
    pdn=None,
)

_lte_real_enb = RealEnb(
    airscale=_airscale, rms=[_rmod_1], instance_id=2123, global_bts_id=11165
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_android_1],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    core=_realcore,
    attenuator=[_attenuator],
)
