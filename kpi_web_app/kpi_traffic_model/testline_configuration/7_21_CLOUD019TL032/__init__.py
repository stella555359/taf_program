__maintainer__ = "Jiang Shengmin"
__team__ = "MN 5G&SC mmW&SC Pz 1 CN SysVrf 3"
__email__ = "I_EXT_MN_5GMMW_ASIRPROD_SYSVRF3@internal.nsn.com"
__owner_email__ = "shengmin.jiang@nokia-sbell.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim

from taf.config.testline.pdu import PduPort, ATEN, FACOM, Pdu, EPC
from taf.config.testline.gnb.networkaddress import NetworkAddress
import os
import yaml


##############
#  Test PCs  #
##############

test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.47", username="ute", password="ute"
    )
)

test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.48", username="ute", password="ute"
    )
)
# ),
# connections=[lteenb]
# )

################
#  gNB section #
################

cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIL", hardware_version="A102"
)

# need to be updated later for PDU configuration
# du_pdu = ATEN(
#     addr='',
#     port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9])
# du_pdu_port = PduPort(
#     pdu=du_pdu,
#     port_no=9)
#
# du_common_unit = CommonUnit(
#     lmp_connection=du_lmp_connection,
#     capacity_units=[du_capacity_unit],
#      pdu_port=du_pdu_port)

_du_pdu = ATEN("1.1.1.1", [0])
_du_pdu_port = PduPort(_du_pdu, 0)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A101",
    pdu_port=_du_pdu_port,
)
# need to be updated later for PDU configuration

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.29.50", username="ute", password="ute"),
        ),
        # telnet_connection_details=TelnetConnectionDetails(
        #     addr='tty-server',
        #     username='toor4nsn',
        #     password='oZPS0POrRieRtu'
        # )
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(
    #     pdu=Pdu(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=airscale, rus=[_ru])

cbts = ClassicalBts(cu=cu, dus=[_du], instance_id=4005, global_bts_id=4005)

################
#  eNB section #
################

_real_enb_pdu = FACOM(addr="10.66.29.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_du_capacity_unit_enb = CapacityUnit(
    addr="192.168.253.39", hardware_type="ABIA", hardware_version="A103"
)

_du_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_du_capacity_unit_enb],
    hardware_type="ASIA",
    hardware_version="A203",
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_du_common_unit_enb])

lteenb = RealEnb(
    system_module=_real_enb,
    x2_link_addr=NetworkAddress(v4="172.30.1.10"),
    instance_id=32,
    global_bts_id=32,
)


################
#    EPCSim    #
################

epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.47",
        username="ute",
        password="ute",
    ),
    dir_path="/opt/iphy/latest",
    cfg_filename="sim_ipv4.cfg",
)

# tl = TestLine(test_pc=test_pc, gnbs=[cbts], enbs=[lteenb], ues=None, core=epcsim,
#               tl_cloud_topology='CLOUD_5G_CLASSICAL_ASIR_ASIK101L_ABIL101B1')

################
#     Moler    #
################

moler_config = {
    "DEVICES": {
        "GNB1_HUB1": {
            "DEVICE_CLASS": "ta_moler.device.hub.Hub",
            "CONNECTION_HOPS": {
                "UNIX_LOCAL": {
                    "PROXY_PC": {
                        "execute_command": "ssh",
                        "command_params": {
                            "host": "10.66.29.50",
                            "login": "ute",
                            "password": "ute",
                            "expected_prompt": "ute@SC-NJN-CLOUD019TL032-5GHUB",
                            "set_timeout": False,
                        },
                    }
                },
                "LINUX": {
                    "PROXY_PC": {
                        "command_params": {
                            "expected_prompt": "ute@SC-NJN-CLOUD019TL032-5GHUB",
                        }
                    }
                },
            },
        },
        "HUB1_WS": {
            "DEVICE_CLASS": "moler.device.unixremote.UnixRemote",
            "CONNECTION_HOPS": {
                "UNIX_LOCAL": {
                    "UNIX_REMOTE": {
                        "execute_command": "ssh",
                        "command_params": {
                            "host": "10.66.29.50",
                            "login": "ute",
                            "password": "ute",
                            "expected_prompt": "ute@SC-NJN-CLOUD019TL032-5GHUB",
                            "set_timeout": False,
                        },
                    }
                },
            },
        },
        "GNB1_ASIMGR": {
            "DEVICE_CLASS": "ta_moler.device.asi_mgr.AsiMgr",
            "CONNECTION_HOPS": {
                "UNIX_LOCAL": {
                    "UNIX_REMOTE": {
                        "execute_command": "ssh",  # default value
                        "command_params": {
                            "host": "10.66.29.47",
                            "login": "ute",
                            "password": "ute",
                            "expected_prompt": "ute@SC-NJN-CLOUD019TL032",
                        },
                    }
                }
            },
        },
    }
}


################
#  UE config   #
################
def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

################
#   TestLine   #
################
tl = TestLine(
    test_pc=test_pc_gnb,
    test_pcs=[test_pc_gnb, test_pc_enb],
    gnbs=[cbts],
    enbs=[lteenb],
    ues=[_ue_config],
    core=epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIK101L_ABIL101B1",
)

__all__ = ["tl"]
