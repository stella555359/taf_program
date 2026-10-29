import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek, TafUeAt

from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import TafUeAndroid

__maintainer__ = "l3gao"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "lei.4.gao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.54", username="ute", password="uteUTE!"
    )
)

_qc_host_ssh = SshServiceDetails(
    addr="10.57.150.133", username="MN5GRAN", password="nokia123@"
)


_appserver_ssh = SshServiceDetails(
     addr="10.57.191.242",
     username="vrf4_sg13",
     password="vrf4@13",
     port="33803",
 )
 
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.242",
)

_appserver = AppServer(_iperf_details_on_appserver)


_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.242",
    user="vrf4_sg13",
    password="vrf4@sg13",
    bind_interface_ip="10.57.191.242",
    expected_prompt="\\[vrf4_sg13.*\\$ ",
    ports=[33821, 33822]
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    # binary_path="/usr/bin/",
    interface_name="weistatic",
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
   serial_number="c2d07079",  # import,check by "adb ls"
   # capabilities=['REAL_UE', "samsung_ue"],
   capabilities=["qualcomm"],
   ue_pc_address="10.57.150.133",
   data_transfer=[_data_transfer_iperf,
                  _data_transfer_ping,
                  _data_transfer_ftp],
   phone_number="+8613032996485",
   ue_pc_port="8080",
   imei="004403160422855",
   imsi="262033100008225",
   qualcomm_prototype=True,
   # service_call_attach='17',
   # service_call_detach='17',
)

_android2 = TafUeAndroid(
    serial_number="2cdcf49b",  # import,check by "adb ls"
    # capabilities=['REAL_UE', "samsung_ue"],
    capabilities=["qualcomm"],
    ue_pc_address="10.57.150.133",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    phone_number="+8613032996485",
    ue_pc_port="8080",
    imei="004403160433860",
    imsi="262033100008233",
    qualcomm_prototype=True,
    # service_call_attach='17',
    # service_call_detach='17',
)

_android3 = TafUeAndroid(
    serial_number="db6ec13d",  # import,check by "adb ls"
    # capabilities=['REAL_UE', "samsung_ue"],
    capabilities=["qualcomm"],
    ue_pc_address="10.57.150.133",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    phone_number="+8613032996485",
    ue_pc_port="8080",
    imei="004403162107801",
    imsi="262033100011002",
    qualcomm_prototype=True,
    # service_call_attach='17',
    # service_call_detach='17',
)

_android4 = TafUeAndroid(
    serial_number="83fe0001",  # import,check by "adb ls"
    # capabilities=['REAL_UE', "samsung_ue"],
    capabilities=["qualcomm"],
    ue_pc_address="10.57.150.133",
    data_transfer=[_data_transfer_iperf,
                   _data_transfer_ping,
                   _data_transfer_ftp],
    phone_number="+8613032996485",
    ue_pc_port="8080",
    imei="004403160738839",
    imsi="262033100010998",
    qualcomm_prototype=True,
    # service_call_attach='17',
    # service_call_detach='17',
)



#AVHA
_pdu_1 = HBTE(
    addr="10.57.251.226",
    port_numbers=[1, 2, 3, 4, 5, 6],
)
#FDD RF AHFIB
_pdu_2 = HBTE(
    addr="10.57.251.229",
    port_numbers=[1, 2, 3, 4, 5, 6],
)
#gnb 37577 and 37434
_pdu_3 = HBTE(
    addr="10.57.251.228",
    port_numbers=[1, 2, 3, 4, 5, 6],
)


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    )

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.129", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[2],
    radio_type=RadioTypes.AHFIB,
    )
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.130", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[3],
    radio_type=RadioTypes.AHLOA,
    )
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.131", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.131", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AHLOA,
    )
_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AVHA,
    )

_fsp_1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    hardware_version="474824A.103",
    serial_number="DH220940564",
    )
    
