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
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress
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
    "I_NSB_MN_RAN_RD_VRF_HAZ3_01@internal.nsn.com"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.175", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# AppServer info
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.194", username="vrf3_sg1", password="vrf3@sg1", port="41652"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="iperf",
    port="41652",
)

_appserver = AppServer(_iperf_details_on_appserver)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="wustatic", apnName="wustatic", apnType=["DEFAULT"]
)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="/cygdrive/c/iperf",
    port="41653",
)
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.170", username="mn5gran", password="nokia123@"
    ),
    serial_number="fa605f2f",
    imsi="262033100024116",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/MN5GRAN/AppData/Local/Programs/Python/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# _attenuator = ATTEN_HBTE(
#     ip_addr="1.1.1.1",
#     port=5000,
#     model="PA-16-16-6-127-0.5-B-S",
#     attenuation_port_numbers=[1, 2, 3, 4],
# )

# 5GRU------------------------------------
_rmod_pdu = HBTE(addr="1.1.1.1", port_numbers=[1, 2, 3, 4, 5, 6])

_awhhj_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="),
    pdu_port=_rmod_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHHJ,
    serial_number="1M243806971",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    #     _attenuator.attenuator_ports[3],
    #     _attenuator.attenuator_ports[4],
    # ],
)

_awhhj_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="),
    pdu_port=_rmod_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHHJ,
    serial_number="1M243403492",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    #     _attenuator.attenuator_ports[3],
    #     _attenuator.attenuator_ports[4],
    # ],
)

_awhhj_3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="),
    pdu_port=_rmod_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHHJ,
    serial_number="1M250310864",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    #     _attenuator.attenuator_ports[3],
    #     _attenuator.attenuator_ports[4],
    # ],
)

_awhhj_4 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="),
    pdu_port=_rmod_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWMFIA,
    serial_number="1M243806998",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    #     _attenuator.attenuator_ports[3],
    #     _attenuator.attenuator_ports[4],
    # ],
)

_awhhj_5 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="),
    pdu_port=_rmod_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWMFIA,
    serial_number="1M243806956",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    #     _attenuator.attenuator_ports[3],
    #     _attenuator.attenuator_ports[4],
    # ],
)

_awhhj_6 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="serviceuser",
                                     password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="),
    pdu_port=_rmod_pdu.pdu_ports[6],
    radio_type=RadioTypes.AWMFIA,
    serial_number="1M243403491",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    #     _attenuator.attenuator_ports[3],
    #     _attenuator.attenuator_ports[4],
    # ],
)

# #DU
_gnb_mplane_ip_addr = "10.101.51.197"

_lmp_connection = SshServiceDetails(
    addr=_gnb_mplane_ip_addr, username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.45.240", port_numbers=[7])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_awhhj_1, _awhhj_2, _awhhj_3, _awhhj_4, _awhhj_5, _awhhj_6],
         f1_m_ip_addr=_gnb_mplane_ip_addr)

# CU
_cu = CU(
    backhaul_site_oam_ip=_gnb_mplane_ip_addr,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_gnb_mplane_ip_addr, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_gnb_mplane_ip_addr, username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2126, global_bts_id=37731)

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


tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    ues=[_android_1],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    appserver=_appserver
    # attenuator=[_attenuator],
)
