import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim
from taf.config.testline.nms import Netact
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

# from taf.config.testline.attenuator import HBTE
from taf.config.testline.appserver import AppServer


__maintainer__ = "Li Yuanyuan"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "yuanyuan.liu@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.94 ", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
_ru_enb_pdu = TopYoung(addr="10.101.45.230", port_numbers=[3])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[3],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.71.195.99", port_numbers=[8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[8],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.71.195.104", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type="AEWB",
)

_ru_2_pdu = HBTE(addr="10.71.195.104", port_numbers=[2])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[2],
    radio_type="AEWB",
)

_ru_3_pdu = HBTE(addr="10.71.195.104", port_numbers=[3])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[3],
    radio_type="AEWB",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = TopYoung(addr="10.71.195.108", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3], f1_m_ip_addr="192.168.255.129")


##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.209.41",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.41", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.41", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2076", global_bts_id="2076"
)

netact_id_Han = {
    "cmwas_ip": "10.107.183.61",
    "user": "omc",
    "password": "Nokia126_",
    "url": "https://han5lbwas.han5.srnhz.nsn-rdnet.net/",
    "url_user": "omc",
    "url_password": "Nokia126_",
    "mr": "MRC-5GSC-HZ/MR-5GSC-HZ",
}

netact_id_Qin = {
    "cmwas_ip": "10.107.178.214",
    "user": "omc",
    "password": "Nokia123!",
    "url": "https://qin1lbwas.qin1.srnhz.nsn-rdnet.net/",
    "url_user": "omc",
    "url_password": "Nokia123!",
    "mr": "MRC-5GSC-HZ/MR-5GSC-HZ",
}

_netact = Netact(netact_id_Han)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
