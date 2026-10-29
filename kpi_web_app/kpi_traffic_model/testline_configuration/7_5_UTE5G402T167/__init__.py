import os
from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FPFH, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
# added in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    RU,
)

__maintainer__ = "Helen.1.Chen"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "helen.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


##5GRU_1

_ru1_pdu = FPFH(addr="10.71.196.88", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQS,
)

##5GRU_2
_ru2_pdu = FPFH(addr="10.71.196.88", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQH,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="42167"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.2",
    iperf_path="/system/bin",
    port=42167,
)

##DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.212.100", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = HBTE(addr="10.71.196.86", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.71.212.100")

##CU

_cu = CU(
    backhaul_site_oam_ip="10.71.212.100",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.100", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.100", username="Nemuadmin", password="nemuuser"
    ),
)

##classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=167, global_bts_id=167)

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.61", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_iperf_details = _iperf

_appserver = AppServer(_iperf_details)

##cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_AEQY_eCPRI"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
