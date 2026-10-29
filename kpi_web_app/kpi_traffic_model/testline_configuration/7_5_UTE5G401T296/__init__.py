__maintainer__ = "Name Surname"
__team__ = "team"
__email__ = "mail"

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
from taf.config.testline.nms import Netact

__maintainer__ = "qingli"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "qingli@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.40", username="root", password="nokia123"
    )
)

_tl_cloud_topology = "CLOUD_5G_BB3"

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.2",
        username="nokiauser",
        tenant="FivG",
        password="NOki@234!",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="nokiauser", password="HZnoki@123!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(
    compute_nodes=[], control_nodes=[_control], version="NCIR", cloud_deployments=None
)

__flavor_prefix = "sg8_tl296"
_cbts_flavor = DeploymentFlavorStack(
    name="sg8_tl296_flavor",
    default_vnf_prefix=__flavor_prefix,
    configuration_data={"parameters": {"vnf_prefix": __flavor_prefix}},
)

__net_prefix = "sg8_tl296_net"
_cbts_net = DeploymentNetworkStack(
    name="sg8_tl296_net",
    configuration_data={
        "parameters": {
            "network_opts": {
                "vnf_name": __net_prefix,
                "dns_forwarders": "10.57.126.31",
                "networks": [
                    {
                        "name": "tracing",
                        "cidr": "172.16.4.0/24",
                        "gateway": "172.16.4.1",
                        "start": "172.16.4.100",
                        "end": "172.16.4.200",
                        "net_type": "vlan",
                        "sid": 1200,
                        "ip_ver": 4,
                        "provider": "provider0",
                    }
                ],
            }
        }
    },
)

_cbts_vnf = DeploymentVnfStack(
    name="sg8_tl296_vnf",
    configuration_data={
        "parameters": {
            "vnf_name": "sg8-tl296-vnf",
            # 'image': 'AirFrameVirtualized-0.190.239',
            # 'uvm_image': 'AirFrameVirtualized-0.190.239',
            "flavors": {
                "db": __flavor_prefix + "_db",
                "uvm": __flavor_prefix + "_uvm",
                "oam": __flavor_prefix + "_oam",
                "cpcl": __flavor_prefix + "_cpcl",
                "cpif": __flavor_prefix + "_cpif",
                "cpnrt": __flavor_prefix + "_cpnrt",
                "cpnb": __flavor_prefix + "_cpnb",
                "cpue": __flavor_prefix + "_cpue",
                "upue": __flavor_prefix + "_upue",
            },
            "password": {
                "_nokfsoperator": "$5$rounds=10000$lgSVGprx$BqAt4JD1XJCUBFy7NM4lbjzfns4iS09lM37.8ldaWzC",
                "root": "$5$rounds=10000$lgSVGprx$BqAt4JD1XJCUBFy7NM4lbjzfns4iS09lM37.8ldaWzC",
            },
            "internal_segment_ids": {
                "internal": 1201,
                "internal_srv": 1202,
                "internal_e1": 1203,
            },
            "external_networks": {
                "tracing": {"uuid": __net_prefix + "-tracing_net-v4"},
                "oam": {
                    "fixed_ips": [],
                    "fixed_v6_ips": [{"ip_address": "2a00:8a00:8000:136:10:57:250:2"}],
                    "uuid": "public-oam_net-v46",
                },
                "f1c": {
                    "fixed_ips": [],
                    "fixed_v6_ips": [
                        {"ip_address": "2a00:8a00:8000:136:10:57:250:4056"}
                    ],
                    "uuid": "public-fronthaul_net-v46",
                },
                "f1u": {
                    "fixed_ips": [],
                    "fixed_v6_ips": [
                        {"ip_address": "2a00:8a00:8000:136:10:57:250:4057"}
                    ],
                    "uuid": "public-fronthaul_net-v46",
                },
                "x2c": {
                    "fixed_ips": [],
                    "fixed_v6_ips": [
                        {"ip_address": "2a00:8a00:8000:136:10:57:250:8090"}
                    ],
                    "uuid": "public-backhaul_net-v46",
                },
                "x2u": {
                    "fixed_ips": [],
                    "fixed_v6_ips": [
                        {"ip_address": "2a00:8a00:8000:136:10:57:250:8091"}
                    ],
                    "uuid": "public-backhaul_net-v46",
                },
                "s1u": {
                    "fixed_ips": [],
                    "fixed_v6_ips": [
                        {"ip_address": "2a00:8a00:8000:136:10:57:250:8091"}
                    ],
                    "uuid": "public-backhaul_net-v46",
                },
            },
            "internal_provider_networks": "provider0",
            "internal_e1_provider_networks": "provider0",
            "user_info": {
                "system_info": {"default_user": {"name": "robot"}},
                "write_files": [
                    {
                        "content": "robot\n",
                        "path": "/etc/opt/nokia/setupsshkey.d/testusers",
                        "permissions": "0644",
                    },
                    {
                        "content": '{ "nonRootFullBashEnabled": true }',
                        "path": "/usr/lib/umconfig.d/zzz.json",
                        "permissions": "0644",
                    },
                ],
                "users": [
                    "default",
                    {
                        "plain_text_passwd": "rastre1",
                        "shell": "/bin/bash",
                        "name": "robot",
                        "sudo": ["ALL=(ALL) NOPASSWD:ALL"],
                        "lock_passwd": False,
                        "primary-group": "root",
                        "gecos": "Robot user for test automation purposes",
                        "home": "/home/robot",
                    },
                ],
            },
        }
    },
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")
_du_pdu = FACOM(addr="10.57.241.232", port_numbers=[5])
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.151.233", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale)

_cu = CU(
    backhaul_site_oam_ip="2a00:8a00:8000:136:10:57:250:2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:136:10:57:250:2", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="[2a00:8a00:8000:136:10:57:250:2]",
        username="Nemuadmin",
        password="nemuuser",
    ),
)

_cbts = CloudBts(
    dus=[_du],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="sg8-tl296",
    instance_id=296,
    global_bts_id=296,
)

# _epcsim = EPCSim(mme_ip='172.18.10.20', mcc=311, mnc=489, tac=788,
# default_ssh_connection_details=SshServiceDetails(
# addr='10.57.167.59', username='root', password='nokia123'),
# dir_path='/home/ute/WTS_QT', cfg_filename='basic_wts_tl086_ipv6.cfg',
# edaemon_port='22222', egate_port='20000')

# _netact = Netact('10.108.243.22')

tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    cloud_hostings=[_ncir],
    # nms=_netact
)

tl = TestlineWrapper(tl)
