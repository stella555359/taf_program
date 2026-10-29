import os
import yaml
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
    IperfDataTransferDetails,
)
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE, TopYoung
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.appserver import AppServer

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
#from taf.config.testline.attenuator import TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
#from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdu import ATEN
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.testpc import Connection


__maintainer__ = "Anne Ying"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ4_12@internal.nsn.com"
__email__ = "anne.ying@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
#_host = TestPc(
#_gnb_testpc = TestPc(    
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.70.230.138", username="ute", password="ute"
#    ),
#    connections=[Connection(interface="eth1", device=_classical_bts.dus[0].airscale.common_units[0], interface_type="lmp")],
#)

# _app_server_1 = TafUeAppServer(
#     app_server_name="41606",
#     address="10.57.208.28",#traffic server IP
#     user="ute",
#     password="ute",
#     bind_interface_ip="10.57.208.28",#traffic server IP
#     expected_prompt="ute.*\$ ",
#     ports=[41606, 41607]
# )

# _app_server_1 = TafUeAppServer(
# app_server_name="APP_SERVER_1",
# address="10.57.162.5",
# user="vrf3_sg8",
# password="vrf3@8",
# bind_interface_ip="10.57.162.5",
# expected_prompt="\[vrf3_sg8.*\$ ",
# ports=[58000, 58001]
# )

_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.179.230",
    user="vrf4_sg13",
    password="vrf4@sg13",
    bind_interface_ip="10.57.179.230",
    expected_prompt="\\[vrf4_sg13.*\\$ ",
    ports=[33802, 33801]
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    # binary_path="/usr/bin/",
    interface_name="dxdata4",
    version=2,
    dt_from_uepc=False,
)

_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_data_transfer_ftp = TafUeDataTransferProtocol(
    protocol_name="ftp", app_server=_app_server_1, interval=1
)


_android1 = TafUeAndroid(
    serial_number="b2fdc387",  # import,check by "adb ls"
    # capabilities=['REAL_UE', "samsung_ue"],
    capabilities=["qualcomm"],
    ue_pc_address="10.64.57.57",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    phone_number="+8613032996485",
    ue_pc_port="8080",
    imei="004403160404507",
    imsi="262033032996485",
    qualcomm_prototype=True,
    # service_call_attach='17',
    # service_call_detach='17',
)

# Attenuator
#_attenuator = HBTE(
#    addr="10.64.56.98",
#    port=23,
#    attenuation_port_numbers=[5, 6, 7, 8],
#    model="TAS16T16-51-120-1N-DES",
#)

# RealEnb---------------------------------------------------------
# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ
#_ru1_pdu = HBTE(addr="10.64.49.18", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
#_ru1_pdu = HBTE(addr="10.64.49.16", port_numbers=[1])
#_ru2_pdu = HBTE(addr="10.64.49.18", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
#_ru2_pdu = HBTE(addr="10.64.49.16", port_numbers=[2])
_ru1_pdu = TopYoung(addr="10.64.49.16", port_numbers=[1])
_ru2_pdu = TopYoung(addr="10.64.49.16", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk="),
    pdu_port=_ru1_pdu.pdu_ports[1],

    radio_type=RadioTypes.AHFIB.value,   
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.102.1",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.0.4",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="),
    pdu_port=_ru2_pdu.pdu_ports[2],

    radio_type=RadioTypes.AEQV.value,   
)


# #DU
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"  # mplane IP
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP",rus=[_ru1,_ru2])

#_gnb_pdu = HBTE(addr="10.64.49.28", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_gnb_pdu = HBTE(addr="10.64.49.28", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1,_ru2],
         f1_m_ip_addr="10.64.54.69")  # mplane IP

# CU
_cu = CU(
    backhaul_site_oam_ip="10.64.54.69",  # mplane IP
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.69", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.69", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(
    dus=[_du],
    cu=_cu,
    instance_id=37324,
    global_bts_id=37324)

# host
#_host = TestPc(
_gnb_testpc = TestPc(    
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.21", username="ute", password="uteUTE!"
    ),
    connections=[Connection(interface="eth1", device=_classical_bts.dus[0].airscale.common_units[0], interface_type="lmp")],
)
_qc_host_ssh = SshServiceDetails(
    addr="10.64.57.57", username="mn5gran", password="nokia123@"
)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASIML_ABIPB1_AEQV_AHFIB"

tl = TestLine(
    test_pc=_gnb_testpc,
    gnbs=[_classical_bts],
    ues=[_android1],
    tl_cloud_topology=_tl_cloud_topology,
    # appserver=_appserver,
    #attenuator=_attenuator,
)


if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
