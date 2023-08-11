#!/bin/sh /etc/rc.common
START=99

start()
{
    mount /tmp/mountd/disk1_part1 /root/USB
    python3 /root/packet_fox.py
}
