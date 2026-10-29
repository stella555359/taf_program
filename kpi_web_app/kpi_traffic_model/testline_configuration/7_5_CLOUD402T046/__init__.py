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
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
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

__maintainer__ = "Xiaxian Meng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "xiaxian.meng@nokia-sbell.com"

# common
__all__ = ["tl"]

# SCF (Workaround)
# SCF related configuration. Keep this part in this file temporary, will remove it when go to UTE
PARAMS_TO_MODIFY_SCF = [
    dict(value="Nokia HZ TL046", dist_name="MRBTS-1900", p_name="btsName"),
    dict(
        value="10.2.2.3",
        dist_name="MRBTS-1900/NRBTS-1/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="5G18A/5g_pid11_classical_eoc",
        dist_name="MRBTS-1900/EQM-1/APEQM-1",
        p_name="rapProfile",
    ),
    dict(
        value="10.2.2.6",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.6",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.7",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="10.2.2.7",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpAddr",
    ),
    dict(
        value="24",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-4",
        p_name="localIpPrefixLength",
    ),
    dict(value="3", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="dllaIniMcs"),
    dict(value="2073343", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="nrarfcn"),
    dict(value="22452", dist_name="MRBTS-1900/NRBTS-1/NRCELL-1", p_name="gscn"),
    dict(
        value="-73",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="ulPowerControlCommon",
        p_name="p0NominalPusch",
    ),
    dict(
        value="-109",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="ulPowerControlCommon",
        p_name="p0NominalPucch",
    ),
    dict(
        value="semiStatic",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="tddFrameStructure",
        p_name="frameStructureType",
    ),
    dict(
        value="2Symbols",
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
        value="1/4",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        list_name="tddFrameStructure",
        p_name="ulDlDataSlotRatio",
    ),
    dict(
        value="9",
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
]


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.128", username="root", password="nokia123"
    )
)

# #epcsim
_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc="03",
    tac=61,
    edaemon_port=10300,
    egate_port=20300,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.128", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/latest",
    cfg_filename="eNB_WMP_TL046_new.cfg",
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.246.195", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.2.2.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.246.196", port_numbers=[6])

_ru = RU(
    ru_hw_group="Above6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[6],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.247.11", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.246.195", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
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
    print("GNB RU PDU IP:{}".format(tl.gnbs[0].du.rus[0].pdu_port.pdu.addr))
    print("GNB RU PDU port:{}".format(tl.gnbs[0].du.rus[0].pdu_port.port_no))
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
