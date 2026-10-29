# This script was generated automatically, --None-- values indicate lacking data, please fill them manually

__maintainer__ = "Xuewen.wen"
__email__ = "xuewen.wen@nokia-sbell.com"

import os, subprocess
from typing import Optional, List, Union
from enum import Enum
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import Gude, TopYoung, FACOM, FPFH
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline import TopYoung_PDU
from taf.config.testline import HBTE_PDU
from taf.config.testline.pdu import FACOM, HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude,FPFH
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
    HttpConnectionDetails,
)
from taf.config.testline import NetAct



vm_password='uteUTE!'
if os.path.exists('/etc/ute/vncpasswd'):
    vm_password=subprocess.check_output("sudo cat /etc/ute/vncpasswd", shell=True).decode('utf-8')





### BLR Labs ### start ###
_netact_ssh_1013 = SshServiceDetails('10.41.146.72', 'omc', password='Medsql!_1893')
_netact_http_1013 = HttpConnectionDetails('srnclab1013lbwas.srnblr.nsn-rdnet.net', 'omc', password='Medsql!_1893')
_netact_1013 = NetAct(_netact_ssh_1013, _netact_http_1013)

_netact_ssh_1014 = SshServiceDetails('10.41.146.105', 'omc', password='Medsql!_1893')
_netact_http_1014 = HttpConnectionDetails('srnclab1014lbwas.srnblr.nsn-rdnet.net', 'omc', password='Medsql!_1893')
_netact_1014 = NetAct(_netact_ssh_1014, _netact_http_1014)

_netact_ssh_1047 = SshServiceDetails('10.43.48.192', 'omc', password='Medsql!_1893')
_netact_http_1047 = HttpConnectionDetails('srnclab1047lbwas.srnblr.nsn-rdnet.net', 'omc', password='Medsql!_1893')
_netact_1047 = NetAct(_netact_ssh_1047, _netact_http_1047)

_netact_ssh_2003 = SshServiceDetails('10.82.47.46', 'omc', password='Medsql!_1893')
_netact_http_2003 = HttpConnectionDetails('srnclab2003lbwas.srnblr.nsn-rdnet.net', 'omc', password='Medsql!_1893')
_netact_2003 = NetAct(_netact_ssh_2003, _netact_http_2003)

### Hangzhou Labs Recommend### end ###

_netact_ssh_2014 = SshServiceDetails('10.107.183.26', 'omc', password='Nokia123!')
#_netact_ssh_2014 = SshServiceDetails('10.107.245.83', 'omc', password='Nokia123!')
_netact_http_2014 = HttpConnectionDetails('han5lbwas.han5.srnhz.nsn-rdnet.net', 'omc', password='Nokia123!')
_netact_2014 = NetAct(_netact_ssh_2014, _netact_http_2014)
### BLR Labs ### start ###

### Hangzhou Labs ### start ###
_netact_ssh_chen4 = SshServiceDetails('10.108.248.82', 'omc', password='Nokia123!')
_netact_http_chen4 = HttpConnectionDetails('chen4lbwas.chen4.srnhz.nsn-rdnet.net', 'omc', password='Nokia123!')
_netact_chen4 = NetAct(_netact_ssh_chen4, _netact_http_chen4)
### Hangzhou Labs ### end ###

_ue_pc_ssh_1 = SshServiceDetails('10.97.92.202', 't05-tester', password='Nokia123!')
_ue_pc_ssh_2 = SshServiceDetails('10.97.92.203', 't05-tester', password='Nokia123!')

_iperf_pc_ssh = SshServiceDetails('10.106.245.178', 'ute', password=vm_password)
_android_iperf = IperfDataTransferDetails(_iperf_pc_ssh, '40.1.1.254', None)




###PDU####
_pdu_1 = FACOM(
    addr="10.97.92.21",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

_pdu_2 = FPFH(
    addr="10.97.92.231",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

_pdu_3 = TopYoung(
    addr="10.97.97.148",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)


###BBMOD####

_fsp_2 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    hardware_version="475266A.103",
    serial_number="L1211511269",
)
_fsp_1 = CapacityUnit(
    addr="192.168.253.24",
    hardware_type="ABIO",
    hardware_version="475266A.102",
    serial_number="L1204506006",
)


###SMOD####
_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1, _fsp_2],
    pdu_port=_pdu_1.pdu_ports[1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1211104932",
)
_smod_1 = Airscale([_fct_1])




