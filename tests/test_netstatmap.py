import sys
import unittest
import sqlite3
from io import StringIO
import netstatmap

class TestNetstatMap(unittest.TestCase):
    def setUp(self):
        # Create a fresh in-memory database for each test
        netstatmap.db = sqlite3.connect(":memory:")

    def test_insert_netstat(self):
        # Test that data is inserted correctly
        netstatmap.create_netstat_tables()
        sample_conn = {
            "proto": "tcp",
            "recv_q": 0,
            "send_q": 0,
            "local_address": "127.0.0.1",
            "foreign_address": "192.168.0.1",
            "state": "ESTABLISHED",
            "program_name": "python",
            "kind": "LISTEN",
            "pid": 1234,
            "local_port": "5000",
            "foreign_port": "42345",
            "transport_protocol": "tcp",
            "network_protocol": "ipv4",
            "local_port_num": 5000
        }
        netstatmap.insert_netstat([sample_conn])
        cursor = netstatmap.db.cursor()
        cursor.execute("SELECT count(*) FROM network_connections")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_display_netstat(self):
        # Test that display_netstat runs without error
        netstatmap.create_netstat_tables()
        sample_conn = {
            "proto": "udp",
            "recv_q": 10,
            "send_q": 5,
            "local_address": "0.0.0.0",
            "foreign_address": "",
            "state": "CLOSEWAIT",
            "program_name": "server",
            "kind": "LISTEN",
            "pid": 4321,
            "local_port": "80",
            "foreign_port": "",
            "transport_protocol": "udp",
            "network_protocol": "ipv4",
            "local_port_num": 80
        }
        netstatmap.insert_netstat([sample_conn])
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            netstatmap.display_netstat("program_name", "program_name")
        except Exception as e:
            self.fail(f"display_netstat raised an exception: {e}")
        finally:
            sys.stdout = sys.__stdout__

    def test_getargs_defaults(self):
        # Test getargs default behavior
        test_args = ["netstatmap.py", "-g", "program_name", "-o", "txt"]
        sys.argv = test_args
        args = netstatmap.getargs()
        self.assertEqual(args.groupby, "program_name")
        self.assertEqual(args.fields, "program_name")
        self.assertEqual(args.output, "txt")

if __name__ == "__main__":
    unittest.main()
