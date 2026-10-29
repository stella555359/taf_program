import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeMtk
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.pdn import PDN, PDPTypes

# from taf.config.testline.attenuator import HBTE
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

__maintainer__ = "Zhang Xiaping"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG11"
__email__ = "xiaping.zhang@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.208.94", username="ute", password="ute"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.133.68",
    mcc="262",
    mnc="03",
    tac="270",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_12341"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

## 4GRU for RealEnb
# _ru_enb_pdu = TopYoung(addr="10.101.45.85", port_numbers=[4])
#
# _ru_enb = RadioModule(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="usr", password="psswd"
#    ),
#    pdu_port=_ru_enb_pdu.pdu_ports[4],
# )
#
## #RealEnb
# _real_enb_pdu = TopYoung(addr="10.101.45.86", port_numbers=[4])
#
#
# _common_unit_2 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.101.49.235", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
#    pdu_port=_real_enb_pdu.pdu_ports[4],
# )
#
# _real_enb = Airscale(common_units=[_common_unit_2])
#
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.64.49.90", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type="AEHC",
)

_ru_2_pdu = HBTE(addr="10.64.49.90", port_numbers=[2])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[2],
    radio_type="AHFIB",
)

#_ru_3_pdu = TopYoung(addr="10.71.197.59", port_numbers=[4])

#_ru_3 = RU(
#    ru_hw_group="hw_group",
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="user", password="pass"
#    ),
#    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
#    pdu_port=_ru_3_pdu.pdu_ports[4],
#    radio_type="AHFB",
#)

#_ru_4_pdu = HBTE(addr="10.71.197.49", port_numbers=[6])

#_ru_4 = RU(
#    ru_hw_group="hw_group",
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="user", password="pass"
#    ),
#    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
#    pdu_port=_ru_4_pdu.pdu_ports[6],
#    radio_type="AWHQX",
#)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.64.49.93", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2],
    f1_m_ip_addr="10.64.53.163",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.64.53.163",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.53.163", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.53.163", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="37425", global_bts_id="37425"
)



# _mtk_appserver_taf = TafUeAppServer(
    # app_server_name="APP_SERVER_1",
    # address="10.57.162.6",
    # user="vrf4_sg11",
    # password="vrf4@11",
    # bind_interface_ip="10.57.162.6",
    # expected_prompt="[vrf4_sg11@rocky9-KVM-nogui ~]$ ",
    # binary_path="/usr/bin/iperf",
    # ports=[21603, 21604, 21605],
# )
 
# _mtk_data_transfer_iperf = TafUeDataTransferProtocol(
    # protocol_name="iperf",
    # app_server=_mtk_appserver_taf,
    # interval=1,
    # binary_path="/data/local/tmp/iperf",
    # version=2,
# )


_pdns = [
          PDN(pdp_type=PDPTypes.IPV4V6.value, apn='dxdata1'),
   		  PDN(pdp_type=PDPTypes.IPV4V6.value, apn="wap2.nokia.com")
]


# _mtk = TafUeMtk(
    # ue_pc_address="10.64.57.18",
    # ue_pc_port=8080,
	# serial_number="0123456789ABCDEF",
    # pdns=_pdns,
    # data_transfer=[_mtk_data_transfer_iperf],
    # com_port="auto",
    # edb_file_path="auto",
    # log_filter="2.Gen98_Default_Standard",
    # imei="123456789012347",
    # imsi="262033100001120",
    # default_pdn_name="dxdata1",
    # capabilities=["REAL_UE", "mtk_ue"],
# )


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    # enbs=[_lte_real_enb],
    # ues=[_mtk],
    # ues=[_fastmile_1, _fastmile_2],
    tl_cloud_topology=_tl_cloud_topology,
)
