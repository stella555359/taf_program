import os
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer, AppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.lmi import LMI, Local

__maintainer__ = "Shifu Lan"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "shifu.lan@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# test_pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##PB info
# TOPYOUNG 6-6 DBII04 30821090021
_ru_pdu = TopYoung(addr="10.71.196.168", port_numbers=[2, 3, 5])
_ru_pdu1 = HBTE(addr="10.71.196.171", port_numbers=[2])
# HBTE 1-8 DBII02 PPB2108300010
_gnb_pdu = HBTE(addr="10.71.196.165", port_numbers=[2])

# 5GRU_1 for classicalBTS

_ru_lmi_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.218.33", username="ute", password="!Q2w3e4r5t6y7u"
    )
)

_ru_lmi_pc_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.173", username="ute", password="!Q2w3e4r5t6y7u"
    )
)

_ru_lmi_pc_3 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.218.30", username="ute", password="!Q2w3e4r5t6y7u"
    )
)

_ru_lmi1 = LMI(product_code="",
              host=_ru_lmi_pc_1,
              uart_mapping=[Local(port='/dev/ttyUSB0')])

_ru_lmi2 = LMI(product_code="",
              host=_ru_lmi_pc_2,
              uart_mapping=[Local(port='/dev/ttyUSB0')])

_ru_lmi3 = LMI(product_code="",
              host=_ru_lmi_pc_3,
              uart_mapping=[Local(port='/dev/ttyUSB0')])

##SN:1M222812815 - AKNB_RMOD4
_ru4 = RU(
    ru_hw_group="AKNB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    # lmp_connection=SshServiceDetails(
    #     addr="10.71.218.30", username="ute", password="!Q2w3e4r5t6y7u"
    # ),
    pdu_port=_ru_pdu1.pdu_ports[2],
    radio_type=RadioTypes.AKNB,
    serial_number="1M222812815",
    # lmi=_ru_lmi3
)

##SN:1M222627864 - AQQY3
_ru3 = RU(
    ru_hw_group="AQQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.30", username="ute", password="!Q2w3e4r5t6y7u"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQY,
    serial_number="1M222627864",
    lmi=_ru_lmi3
)

##SN:1M214306648 - AQQY2
_ru2 = RU(
    ru_hw_group="AQQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.173", username="ute", password="!Q2w3e4r5t6y7u"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQY,
    serial_number="DH233065584",
    lmi=_ru_lmi2
)

##5GRU_2 for classicalBTS
##SN:1M224946013 - AQQA
_ru1 = RU(
    ru_hw_group="AQQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.33", username="ute", password="!Q2w3e4r5t6y7u"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQY,
    serial_number="DH233082813",
    lmi=_ru_lmi1
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIB",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4], f1_m_ip_addr="10.71.213.106"
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.213.106",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.106", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.106", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.213.106",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.71.213.97/27"),
    ),
    x2u=NetworkAddress(
        v4="10.71.213.106",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.71.213.97/27"),
    ),
    s1u=NetworkAddress(
        v4="10.71.213.106",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.71.213.97/27"),
    ),
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL603"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870837, global_bts_id=536870837)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54702, 54602],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.159.48",
    root_password="DNQraDbi@Tk=7Mu9",
    default_user_password='6zifVkv.-eF2TWf2',
    ue_manage_ip="10.71.213.145",
    serial_number="LPL24430020D",
    data_transfer=[_fastmile_data_transfer_1],
    #ue_pc_port=9955,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-B',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_appserver_2 = TafUeAppServer(
   app_server_name='APP_SERVER_1',
   address='10.71.207.151',
   user='vrf4_sg4',
   password='vrf4@sg4',
   bind_interface_ip='10.71.207.151',
   expected_prompt='[vrf4_sg4@appserver ~]$ ',
   binary_path='/home/vrf4_sg4/taf_debug/iperf',
   ports=[54816, 54716])

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
   protocol_name='iperf',
   app_server=_fastmile_appserver_2,
   interval=1,
   binary_path='iperf',
   version=2)

_fastmile_2= TafUeFastmile(
   ue_pc_address='10.57.159.48',
   root_password='T++2zQnPDXvu+oZf',
   default_user_password='fMVcJjxLcv5oeMCi',
   ue_manage_ip='10.71.213.146',
   serial_number='LPL243600013',
   data_transfer=[_fastmile_data_transfer_2],
   #ue_pc_port=9955,
   proxy_mngr_port=9955,
   ueproxy_force_release=True,
   version='Receiver 5Gmm28-B',
   capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _fastmile_2],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
