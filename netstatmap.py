#!/bin/env python3

# netstatmap.py (c) 2025 jamespo [at] gmail [dot] com
# USAGE: netstat -pan --inet | netstatmap.py

import jc
import sqlite3
import sys

# {'proto': 'udp', 'recv_q': 0, 'send_q': 0, 'local_address': '127.0.0.1', 'foreign_address': '0.0.0.0', 'state': None, 'kind': 'network', 'local_port': '972', 'foreign_port': '*', 'transport_protocol': 'udp', 'network_protocol': 'ipv4', 'local_port_num': 972}
# {'proto': 'tcp', 'recv_q': 0, 'send_q': 0, 'local_address': '0.0.0.0', 'foreign_address': '0.0.0.0', 'state': 'LISTEN', 'kind': 'network', 'local_port': '22', 'foreign_port': '*', 'transport_protocol': 'tcp', 'network_protocol': 'ipv4', 'local_port_num': 22}
#  {'proto': 'tcp', 'recv_q': 0, 'send_q': 0, 'local_address': '127.0.0.1', 'foreign_address': '127.0.0.1', 'state': 'ESTABLISHED', 'kind': 'network', 'local_port': '34699', 'foreign_port': '47392', 'transport_protocol': 'tcp', 'network_protocol': 'ipv4', 'local_port_num': 34699, 'foreign_port_num': 47392}
# {'proto': 'udp', 'recv_q': 0, 'send_q': 0, 'local_address': '0.0.0.0', 'foreign_address': '0.0.0.0', 'state': None, 'program_name': 'avahi-daemon: r', 'kind': 'network', 'pid': 677, 'local_port': '5353', 'foreign_port': '*', 'transport_protocol': 'udp', 'network_protocol': 'ipv4', 'local_port_num': 5353}, {'proto': 'udp', 'recv_q': 0, 'send_q': 0, 'local_address': '0.0.0.0', 'foreign_address': '0.0.0.0', 'state': None, 'program_name': 'avahi-daemon: r', 'kind': 'network', 'pid': 677, 'local_port': '42089', 'foreign_port': '*', 'transport_protocol': 'udp', 'network_protocol': 'ipv4', 'local_port_num': 42089}

db = sqlite3.connect("file::memory")


def create_netstat_tables():
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS network_connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proto TEXT,
        recv_q INTEGER,
        send_q INTEGER,
        local_address TEXT,
        foreign_address TEXT,
        state TEXT,
        program_name TEXT,
        kind TEXT,
        pid INTEGER,
        local_port TEXT,
        foreign_port TEXT,
        transport_protocol TEXT,
        network_protocol TEXT,
        local_port_num INTEGER
    )
    """)


def insert_netstat(netstat_data):
    cursor = db.cursor()
    for conn in netstat_data:
        print('pid: %s' %  conn['pid'])  # DEBUG
        # TODO: set None entry for non-existent fields
        cursor.execute("""
        INSERT INTO network_connections (
        proto, recv_q, send_q, local_address, foreign_address,
        state, program_name, kind, pid, local_port,
        foreign_port, transport_protocol, network_protocol, local_port_num
        ) VALUES (
        :proto, :recv_q, :send_q, :local_address, :foreign_address,
        :state, :program_name, :kind, :pid, :local_port,
        :foreign_port, :transport_protocol, :network_protocol, :local_port_num
        )
        """, conn)
    db.commit()


def main():
    netstat_in = str(sys.stdin.read())
    create_netstat_tables()
    netstat_data = jc.parse('netstat', netstat_in)
    insert_netstat(netstat_data)

    # print(data)
    # TODO: put into db


if __name__ == "__main__":
    main()
