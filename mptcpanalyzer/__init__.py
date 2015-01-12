#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkgutil import extend_path

# from mptcpanalyzer.core import get_basename
import logging
import os


__path__ = extend_path(__path__, __name__)


h = logging.FileHandler(".mptcpanalyzer-" + str(os.getpid()), delay=True)

logger = logging.getLogger(__name__)
logger.addHandler(h)
logger.setLevel(logging.CRITICAL)


def get_basename(fullname, ext):
    return os.path.splitext(os.path.basename(fullname))[0] + "." + ext


def load_fields_to_export_from_file(filename):
    """
    Returns list of fields to export, EOL does not matter
    """
    import json

    with open(filename, newline=None) as input:
        # results = list(csv.reader(inputfile))
        return json.load(input)
    # return results
    raise RuntimeError("error")

# status.run()
# dict to create distinct and understandable csv/sql keys
# print(__path__[0])
# TODO this sounds like a bit of a hack
fields_dict = load_fields_to_export_from_file(__path__[0] + "/mptcp_fields.json")
# {
#     "packetid": "frame.number",
#     "time": "frame.time",
#     "time_delta": "frame.time_delta",
#     "ip4src": "ip.src", "ip4dst": "ip.dst",
#     "ip6src": "ipv6.src", "ip6dst": "ipv6.dst",
#     "srcport": "tcp.srcport",
#     "tcpstream": "tcp.stream",
#     "mptcpstream": "mptcp.stream",
#     "dstport": "tcp.dstport",
#     "sendkey": "tcp.options.mptcp.sendkey",
#     "recvkey": "tcp.options.mptcp.recvkey",
#     # sent in MP_JOIN s
#     "recvtok": "tcp.options.mptcp.recvtok",
#     # sent in MP_JOIN SYN/ACK
#     "sendtruncmac": "tcp.options.mptcp.sendtruncmac",
#     "datafin": "tcp.options.mptcp.datafin.flag",
#     # be careful this outputs subtype0,subtype1,... etc.. so it can introduce "," that
#     # prevents csv parsing if not correctly delimited
#     "subtype": "tcp.options.mptcp.subtype",
#     "tcpflags": "tcp.flags",
#     # mptcp level DATASEQ ...
#     "mapping_dsn": "tcp.options.mptcp.dataseqno",
#     # ... mapped to subflow level seq
#     "mapping_ssn": "tcp.options.mptcp.subflowseqno",
#     "mapping_length": "tcp.options.mptcp.datalvllen",
#     # converts SSN to DSN
#     "ssn_to_dsn": "tcp.options.mptcp.seq2dsn",
#     "master": "tcp.options.mptcp.master",
#     "tcpseq": "tcp.seq",
#     "unmapped": "tcp.options.mptcp.unmapped",
# }


# TODO move away
# plotsDir = "plots"
table_name = "connections"

__all__ = [
    # "Status",
    # "Module", "IntervalModule",
    # "SettingsBase",
    # "formatp",
    "fields_dict",
    "table_name",
    "get_basename",
    # fields_to_export,
]