_fsp_2 = CapacityUnit(
    addr="192.168.253.24",
    hardware_type="ABIA",
    hardware_version="473096A.103",
    serial_number="L1171408874",
    )
_fsp_3 = CapacityUnit(
    addr="192.168.253.40",
    hardware_type="ABIP",
    hardware_version="473096A.103",
    serial_number="L1234804254",
    )
_fsp_4 = CapacityUnit(
    addr="192.168.253.36",
    hardware_type="ABIP",
    hardware_version="474824A.103",
    serial_number="L1233804756",
    )

_fsp_5 = CapacityUnit(
    addr="192.168.253.37",
    hardware_type="ABIP",
    hardware_version="474824A.103",
    serial_number="L1233804757",
    )

# #DU for classicalBTS
_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1, _fsp_2,_fsp_3],
    pdu_port=_pdu_3.pdu_ports[1],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1234809306",
)
_fct_2 = CommonUnit(
    SshServiceDetails(
#        addr="192.168.255.7", username="toor4nsn", password="oZPS0POrRieRtu"
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_4, _fsp_5],
    pdu_port=_pdu_3.pdu_ports[2],
    hardware_type="ASIM",
    hardware_version="A.102",
    serial_number="L1234809436",
    )

_airscale1 = Airscale(common_units=[_fct_1])
_airscale2 = Airscale(common_units=[_fct_2])

_cu = CU(backhaul_site_oam_ip=NetworkAddress(v4='10.57.149.131', vlan_id=None,
                                             routing=RoutingInformation(gateway='10.57.149.129', ip_prefix_length=27)),
    oam_ssh_connection_details=SshServiceDetails(addr='10.57.149.131', username='toor4nsn', password='oZPS0POrRieRtu'),
    oam_http_connection_details=HttpConnectionDetails(addr='10.57.149.131', username='Nemuadmin', password='nemuuser'),
    x2c=NetworkAddress(v4='10.57.149.131', vlan_id=None,routing=RoutingInformation(gateway='10.57.149.129', ip_prefix_length=27)),
    x2u=NetworkAddress(v4='10.57.149.131', vlan_id=None,routing=RoutingInformation(gateway='10.57.149.129', ip_prefix_length=27)),
    s1u=NetworkAddress(v4='10.57.149.131', vlan_id=None,routing=RoutingInformation(gateway='10.57.149.129', ip_prefix_length=27))
    )

_du1 = DU(
    airscale=_airscale1,
    f1_m_ip_addr="192.168.255.129",
)

_du2 = DU(
    airscale=_airscale2,
)

_cbts1 = ClassicalBts(cu=_cu, dus=[_du1], instance_id=37577, global_bts_id=37577)
_cbts2 = ClassicalBts(cu=_cu, dus=[_du2], instance_id=37577, global_bts_id=37577)

_test_pc1 = TestPc(
  SshServiceDetails(addr="10.57.217.54", username="ute", password="uteUTE!"),
  connections=[
      NetworkAddress(v4="192.168.255.126"),
      Connection(
          interface="eth1",
          device=_cbts1.dus[0].airscale.common_units[0],
          interface_type="lmp",
      ),
  ],
 )
_test_pc2 = TestPc(
  SshServiceDetails(addr="10.57.217.55", username="ute",  password="uteUTE!"),
  connections=[
      NetworkAddress(v4="192.168.255.126"),
      Connection(
          interface="eth1",
          device=_cbts2.dus[0].airscale.common_units[0],
          interface_type="lmp",
      ),
  ],
 )

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2],
    #enbs=[_enb_sbts_1, _enb_sbts_2],
    gnbs=[_cbts1, _cbts2],
    #gnbs=[_classical_bts0],
    ues=[_android1,_android2,_android3,_android4],
    appserver=_appserver,
#    attenuator=[_attenuator],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_FULLRACK_SA_ASIML_ABIOB1_ABIAB3_2xAHLOA_2xAHFIB-ASIMR_ABIPB4_ABIPB5_AVHA",
)
__all__ = ["tl"]
