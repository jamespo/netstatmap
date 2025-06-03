#!/bin/env python3

# netstatmap.py (c) 2025 jamespo [at] gmail [dot] com
# USAGE: netstat -pan --inet | netstatmap.py [group by field]

import jc
import sqlite3
import sys

# {'proto': 'udp', 'recv_q': 0, 'send_q': 0, 'local_address': '127.0.0.1', 'foreign_address': '0.0.0.0', 'state': None, 'kind': 'network', 'local_port': '972', 'foreign_port': '*', 'transport_protocol': 'udp', 'network_protocol': 'ipv4', 'local_port_num': 972}
# {'proto': 'tcp', 'recv_q': 0, 'send_q': 0, 'local_address': '0.0.0.0', 'foreign_address': '0.0.0.0', 'state': 'LISTEN', 'kind': 'network', 'local_port': '22', 'foreign_port': '*', 'transport_protocol': 'tcp', 'network_protocol': 'ipv4', 'local_port_num': 22}
#  {'proto': 'tcp', 'recv_q': 0, 'send_q': 0, 'local_address': '127.0.0.1', 'foreign_address': '127.0.0.1', 'state': 'ESTABLISHED', 'kind': 'network', 'local_port': '34699', 'foreign_port': '47392', 'transport_protocol': 'tcp', 'network_protocol': 'ipv4', 'local_port_num': 34699, 'foreign_port_num': 47392}
# {'proto': 'udp', 'recv_q': 0, 'send_q': 0, 'local_address': '0.0.0.0', 'foreign_address': '0.0.0.0', 'state': None, 'program_name': 'avahi-daemon: r', 'kind': 'network', 'pid': 677, 'local_port': '5353', 'foreign_port': '*', 'transport_protocol': 'udp', 'network_protocol': 'ipv4', 'local_port_num': 5353}, {'proto': 'udp', 'recv_q': 0, 'send_q': 0, 'local_address': '0.0.0.0', 'foreign_address': '0.0.0.0', 'state': None, 'program_name': 'avahi-daemon: r', 'kind': 'network', 'pid': 677, 'local_port': '42089', 'foreign_port': '*', 'transport_protocol': 'udp', 'network_protocol': 'ipv4', 'local_port_num': 42089}

db = sqlite3.connect(":memory:")
db_fields = ( "proto", "recv_q", "send_q", "local_address", "foreign_address",
              "state", "program_name", "kind", "pid", "local_port",
              "foreign_port", "transport_protocol", "network_protocol", "local_port_num" )

def create_netstat_tables():
    """create table to store netstat connections"""
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
    """insert netstat connections into table"""
    cursor = db.cursor()
    for conn in netstat_data:
        # set None entry for non-existent fields
        for db_field in db_fields:
            if db_field not in conn:
                conn[db_field] = None
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


def display_netstat(group_by):
    """display netstat results grouped by group_by"""
    cursor = db.cursor()
    if group_by and group_by in db_fields:
        netstat_query = "SELECT %s, count(id), * FROM network_connections GROUP BY %s" % \
            (group_by, group_by)
    else:
        netstat_query = "SELECT * FROM network_connections"
    for row in cursor.execute(netstat_query):
        print(row)


def main():
    try:
        group_by = sys.argv[1]
    except:
        group_by = None
    netstat_in = sys.stdin.read()
    create_netstat_tables()
    netstat_data = jc.parse('netstat', netstat_in)
    insert_netstat(netstat_data)
    display_netstat(group_by)

    # print(data)
    # TODO: put into db


if __name__ == "__main__":
    main()
