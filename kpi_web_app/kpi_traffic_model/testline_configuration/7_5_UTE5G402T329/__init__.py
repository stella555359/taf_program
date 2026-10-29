__maintainer__ = "Chen Brian"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS"  # TL owner's team
__email__ = "brian.1.chen@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.pdu import FACOM, HBTE, TopYoung
from taf.config.testline.pdu import TopYoung as PDU_TopYoung
from taf.config.testline.ue import Prisma, MediaTek
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline import LicenseKeeper
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import Attenuator, AttenuationPort, TopYoung


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.35", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# PA
_attenuator = TopYoung(
    ip_addr="10.71.205.52",
    port=23,
    attenuation_port_numbers=[13, 14],
)

# 5g ru for TL329 classicalBTS
_gnb_1_ru_1_pdu = PDU_TopYoung(addr="10.71.196.80", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.1", username="rfsw", password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=	"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQN,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)


# 5g du for TL329 classicalBTS
_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="10.71.212.66", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = PDU_TopYoung(addr="10.71.196.78", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[1],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_gnb_1_du = DU(airscale=_gnb_1_airscale, rus=[_gnb_1_ru_1], f1_m_ip_addr="10.71.212.66")


# cu for TL329 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.66", username="Nemuadmin", password="nemuuser"
    ),
)

# TL329 classicalBTS
_classical_gnb_1 = ClassicalBts(
    dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="329", global_bts_id="10012"
)


_app_server_1 = TafUeAppServer(app_server_name="APP_1",
                               address="10.57.162.2",
                               user="mmw_sg2",
                               password="mm@2",
                               bind_interface_ip="10.57.162.2",
                               binary_path="/home/mmw_sg2/huawei_iperf/ipef",
                               expected_prompt="mmw_sg2",
                               ports=['42329','42329'])
 
_data_transfer_iperf = TafUeDataTransferProtocol(protocol_name='iperf',
                                                 app_server=_app_server_1,
                                                )
 
_data_transfer_ping = TafUeDataTransferProtocol(protocol_name='ping',
                                                app_server=_app_server_1,
                                                interval=1)
 
_pdn1 = \
    PDNTafUeAndroidDetails(entryName='default',                  #MANDATORY / use this entry point as KW argument (pdn)
                           apnName='dxdata1',                       #MANDATORY
                           apnType=['DEFAULT', 'MMS', 'XCAP'],   #MANDATORY
                           )
 
_android1 = TafUeAndroid(serial_number='9YS0220811002135',
                         capabilities=['REAL_UE'],
                         ue_pc_address='10.71.218.100',
                         data_transfer=[_data_transfer_iperf,
                                        _data_transfer_ping],
                         ssh_connection_details=SshServiceDetails(addr='10.71.218.100',
                                                                  username='nokia5G',
                                                                  password='noki@123'),
                         ue_pc_port='9191',
                         imsi='262038001006426',
                         pdns=[_pdn1],
                         )

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_gnb_1],
    ues=[_android1],
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)

__all__ = ["tl"]
