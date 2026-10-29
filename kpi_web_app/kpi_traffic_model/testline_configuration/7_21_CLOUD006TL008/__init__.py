__maintainer__ = "Qian Janet"
__team__ = "Nanjing ASIR Test Team - LOTUS"
__email__ = "nj-fz-lotus@LIST.NOKIA.COM"
__owner_email__ = "janet.qian@nokia-sbell.com"

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
import os
import yaml

""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.11.186", username="ute", password="ute"
    )
)

_cu = CU(
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

_du_pdu = ATEN("1.1.1.1", [0])
_du_pdu_port = PduPort(_du_pdu, 0)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A101",
    pdu_port=_du_pdu_port,
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.11.187", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_airscale = Airscale([_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=1, global_bts_id=1)

_core_pc_ssh = SshServiceDetails(
    addr="10.66.14.205", username="scpadm", password="scpadm"
)
_core_pc = TestPc(default_ssh_connection_details=_core_pc_ssh)
_core = EPCSim(
    mme_ip="172.31.1.1",
    mcc=440,
    mnc=80,
    tac=1,
    default_ssh_connection_details=_core_pc_ssh,
    dir_path="/home/wts",
    cfg_filename="epcsim.cfg",
    edaemon_port=60002,
    egate_port=60001,
)

""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""
ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    ues=[],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKA101L_ABILA102B1_PERF",
    core=_core,
)

moler_config = {
    "DEVICES": {
        "GNB1_HUB1": {
            "DEVICE_CLASS": "ta_moler.device.hub.Hub",
            "CONNECTION_HOPS": {
                "UNIX_LOCAL": {
                    "PROXY_PC": {
                        "execute_command": "ssh",
                        "command_params": {
                            "host": "10.66.11.187",
                            "login": "ute",
                            "password": "ute",
                            "expected_prompt": "ute@721-CLOUD006TL008-gHUB",
                            "set_timeout": False,
                        },
                    }
                },
                "LINUX": {
                    "PROXY_PC": {
                        "execute_command": "ssh",
                        "command_params": {
                            "host": "10.66.11.187",
                            "login": "ute",
                            "password": "ute",
                            "expected_prompt": "ute@721-CLOUD006TL008-gHUB",
                        },
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
                            "host": "10.66.11.187",
                            "login": "ute",
                            "password": "ute",
                            "expected_prompt": "ute@721-CLOUD006TL008-gHUB",
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
                            "host": "10.66.11.186",
                            "login": "ute",
                            "password": "ute",
                        },
                    }
                }
            },
        },
    }
}


__all__ = ["tl"]