###RMOD####

_rmod_1 = RU(
    ru_hw_group="FRMr5.1a_4T4R",
    radio_type=RadioTypes.AHEGB,
    serial_number="EA203761589",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="172.16.16.161", port=2323
    ),
    pdu_port=_pdu_3.pdu_ports[1],
)
_rmod_2 = RU(
    ru_hw_group="FRMr2.2_3T6R_Medusa",
    radio_type=RadioTypes.FXDB,
    serial_number="1M170932989",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="172.16.17.33", port=2323
    ),
    pdu_port=_pdu_2.pdu_ports[3],
)


# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.57.179.233",
    username="vrf3_sg7",
    password="vrf3@sg7",
    port="47777",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="47778",
)

_appserver = AppServer(_iperf)



#Mplan IP
_enb_sbts_1 = RealEnb(
    system_module=_smod_1,
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.71.215.142"),
    instance_id=37339,
)

#TestPC
_test_pc_1 = TestPc(
    SshServiceDetails(addr="10.57.155.104", username="ute", password='iW_K#8.ute%A10h0m0ra'),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            device=_enb_sbts_1.system_module.common_units[0],
            interface_type="lmp",
        ),
        ],
)

# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.215.142", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.71.197.70", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[4],
)


# attenuator
_attenuator_0 = HBTE(
    addr="10.71.206.204",
    port_numbers=[4]
)

_attenuator_1 = HBTE(
    addr="10.71.206.205",
    port_numbers=[4]
)
    
_attenuator_2 = HBTE(
    addr="10.71.206.206",
    port_numbers=[4]
)

# #5GRU for classicalBTS
_ru1_pdu = FPFH(addr="10.71.197.72", port_numbers=[1])
_ru2_pdu = FPFH(addr="10.71.197.72", port_numbers=[2])
_ru3_pdu = FPFH(addr="10.71.197.72", port_numbers=[4])
_ru4_pdu = FPFH(addr="10.71.197.73", port_numbers=[2])
_ru5_pdu = FPFH(addr="10.71.197.73", port_numbers=[3])
_ru6_pdu = FPFH(addr="10.71.197.73", port_numbers=[4])
_ru7_pdu = FPFH(addr="10.71.197.73", port_numbers=[1])
_ru8_pdu = FPFH(addr="10.71.197.90", port_numbers=[1])
_ru9_pdu = FPFH(addr="10.71.197.90", port_numbers=[2])
_ru10_pdu = FPFH(addr="10.71.197.70", port_numbers=[2])
_ru11_pdu = FPFH(addr="10.71.197.70", port_numbers=[1])
_ru12_pdu = FPFH(addr="10.71.197.72", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    #attenuation_ports=[
    #    _attenuator_2.attenuator_ports[1],
    #    _attenuator_2.attenuator_ports[2],
    #    _attenuator_2.attenuator_ports[3],
    #   _attenuator_2.attenuator_ports[4],
    #],
    #serial_number="L1213413664",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    #attenuation_ports=[
    #    _attenuator_2.attenuator_ports[5],
    #    _attenuator_2.attenuator_ports[6],
    #    _attenuator_2.attenuator_ports[7],
    #    _attenuator_2.attenuator_ports[8],
    #],
    #serial_number="L1213413662",
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    #attenuation_ports=[
    #    _attenuator_2.attenuator_ports[9],
    #    _attenuator_2.attenuator_ports[10],
    #    _attenuator_2.attenuator_ports[11],
    #    _attenuator_2.attenuator_ports[12],
    #],
    #serial_number="L1210107221",
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    #attenuation_ports=[
    #    _attenuator_2.attenuator_ports[13],
    #    _attenuator_2.attenuator_ports[14],
    #    _attenuator_2.attenuator_ports[15],
    #    _attenuator_2.attenuator_ports[16],
    #],
    #serial_number="BL2116G1CHK",
)

_ru5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHLOA,
    #attenuation_ports=[
    #    _attenuator_1.attenuator_ports[1],
    #    _attenuator_1.attenuator_ports[2],
    #    _attenuator_1.attenuator_ports[3],
    #    _attenuator_1.attenuator_ports[4],
    #],
    #serial_number="BL2106G10IL",
)

