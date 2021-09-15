#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from interactive import iparser
import time

bind = '0.0.0.0:8000'
workers = 4
loglevel = "info"

# Server Hooks
def on_starting(server):
    # make phony calls to interactive parser method just to the grammars are preloaded into memory at startup
    for gr in [r'./bin/eng_sm6.gr',
               r'./bin/wsj02to21.gcg15.prtrm.4sm.fullberk.model'
               ]:
        _ = iparser(gr)
