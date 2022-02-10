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

import os
import pickle
import sys
from time import time

from flask import Flask, Response, jsonify, request
from StringIO import StringIO

from berkeleyinterface import (dictToArgs, getOpts, loadGrammar, parseInput,
                               shutdown, startup)

##########################################################################
## Printing for sanity
##########################################################################

START_TIME = time()
def log(message, type='INFO'):
    timestamp = '%.2f' % (time() - START_TIME) 
    print('='*4, type, '@', timestamp, file=sys.stderr, end=' ')
    print(message, file=sys.stderr)


##########################################################################
## Main functionality
##########################################################################

# initialize the flask app
app = Flask(__name__)

# Always start the JVM first!
log('attempting to start up the parser JVM using %s' % r'./bin/BerkeleyParser-1.7.jar')
startup(r'./bin/BerkeleyParser-1.7.jar')
log('---done--- starting up the parser JVM')



@app.route('/')
def index():
    return Response("hello, world!"), 200

@app.route('/default', methods=['GET'])
def default_parser():
    data = request.get_json()
    log('lightweight parser received sentence: ' + data['sentence'])
    parse_method = iparser(r'./bin/eng_sm6.gr')
    parsed = parse_method(data['sentence'])
    log('---done--- lightweight parser produced the following tree: ' + parsed)
    return parsed

@app.route('/fullberk', methods=['GET'])
def fullberk_parser():
    data = request.get_json()
    log('GCG-15 parser received sentence: ' + data['sentence'])
    parse_method = iparser(r'./bin/wsj02to21.gcg15.prtrm.4sm.fullberk.model')
    parsed = parse_method(data['sentence'])
    log('---done--- GCG-15 parser produced the following tree: ' + parsed)
    return parsed


# TODO: write registry to disk somehow?
# if os.path.exists('.cached_parsers.pkl'):
#     log('found pickled parser registry on disk at `.cached_parsers.pkl`. attempting to load.')
#     with open('.cached_parsers.pkl', 'rb') as f:
#         registry = pickle.load(f)
# else:
#     log('no pickled parser registry on disk. initializing empty registry.')
registry = {}


def iparser(gr, registry=registry, tokenize=True, kbest=1):
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

    if gr not in registry:
        # Convert args from a dict to the appropriate Java class
        opts = getOpts(dictToArgs({"gr": gr, "tokenize": tokenize, "kbest": kbest}))

        # Load the grammar file and initialize the parser with our options
        log('loading the grammar %s' % gr)
        parser = loadGrammar(opts)
        log('---done--- loading the grammar')

        # store the loaded parser in registry for future use
        registry[gr] = parser, opts

        # log('dumping parser registry to disk at `.cached_parsers.pkl`.')
        # with open('.cached_parsers.pkl', 'wb') as f:
        #     pickle.dump(registry, f)

    def parse(sentence, gr=gr):
        parser, opts = registry[gr]
        out = StringIO()
        parseInput(parser, opts, inputFile=StringIO(sentence), outputFile=out)
        return out.getvalue()
    return parse


# # make phony calls to interactive parser method just to the grammars are preloaded into memory at startup
# for gr in [r'./bin/eng_sm6.gr',
#            r'./bin/wsj02to21.gcg15.prtrm.4sm.fullberk.model']:
#     _ = iparser(gr)




if __name__ == '__main__':
    # parser = argparse.ArgumentParser('berkeleyinteract')

    # parser.add_argument('-cp', '--parser', type=str, help='Path to Berkeley Parser', default=r'./BerkeleyParser-1.7.jar')
    # parser.add_argument('-gr', '--grammar', type=str, help='Path to Berkeley Parser', default=r'./eng_sm6.gr')
    # parser.add_argument('-p', '--port', type=int, help='Port for the server to run on', default=5000)
    # args = parser.parse_args()

    log('Interactive Berkeley Parser starting')
    app.run(debug=False, port=8000)
