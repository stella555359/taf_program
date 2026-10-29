__maintainer__ = "Maciej Cupial"
__team__ = "DCM"
__email__ = "maciej.cupial@nokia.com"


from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU, Connection
from taf.config.testline.pdu import Gude


__all__ = ["tl"]

_cu_gnb_1 = CU(
    backhaul_site_oam_ip="192.168.255.1",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(v4='10.0.1.2', vlan_id=4093),
    x2u=NetworkAddress(v4='10.0.1.2', vlan_id=4093),
    s1u=NetworkAddress(v4='10.0.1.2', vlan_id=4093),
)

_pdu_gnb = Gude(addr="10.44.200.70", port_numbers=[10, 11, 12], model="EPC", version="8220-1")

_ru_1 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002472",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_2 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002473",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_3 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002474",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_4 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002475",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_5 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002476",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_6 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002477",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_7 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002450",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_8 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002451",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_9 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002452",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_10 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002453",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_11 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002454",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)

_ru_12 = RU(
    ru_hw_group="",
    product_code="37L4CRRU",
    serial_number="00002455",
    radio_type="simulated O-RU",
    pdu_port="1.1.1.1",
)


_abip_gnb_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
    hardware_version="A102",
    serial_number="L1253206572",
)

_abio_gnb_2 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A105",
    serial_number="L1232101301",
)

_abio_gnb_3 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A105",
    serial_number="L1232101299",
)

_asil_gnb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abip_gnb_1, _abio_gnb_2, _abio_gnb_3],
    hardware_type="ASIL",
    hardware_version="A103",
    serial_number="L1232304352",
    pdu_port=_pdu_gnb.pdu_ports[11],
)

_airscale_gnb_1 = Airscale(common_units=[_asil_gnb])

_du_1 = DU(
    airscale=_airscale_gnb_1,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9, _ru_10, _ru_11, _ru_12]
)

_cbts_1 = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1], instance_id=1
)

_apo_abio_1 = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type='ASIL',
                capacity_units=[
                    CapacityUnit(addr='192.168.253.84', hardware_type='ABIO')],
                pdu_port=_pdu_gnb.pdu_ports[12]
          )
       ]
    ),
)

_apo_abio_2 = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    "192.168.200.2", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type='ASIL',
                capacity_units=[
                    CapacityUnit(addr='192.168.253.84', hardware_type='ABIO')],
                pdu_port=_pdu_gnb.pdu_ports[10]
          )
       ]
    ),
)

_lmp_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.221.215", username="ute", password="UTE.debian12"
    ),
    connections=[
        Connection(
           interface="eth1",
           interface_type="lmp",
           device=_cbts_1.dus[0].airscale.common_units[0]
        ),
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_apo_abio_1
        ),
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_apo_abio_2
        )
    ]
)

tl = TestLine(
    test_pc=_lmp_vm,
    test_pcs=[_lmp_vm],
    gnbs=[_cbts_1],
    pdus=[_pdu_gnb],
    tl_cloud_topology="CLOUD_DCM_I_[LO][LO]_AP_[LOO]",
    ues=[_apo_abio_1, _apo_abio_2]
)


class EGen:
    hostname = "10.42.75.246"
    username = "ute"
    password = "egenDCM2137@"


class KVM:
    hostname = "10.42.221.229"


setattr(tl, "kvm", KVM)

setattr(tl, "egen", EGen)
setattr(tl, "mrbts_id", "1")
setattr(tl, "ltesim_pc_host", "10.42.221.215")

setattr(tl, "af_type", "AF")
setattr(tl, "af_bmc_ip", "10.42.210.128")
setattr(tl, "af_bmc_username", "admin")
setattr(tl, "af_bmc_passwd", "admin")

setattr(tl, "specific_convert_mmt_dir", "/cygdrive/c/ute/MMT")

setattr(tl, "enable_af_ssh_reset_WA", "no")
setattr(tl, "enb_type", "lrc")
setattr(tl, 'gnb_id_list', [1])
setattr(tl, "windows_control_pc_user", "ute")
setattr(tl, "windows_control_pc_pwd", "ute")
setattr(tl, 'oam_http_addr', '192.168.255.1')
setattr(tl, 'oam_http_port', '443')
setattr(tl, 'oam_http_username', 'Nemuadmin')
setattr(tl, 'oam_http_password', 'nemuuser')
setattr(tl, "ute_control_pc_host", "10.42.221.215")
setattr(tl, "gnb_control_pc_host", ["10.42.221.215"])
setattr(tl, "gnb_control_pc_user", "ute")
setattr(tl, "gnb_control_pc_pwd", "ute")
setattr(tl, "epc_host", "10.42.221.215")
setattr(tl, "l3sim_host", "10.42.221.215")
setattr(tl, "ntp_server_ip_address", "10.42.248.70")
