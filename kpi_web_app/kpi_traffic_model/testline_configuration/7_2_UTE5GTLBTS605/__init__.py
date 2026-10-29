__maintainer__ = "Monika Banas, Marcin Wachacki"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "monika.banas@nokia.com, marcin.wachacki@nokia.com"


import os
import yaml
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline import NetworkAddress, RU, RUExtension
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, HPE, RRB
from taf.config.testline.testline import TestLine


# Test PCs configuration (VMs)
_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="10.53.188.167", username="ute", password="BT5l@bus3rl0g1n"   # VM ip addr (e.g. read from vnc), user, password (change it)
)

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details
)

# gNB configuration
_default_ssh_lmp_connection = SshServiceDetails(  # LPM connection to gNB (change it)
    addr="192.168.255.129",  # (change it)
    username="toor4nsn",  # (change it)
    password="oZPS0POrRieRtu",  # (change it)
)

_gnb_1_bc_ip = NetworkAddress(v4="10.53.188.253")  # bc (e.g. read localIpAddr param form webui) (change it)

_default_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_bc_ip.v4,
    username="Nemuadmin",  # user/password for webui (change it)
    password="nemuuser",   # user/password for webui (change it)
)

# CU
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_bc_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_gnb_1_oam_http_connection,
)

# DUs
_du_lmp_connection_gnb_1 = _default_ssh_lmp_connection
_du_lmp_connection_gnb_1.proxy = _test_pc_gnb_1_default_ssh_connection_details

_asil_master_gnb = CapacityUnit(addr="fsp1_c")

_du_common_unit_gnb_1 = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb_1,
    capacity_units=[_asil_master_gnb],
    hardware_type="ASIB",
    hardware_version="102",
    pdu_port=PduPort(pdu=RRB(addr="10.41.155.54", port_numbers=[3]), port_no=7),
)

_gnb_1_ru_0 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr=NetworkAddress(v4="172.22.48.2").v4,  # try ssh to gnb and type: cat /rom/config/FRIps.txt and read RU's ip 
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(pdu=HPE(addr="ze01.mgt.ska-lab.nsn-rdnet.net", port_numbers=[2]), port_no=2),  # I think that it is not required
)

_airscale_gnb_1 = Airscale(common_units=[_du_common_unit_gnb_1])
_du_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_1_ru_0])

# gNB configuration
_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id="605",  # mrbts id (read from admin)
    global_bts_id="605",  # nrbts id (read from admin)
)

# TL configuration
tl = TestLine(
    test_pc=_test_pc_gnb_1,
    gnbs=[_gnb_1],
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_AZHL",
)

def _set_abstract_lib_config_env(ue_config_file):
   tl_config_dir = os.path.dirname(os.path.abspath(__file__))
   ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
   with open(ue_config_abs_path) as ta_ue_config:
       ue_config = yaml.safe_load(ta_ue_config)
   os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

   return ue_config

#_ue_config = _set_abstract_lib_config_env("ue.yaml")

_ue_config = _set_abstract_lib_config_env("ta_ue_config.yaml")

__all__ = ["tl"]
