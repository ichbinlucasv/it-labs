#!/usr/bin/env python3
"""Convert an EVTX file to JSON lines (one flat object per event).

Uses python-evtx (pip install python-evtx). Output fields: EventID,
TimeCreated (UTC, as stored in the file), Computer, Channel, plus every
<Data Name="..."> field from EventData.
Usage: python3 evtx_to_jsonl.py file.evtx > file.jsonl
"""
import json
import sys
import xml.etree.ElementTree as ET

import Evtx.Evtx as evtx

NS = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}

with evtx.Evtx(sys.argv[1]) as log:
    for record in log.records():
        root = ET.fromstring(record.xml())
        system = root.find("e:System", NS)
        out = {
            "EventID": int(system.find("e:EventID", NS).text),
            "TimeCreated": system.find("e:TimeCreated", NS).get("SystemTime"),
            "Computer": system.find("e:Computer", NS).text,
            "Channel": system.find("e:Channel", NS).text,
        }
        for data in root.iterfind("e:EventData/e:Data", NS):
            out[data.get("Name")] = data.text
        print(json.dumps(out))