_ru6 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru6_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHLOA,
    #attenuation_ports=[
    #    _attenuator_1.attenuator_ports[5],
    #    _attenuator_1.attenuator_ports[6],
    #    _attenuator_1.attenuator_ports[7],
    #    _attenuator_1.attenuator_ports[8],
    #],
    #serial_number="BL2106G10A2",
)

_ru7 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru7_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    #attenuation_ports=[
    #    _attenuator_1.attenuator_ports[9],
    #    _attenuator_1.attenuator_ports[10],
    #    _attenuator_1.attenuator_ports[11],
    #    _attenuator_1.attenuator_ports[12],
    #],
    #serial_number="BL2049V0VL4",
)

_ru8 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru8_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    #attenuation_ports=[
    #    _attenuator_1.attenuator_ports[13],
    #    _attenuator_1.attenuator_ports[14],
    #    _attenuator_1.attenuator_ports[15],
    #    _attenuator_1.attenuator_ports[16],
    #],
    #serial_number="BL2215V00PY",
)

_ru9 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru9_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFIB,
    #attenuation_ports=[
    #    _attenuator_0.attenuator_ports[1],
    #    _attenuator_0.attenuator_ports[2],
    #    _attenuator_0.attenuator_ports[3],
    #    _attenuator_0.attenuator_ports[4],
    #],
    #serial_number="BL2147V0RJA",
)



##DU
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9],
    f1_m_ip_addr="10.71.215.142",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.215.142",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.142", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.142", username="Nemuadmin", password="nemuuser"
    ),
)



# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="37339", global_bts_id="37339"
)

# #cloud_topology
_tl_cloud_topology = "CLASSICAL_1ASIL_2ABIO_BTS"
    
########invalid######
#_rnc = RNC(
#    rnc_id=301,
#    oms_ip=NetworkAddress("10.27.127.36"),
#    logging_ssh_connection_details=SshServiceDetails(
#        addr="10.94.92.155", username="Nemuadmin", password="Nemuadmin@123"
#    ),
#)

#_bsc = BSC(
#    name="BSC-1",
#    logging_telnet_connection_details=TelnetConnectionDetails(
#        addr="10.70.120.39", username="SYSTEM", password="SYSTEM"
#    ),
#)
########invalid######

tl = TestLine(
    #ues=[ _android_ue_1, _android_ue_2 ],
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1],
    enbs=[_enb_sbts_1],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    #bscs=[_bsc],
    #rncs=[_rnc],
    nms=_netact_ssh_2014,
    #attenuators=[_attenuator_0, _attenuator_1, _attenuator_2],
    appserver=_appserver,
    
)

__all__ = ["tl"]

dhcp_server = {
	"ip": "10.97.92.238",
	"user": "ute",
	"password": "UTE.debian12",
}

fault_4297={'faultId': 4297, 'faultName': 'NTP Server 2a00:8a00:8000:101::5 unavailable'}
fault_4654={'faultId': 4654, 'faultName': 'Ethernet port security is disabled'}
fault_61642={'faultId': 61642, 'faultName': 'SSH enabled'}
fault_61652={'faultId': 61652, 'faultName': 'R&D Service Port enabled'}
fault_61649={'faultId': 61649, 'faultName': 'LMP access via port'}
fault_4655={'faultId': 4655, 'faultName': 'Automatic BTS Operator Certificate retrieval unsuccessful'}
fault_4293={'faultId': 4293, 'faultName': 'IP Traffic Capacity Limit'}
fault_61074={'faultId': 61074, 'faultName': 'CRL Update Failure'}
fault_7509={'faultId': 7509, 'faultName': 'EN DSS Setup Failure - Max EN DSS Counter Value reached - No answer from CRM'}
ADDITIONAL_IGNORED_ALARMS=[fault_4297, fault_4654, fault_61642, fault_61652, fault_4655, fault_4293, fault_61074, fault_7509]

# dhcp_server = {
# 	"ip": "10.97.92.243",
# 	"user": "ute",
# 	"password": "UTE.debian12",
#   "note": "Backup DHCP server",
# }

__all__ = ["tl", "dhcp_server", "ADDITIONAL_IGNORED_ALARMS"]
