__maintainer__ = ""
__email__ = ""

from ute_testline_configuration.ute_config import UTE_CONFIG, Host, Pdu, FSMr4, IPHY

host = [Host(addr="10.92.11.101")]

fsm4 = [
    FSMr4(
        hw_type="FSIP",
        hw_version="A101",
        pdu=Pdu(addr="10.92.11.107", port=2, device="ATEN"),
        top_ip="10.8.17.250",
        fbip1=True,
        fbip2=False,
        fbip3=False,
    )
]

iphy = [IPHY(pdu=Pdu(addr="10.92.11.107", port=1, device="ATEN"))]

tl = UTE_CONFIG(host=host, fsm=fsm4, iphy=iphy)

__all__ = ["tl"]
