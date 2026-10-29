__maintainer__ = ""
__email__ = ""

from ute_testline_configuration.ute_config import UTE_CONFIG, Host, FSMr4, IPHY, Pdu

host = [Host(addr="10.92.11.195"), Host(addr="10.92.11.196")]

iphy = [
    IPHY(pdu=Pdu(addr="10.92.11.198", port=1, device="ATEN")),
    IPHY(pdu=Pdu(addr="10.92.11.198", port=4, device="ATEN"), trs_ip="10.0.2.4"),
]

fsm = [
    FSMr4(
        hw_type="FSIP",
        hw_version="A101",
        pdu=Pdu(addr="10.92.11.198", port=2, device="ATEN"),
        top_ip="10.8.17.250",
        fbip1=True,
        fbip2=True,
        fbip3=True,
    ),
    FSMr4(
        hw_type="FSIP",
        hw_version="A101",
        pdu=Pdu(addr="10.92.11.198", port=3, device="ATEN"),
        top_ip="10.8.17.250",
        fbip1=True,
        fbip2=True,
        fbip3=True,
        trs_ip="10.0.1.4",
    ),
]

tl = UTE_CONFIG(fsm=fsm, host=host, iphy=iphy)
node1 = tl[1]
node2 = tl[2]

__all__ = ["tl"]
