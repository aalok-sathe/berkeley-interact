#!/bin/python2.7

# BerkeleyInterface.interactive
# An interactive console to the Berkeley Parser
#
# Author:   Elizabeth McNany <beth@cs.umd.edu>
# Created:  Tue Jul 16 16:40:22 2013 -0400
#
# Copyright (C) 2013 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: interactive.py [] beth@cs.umd.edu $

"""
Basic example demonstrating usage of the interface: Interactive console version!
User can enter utterances repeatedly and exit with ctrl-c
"""

##########################################################################
## Imports
##########################################################################

from __future__ import print_function
from berkeleyinterface import *
from StringIO import StringIO
import sys
from time import time
from flask import Flask, Response, request, jsonify
import pickle

##########################################################################
## Printing for sanity
##########################################################################

START_TIME = time()
def log(message, type='INFO'):
    timestamp = '%.2f' % (time() - START_TIME) 
    print('='*8, type, '@', timestamp, file=sys.stderr, end=' ')
    print(message, file=sys.stderr)


##########################################################################
## Main functionality
##########################################################################

# Allow entering a number for kbest parses to show when running
# kbest = 1
# if len(sys.argv) > 1:
#     kbest = int(sys.argv[1])


# TODO: write registry to disk
registry = {}
def iparser(cp, gr, registry=registry, tokenize=True, kbest=1):
    """returns a function for interactive parsing

    Args:
        cp (str): path to BerkeleyParser jar file
        gr (str): path to grammar file for parsing
        registry (dict): a dictionary mapping parser identifier to a loaded instance
        tokenize (bool, optional): whether to tokenize input. Defaults to True.
        kbest (int, optional): refer to Berkeley Parser documentation. Defaults to 1.

    Returns:
        function: a `parse` function that accepts a sentence and returns parse tree
                  using a parser loaded with the given options.
    """

    if (cp, gr) not in registry:
        # Always start the JVM first!
        log('starting up the parser JVM using %s' % cp)
        startup(cp)
        log('---done--- starting up the parser JVM')

        # Convert args from a dict to the appropriate Java class
        opts = getOpts(dictToArgs({"gr":gr, "tokenize":tokenize, "kbest":kbest}))

        # Load the grammar file and initialize the parser with our options
        log('loading the grammar %s' % gr)
        parser = loadGrammar(opts)
        log('---done--- loading the grammar')

        # store the loaded parser in registry for future use
        registry[cp, gr] = parser, opts

    parser, opts = registry[cp, gr]
    def parse(sentence, parser=parser, opts=opts):
        out = StringIO()
        parseInput(parser, opts, inputFile=StringIO(sentence), outputFile=out)
        return out.getvalue()

    return parse



app = Flask(__name__)

@app.route('/')
def index():
    return Response("hello, world!"), 200

@app.route('/default', methods=['GET'])
def default_parser():
    data = request.get_json()
    log('lightweight parser received sentence: ' + data['sentence'])
    parse_method = iparser(r'./bin/BerkeleyParser-1.7.jar', r'./bin/eng_sm6.gr')
    parsed = parse_method(data['sentence'])
    log('---done--- lightweight parser produced the following tree: ' + parsed)
    return parsed

@app.route('/fullberk', methods=['GET'])
def fullberk_parser():
    data = request.get_json()
    log('GCG-15 parser received sentence: ' + data['sentence'])
    parse_method = iparser(r'./bin/BerkeleyParser-1.7.jar', r'./bin/wsj02to21.gcg15.prtrm.4sm.fullberk.model')
    parsed = parse_method(data['sentence'])
    log('---done--- GCG-15 parser produced the following tree: ' + parsed)
    return parsed


if __name__ == '__main__':
    # parser = argparse.ArgumentParser('berkeleyinteract')

    # parser.add_argument('-cp', '--parser', type=str, help='Path to Berkeley Parser', default=r'./BerkeleyParser-1.7.jar')
    # parser.add_argument('-gr', '--grammar', type=str, help='Path to Berkeley Parser', default=r'./eng_sm6.gr')
    # parser.add_argument('-p', '--port', type=int, help='Port for the server to run on', default=5000)
    # args = parser.parse_args()

    log('Interactive Berkeley Parser starting server')
    app.run(debug=True, port=8000)
