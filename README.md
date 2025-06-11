netstatmap
==========

Display summary of network connections

Usage
-----

    sudo netstat -pan --inet | ./netstatmap.py
    sudo netstat -pan --inet6 | ./netstatmap.py

Example output
--------------

    ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
    ┃ num_conns ┃ program_name    ┃ foreign_address ┃
    ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
    │ 3         │ rpc.statd       │ 0.0.0.0         │
    │ 2         │ avahi-daemon: r │ 0.0.0.0         │
    │ 2         │ init            │ 0.0.0.0         │
    │ 1         │ NetworkManager  │ 192.168.4.21    │
    │ 1         │ firefox         │ 34.107.243.93   │
    │ 1         │ master          │ 0.0.0.0         │
    │ 1         │ rpcbind         │ 0.0.0.0         │
    │ 1         │ sshd: /usr/bin/ │ 0.0.0.0         │
    └───────────┴─────────────────┴─────────────────┘
