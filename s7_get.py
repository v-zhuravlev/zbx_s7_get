#!/usr/bin/env python3

import argparse
import ipaddress
import snap7


def create_parser():

    helptext = """
    This implements S7 for Zabbix. Add this script to external script dir 
    on Zabbix proxy or Zabbix server.
    snap7 must be installed as well as python-snap7 wrapper.

    expected Zabbix key:
    s7_get.py[plc_IP_address,rack,slot,database,offset,datatype]
    Where datatype=int, float, string or bool
    """

    parser = argparse.ArgumentParser(description=helptext)
    parser.add_argument("ip_address", type=ipaddress.ip_address)
    parser.add_argument("rack", type=int)
    parser.add_argument("slot", type=int)
    parser.add_argument("DB", type=int),
    parser.add_argument("offset", type=str, help="For bool, set as '6.1' to get bit 1 of byte 6")
    parser.add_argument("datatype", metavar="datatype", type=str, 
                        choices=['int', 'float', 'bool', 'string'])
    # For string, you should explicitly set number of bytes to read
    parser.add_argument("bytes_to_read", type=int, nargs="?")
    return parser.parse_args()


if __name__ == "__main__":

    args = create_parser()
    plc = snap7.client.Client()
    # plc.connect("PLC IP address",rack,slot)

    if args.datatype == 'string':
        raise NotImplementedError("string datatype not implemented yet.")
        if not args.bytes_to_read:
            raise argparse.ArgumentError('Please provide number of bytes to read when using string.')

    if args.datatype == 'int':
        bytes_to_read = 2
        offset = int(args.offset)
    elif args.datatype == 'float':
        bytes_to_read = 4
        offset = int(args.offset)
    elif args.datatype == 'bool':
        bytes_to_read = 1
        offset, bit_index = map(int, args.offset.split(".", 2))

    if args.bytes_to_read:
        bytes_to_read = args.bytes_to_read

    plc.connect(str(args.ip_address),
                args.rack,
                args.slot)

    bytes_response = plc.db_read(args.DB,
                                 offset,
                                 bytes_to_read)

    plc.disconnect()

    if args.datatype == 'int':
        response = snap7.util.get_int(bytes_response, 0)
    elif args.datatype == 'float':
        response = snap7.util.get_real(bytes_response, 0)
    elif args.datatype == 'bool':
        response = snap7.util.get_bool(bytes_response, 0, bit_index)
    elif args.datatype == 'string':
        pass
    #   response = snap7.util.get_string(bytes_response, 0, bytes_to_read)
    
    print(response)
