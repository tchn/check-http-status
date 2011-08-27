#!/bin/env python
# -*- coding: UTF-8 -*-
#

#from IPython.Shell import IPShellEmbed
import urllib2
import httplib
import re
import sys
import time

# class to handle 30x redirect
class MyRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
		result.status = code
		return result

	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		result.status = code
		return result

# class to write to both stdout and file
class MyOutput(object):
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.log = open(logfile, 'w')

    def write(self, text):
        self.stdout.write(text)
        self.log.write(text)
        self.log.flush()

    def close(self):
        self.stdout.close()
        self.log.close()

def do_request(urls):
    for url in urls:
        req = urllib2.Request(url)
        try:
            res = opener.open(req)
                
            # for 30x response code handled by MyRedirectHanlder
            if hasattr(res, 'status'):
                print req._Request__original, res.status, len(res.read()), res.url

            # for 200 response code
            else:
                print req._Request__original, str(res.code), len(res.read())

        # for 40x response code
        except IOError, e:
            if hasattr(e, 'code'):
                print req._Request__original, str(e.code), len(e.read())

        # for errors caused by corrupt response headers, etc.
        except httplib.BadStatusLine, e:
            print "%s %s" % (req._Request__original, "BadStatusLine!")

def do_timed_request(urls):
    for url in urls:
        req = urllib2.Request(url)
        try:
            time.sleep(float(opts.interval))
            res = opener.open(req)
                
            # for 30x response code handled by MyRedirectHanlder
            if hasattr(res, 'status'):
                print req._Request__original, res.status, len(res.read()), res.url

            # for 200 response code
            else:
                print req._Request__original, str(res.code), len(res.read())

        # for 40x response code
        except IOError, e:
            if hasattr(e, 'code'):
                print req._Request__original, str(e.code), len(e.read())

        # for errors caused by corrupt response headers, etc.
        except httplib.BadStatusLine, e:
            print "%s %s" % (req._Request__original, "BadStatusLine!")

# main program
if __name__ == '__main__':
    import optparse

    ## parse command line
    parser = optparse.OptionParser(
        usage='Usage: %prog [options] urlfile',
        version='2011.7.25',
        conflict_handler = 'resolve'
    )

    parser.add_option('-h', '--help', action='help', help='print help text')
    parser.add_option('-v', '--version', action='version', help='print program version')
    parser.add_option('-i', '--interval', action='store', dest='interval', help='set interval seconds of each request')

    ### options to process output file, tbd
    postprocess = optparse.OptionGroup(parser, 'file processing options')
    postprocess.add_option('-o', '--out', action='store', dest='output_file', help='write stdout to file')
    postprocess.add_option('-s', '--stats', action='store_true', dest='stats', help='show result summary')
    parser.add_option_group(postprocess)

    (opts, args) = parser.parse_args()

    ### process input file
    source_file_name = args[0]
    source_file_handle = open(source_file_name, 'r')
    urls = [line for line in source_file_handle.readlines() if line.strip()]
    print 'Start checking %d urls ...' % len(urls)

    ## output to file as well as stdout
    if opts.output_file:
        sys.stdout = MyOutput(opts.output_file)

    ## instantiate opener
    opener = urllib2.build_opener(MyRedirectHandler())

    ## make requests to each url in urls (with interval seconds if set)
    if opts.interval:
        do_timed_request(urls)
    else:
        do_request(urls)

    sys.stdout = sys.__stdout__
    print 'done!'
