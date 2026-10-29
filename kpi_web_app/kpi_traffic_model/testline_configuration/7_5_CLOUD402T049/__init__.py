import os
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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Yin May"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "may.yin@nokia-sbell.com"

# common
__all__ = ["tl"]

# SCF (Workaround)
# SCF related configuration. Keep this part in this file temporary, will remove it when go to UTE
PARAMS_TO_MODIFY_SCF = [
    dict(value="Nokia HZ SQ4 TL049", dist_name="MRBTS-1900", p_name="btsName"),
    dict(
        value="10.2.2.12",
        dist_name="MRBTS-1900/NRBTS-1/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="5G18A/5g_pid12_classical_aahf_eoc",
        dist_name="MRBTS-1900/EQM-1/APEQM-1",
        p_name="rapProfile",
    ),
    dict(
        value="10.2.2.10",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.13",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.14",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.14",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpPrefixLength",
    ),
    dict(value="509070", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="nrarfcn"),
    dict(value="6363", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="gscn"),
    dict(value="60MHz", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="chBw"),
    dict(
        value="97",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="prachConfigurationIndex",
    ),
    dict(
        value="15",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="zeroCorrelationZoneConfig",
    ),
    dict(
        value="41",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="freqBandIndicatorNR",
    ),
    dict(
        value="12",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="type0CoresetConfigurationIndex",
    ),
    dict(
        value="true",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SECADM-1",
        p_name="actServiceAccountSsh",
    ),
    dict(value="244", dist_name="MRBTS-1900/NRBTS-1", p_name="mcc"),
    dict(value="9", dist_name="MRBTS-1900/NRBTS-1", p_name="mnc"),
    dict(value="2", dist_name="MRBTS-1900/NRBTS-1", p_name="mncLength"),
    dict(value="ms10000", dist_name="MRBTS-1900/NRBTS-1", p_name="t304"),
    dict(
        value="false",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="beamSet",
        p_name="nrBtsBeamRefinementP2",
    ),
    dict(
        value="-90",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="ulPowerControlCommon",
        p_name="p0NominalPusch",
    ),
    dict(
        value="-108",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="ulPowerControlCommon",
        p_name="p0NominalPucch",
    ),
    dict(
        value="tdLte",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="tddFrameStructure",
        p_name="frameStructureType",
    ),
    dict(
        value="4Symbols",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="tddFrameStructure",
        p_name="guardPeriodLength",
    ),
    dict(
        value="0ms",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="tddFrameStructure",
        p_name="lteToNrFrameShift",
    ),
    dict(
        value="2/8",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="tddFrameStructure",
        p_name="ulDlDataSlotRatio",
    ),
    dict(
        value="1",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="cipherPrefL",
        p_name="nea0",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="cipherPrefL",
        p_name="nea1_128",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="cipherPrefL",
        p_name="nea2_128",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="cipherPrefL",
        p_name="nea3_128",
    ),
    dict(
        value="1",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="integrityProtPrefL",
        p_name="nia0",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="integrityProtPrefL",
        p_name="nia1_128",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="integrityProtPrefL",
        p_name="nia2_128",
    ),
    dict(
        value="0",
        dist_name="MRBTS-1900/NRBTS-1",
        list_name="integrityProtPrefL",
        p_name="nia3_128",
    ),
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),
]

PARAMS_TO_ADD_ELEMENTS = [
    dict(value="1", dist_name="MRBTS-1900/NRBTS-1/LTEENB-1", p_name="eNodeBId"),
    dict(value="10.2.2.12", dist_name="MRBTS-1900/NRBTS-1/LTEENB-1", p_name="ipAddr"),
    dict(
        value="available",
        dist_name="MRBTS-1900/NRBTS-1/LTEENB-1",
        p_name="x2LinkStatus",
    ),
    dict(
        value="enabled",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SECADM-1",
        p_name="serviceAccountSshStatus",
    ),
    dict(
        value="32767", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="nrCellIdentity"
    ),
]

PARAMS_TO_ADD_LIST = [
    dict(dist_name="MRBTS-1900/NRBTS-1/LTEENB-1", list_name="enbPlmn")
]

