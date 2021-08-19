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
# from argparse import ArgumentParser
from flask import Flask, Response, request, jsonify

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

def iparser(cp, gr, tokenize=True, kbest=1):

    # Always start the JVM first!
    log('starting up the parser JVM using %s' % cp)
    startup(cp)
    log('---done--- starting up the parser JVM')

    # Convert args from a dict to the appropriate Java class
    opts = getOpts(dictToArgs({{"gr":gr, "tokenize":tokenize, "kbest":kbest}}))

    # Load the grammar file and initialize the parser with our options
    log('loading the grammar %s' % gr)
    parser = loadGrammar(opts)
    log('---done--- loading the grammar')

    def parse(sentence):
        out = StringIO()
        parseInput(parser, opts, inputFile=StringIO(sentence), outputFile=out)
        return str(out)

    return parse

    # Now, run the parser
    print("Enter your input below")
    while True:
        try:
            # User can type into the console and the parse will be written to stdout
            strIn = StringIO(raw_input(" > ")) # yes, this is still 2.7...
            strOut = StringIO()
            parseInput(parser, opts, inputFile=strIn, outputFile=strOut)
            print( strOut.getvalue())
        except EOFError:
            print("\n\nGoodbye. </3")
            break

    # That's all, folks!
    shutdown()


app = Flask(__name__)
registry = {# 'default': iparser(r'./BerkeleyParser-1.7.jar', r'./eng_sm6.gr'),
            # 'fullberk': iparser(r'./BerkeleyParser-1.7.jar', r'./wsj02to21.gcg15.prtrm.4sm.fullberk.model'),
           }

@app.route('/')
def index():
    return Response("hello, world!"), 200


@app.route('/default', methods=['GET', 'POST'])
def default_parser():
    data = request.get_json()
    
    if 'default' not in registry:
        registry['default'] = iparser(r'./BerkeleyParser-1.7.jar', r'./eng_sm6.gr')
    
    return registry['default'](sentence=data['sentence'])


@app.route('/fullberk')
def fullberk_parser():
    
    if 'fullberk' not in registry:
        registry['fullberk'] = iparser(r'./BerkeleyParser-1.7.jar', r'./wsj02to21.gcg15.prtrm.4sm.fullberk.model')

    return registry['default'](sentence=data['sentence'])


if __name__ == '__main__':
    # parser = argparse.ArgumentParser('berkeleyinteract')


    # parser.add_argument('-cp', '--parser', type=str, help='Path to Berkeley Parser', default=r'./BerkeleyParser-1.7.jar')
    # parser.add_argument('-gr', '--grammar', type=str, help='Path to Berkeley Parser', default=r'./eng_sm6.gr')
    # parser.add_argument('-p', '--port', type=int, help='Port for the server to run on', default=5000)
    # args = parser.parse_args()

    # log('Interactive Berkeley Parser received the following arguments: %s' % str(args))

    # This should be the path to the Berkeley Parser jar file
    # cp = r'C:\berkeleyparser\BerkeleyParser-1.7.jar'
    # cp = r'/home/asathe/code/berkeleyinterface/berkeleyParser.jar'
    # Set input arguments
    # See the BerkeleyParser documentation for information on arguments
    # gr = r'./wsj02to21.gcg15.prtrm.4sm.fullberk.model'
    # gr = r'/home/asathe/code/berkeleyinterface/eng_sm6.gr'



    # @app.route('/')
    # def custom_parser():
    #     iparser(cp=args.parser, gr=args.grammar)
    
    app.run(debug=True, port=8000)