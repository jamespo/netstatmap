#!/bin/env python3

# netstatmap.py (c) 2025 jamespo [at] gmail [dot] com
# USAGE: netstat -pan --inet | netstatmap.py [group by field]

import argparse
import jc
import os
from rich.console import Console
from rich.table import Table
import sqlite3
import sys

DEBUG = os.getenv('NSMDEBUG')

db = sqlite3.connect(":memory:")
# TODO: get via names = [description[0] for description in cursor.description]
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


def display_netstat(group_by, fields):
    """display netstat results grouped by group_by"""
    cursor = db.cursor()
    if group_by:
        netstat_query = """
        SELECT count(id) as num_conns, %s
        FROM network_connections
        GROUP BY %s
        ORDER BY num_conns DESC
        """ % (fields, group_by)
    else:
        netstat_query = "SELECT * FROM network_connections"
    netstat_rows = list(cursor.execute(netstat_query))
    netstat_header = [description[0] for description in cursor.description]
    render_rich_table(netstat_header, netstat_rows)


def render_rich_table(header, rows):
    """display netstat results in console table"""
    table = Table()
    for column in header:
        table.add_column(column)
    for row in rows:
        strrow = [str(field) for field in row]
        #print(strrow)
        table.add_row(*strrow)
    console = Console()
    console.print(table)


def getargs():
    '''parse CL args'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fields", default="program_name,foreign_address",
                        help="fields to return")
    parser.add_argument("-g", "--groupby", default="program_name,foreign_address",
                        help="fields to group by")
    parser.add_argument("-o", "--output", default="txt",
                        choices=['txt', 'graph'], type=str.lower,
                        help="output (txt|graph)")
    args = parser.parse_args()
    return args


def main():
    args = getargs()
    if DEBUG:
        print(args)
    netstat_in = sys.stdin.read()
    create_netstat_tables()
    netstat_data = jc.parse('netstat', netstat_in)
    if DEBUG:
        print(netstat_data)
    insert_netstat(netstat_data)
    display_netstat(args.groupby, args.fields)


if __name__ == "__main__":
    main()