PARAMS_TO_ADD_LISTITERMS = [
    dict(
        dist_name="MRBTS-1900/NRBTS-1/LTEENB-1",
        list_name="enbPlmn",
        elements=dict(mcc="244", mnc="9", mncLength="2"),
    )
]

PARAMS_TO_DELETE_TL = [
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELL-2"),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELL-2/NRCELL_FDD-1"),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELL-3"),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELL-3/NRCELL_FDD-1"),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELL-4"),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELL-4/NRCELL_FDD-1"),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELLGRP-0", list_name="nrCellList", index=1),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELLGRP-0", list_name="nrCellList", index=1),
    dict(dist_name="MRBTS-1900/NRBTS-1/NRCELLGRP-0", list_name="nrCellList", index=1),
]

# Qualcomm UE control PC
UE_control_pc = "10.57.249.56"
UE_control_pc_user = "5G"
UE_control_pc_password = "5G"
UE_ADDR = "1.7.11.1"
device_model = "dca636d8"
ABSTRACT_LIB_CONFIG = (
    "/home/ute/Projects/robotws5g/testsuite/RRM/Hangzhou/"
    "5GI000113_C/Test_Data/android_qualcomm_ue_config_TL049.yml"
)
lte_earfcn = "40521"

# Catch S1 package eth config
NIC = "eth1"

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.42", username="root", password="nokia123"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc="03",
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.42", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10300,
    egate_port=20300,
    dir_path="/opt/iphy/latest",
    cfg_filename="eNB_WMP_TL049_eNB_bimin.cfg",
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.168", port_numbers=[8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.2.2.12", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[8],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.246.241", port_numbers=[1])

_ru = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[1],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.237.60", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.241.168", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=None)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# switch
_dell_s4048on_ssh = SshServiceDetails(
    addr="1.0.0.1", port=44444, username="user", password="pass"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
)

# old version keyword under robotws5g/resource compatibility workaround
tl = TestlineWrapper(tl)

if __name__ == "__main__":
    print("Example use of new TL config")
    print("EPC address:{}".format(tl.core.default_ssh_connection_details.addr))
    print("EPC username:{}".format(tl.core.default_ssh_connection_details.username))
    print("EPC password:{}".format(tl.core.default_ssh_connection_details.password))
    print("EPC dir_path:{}".format(tl.core.dir_path))
    print("EPC cfg_filename:{}".format(tl.core.cfg_filename))
    print("EPC edaemon port:{}".format(tl.core.edaemon_port))
    print("EPC egate port:{}".format(tl.core.egate_port))
    print(
        "RealEnb SSH address:{}".format(
            tl.enbs[0].airscale.common_units[0].lmp_connection.addr
        )
    )
    print(
        "RealEnb SSH username:{}".format(
            tl.enbs[0].airscale.common_units[0].lmp_connection.username
        )
    )
    print(
        "RealEnb SSH password:{}".format(
            tl.enbs[0].airscale.common_units[0].lmp_connection.password
        )
    )
    print(
        "RealEnb PDU IP:{}".format(
            tl.enbs[0].airscale.common_units[0].pdu_port.pdu.addr
        )
    )
    print(
        "RealEnb PDU port:{}".format(
            tl.enbs[0].airscale.common_units[0].pdu_port.port_no
        )
    )
    print("GNB RU FRIJ PDU IP:{}".format(tl.gnbs[0].du.rus[0].pdu_port.pdu.addr))
    print("GNB RU FRIJ PDU port:{}".format(tl.gnbs[0].du.rus[0].pdu_port.port_no))
    print(
        "GNB DU PDU IP:{}".format(
            tl.gnbs[0].du.airscale.common_units[0].pdu_port.pdu.addr
        )
    )
    print(
        "GNB DU PDU port:{}".format(
            tl.gnbs[0].du.airscale.common_units[0].pdu_port.port_no
        )
    )
    print(
        "GNB ASIK IP:{}".format(
            tl.gnbs[0].du.airscale.common_units[0].lmp_connection.addr
        )
    )
    print(
        "GNB ASIK SSH username:{}".format(
            tl.gnbs[0].du.airscale.common_units[0].lmp_connection.username
        )
    )
    print(
        "GNB ASIK SSH password:{}".format(
            tl.gnbs[0].du.airscale.common_units[0].lmp_connection.password
        )
    )
