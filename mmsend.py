#!/usr/bin/env python3
'''Simple Mattermost send CLI utility written for Python 3
   mmsend.py
   Joaquim Homrighausen <joho@webbplatsen.se>
   TeamYuJo
   2017.10 | 26-Oct-2017

   Guaranteed to contain bugs and stupid constructs.

   There's no magic here, move along.

   Sponsored by WebbPlatsen i Sverige AB, Stockholm Sweden, www.webbplatsen.se
   If you break this code, you own all the pieces :)
 
   You need Python 3 installed on the server

   You need to make this script executable, or run it via the Python interpreter manually

   Any code marked as "CLI" can be removed if you want to embed this somehow

   MIT License
   Copyright (c) 2017 ComXSentio AB; All rights reserved.
  
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
  
   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.
  
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.'''

#CLI begin -------------------------------------------------------------------

import os
import sys
import configparser
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

x_myDir = os.path.dirname (os.path.realpath (__file__))
if (x_myDir == ''):
    sys.stderr.write ("Unable to figure out our own path")
    sys.exit (1)
x_myIni = os.path.join(x_myDir, "mmsend" + ".ini")

# More ugly global variables :)

x_cSection = ""
x_cMode    = ""
x_cURL     = ""
x_cText    = ""
x_cChannel = ""

#Some help, perhaps

def showHelp ():
    sys.stderr.write ("mmsend.py by JoHo\n\n")
    sys.stderr.write ("usage: mmsend [<section>|none] [test|send] [<url>|config] [<text>]\n\n")
    sys.stderr.write ("  section  Use settings from [section] in .ini file\n")
    sys.stderr.write ("  none     Do not use settings from any section in .ini file\n\n")

    sys.stderr.write ("  test     Test, don't actually send anything\n")
    sys.stderr.write ("  send     Do actually send something\n\n")

    sys.stderr.write ("  url      The complete URL for the incoming webhook\n")
    sys.stderr.write ("  config   Read URL from configuration file\n\n")

    sys.stderr.write ("  text     Text to send as message (overrides configuraiton file value)\n")
    sys.stderr.write ("           (use matching quotes for text containing spaces)\n")
    
    sys.exit (1)
    
#Off we go    

if __name__ == '__main__':
    if (len (sys.argv) < 4):
        showHelp ()
    x_cSection = sys.argv [1].strip ();
    x_cMode = sys.argv [2].strip ();
    x_cURL = sys.argv [3].strip ();
    if (len (sys.argv) < 5):
        x_cText = ""
    else:
        x_cText = sys.argv [4].strip ();
    
    if (x_cSection == "none" and x_cURL == "config"):
        sys.stderr.write ("\n{}:\nIf you want to use text from configuration file, you need to specify a section".format (x_myIni))
        sys.exit (2)
    if (x_cMode != "test" and x_cMode != "send"):
        sys.stderr.write ("\nCLI:\nMode must be either 'test' or 'send'");
        sys.exit (2)
    
    if (x_cSection != "none"):
        '''We need the .ini file now'''
        x_cfg = configparser.ConfigParser ()
        rc = x_cfg.read (x_myIni)
        if (not rc or len (rc) == 0):
            sys.stderr.write ("\n{}:\nFile is empty or is not readable".format (x_myIni))
            sys.exit (3)
        if (not x_cfg.has_section (x_cSection)):
            sys.stderr.write ("\n{}:\nSection {} not found".format (x_myIni, x_cSection))
            sys.exit (3)
        if (x_cURL == "config"):
            if (x_cfg.has_option (x_cSection, "url")):
                x_cURL = x_cfg.get (x_cSection, "url")
            else:
                sys.stderr.write ("\n{}:\n'url' option not found in Section {}".format (x_myIni, x_cSection))
                sys.exit (3)
        if (x_cText == ""):
            if (x_cfg.has_option (x_cSection, "text")):
                x_cText = x_cfg.get (x_cSection, "text")
            else:
                sys.stderr.write ("\n{}:\n'text' option not found in Section {}".format (x_myIni, x_cSection))
                sys.exit (3)
        if (x_cfg.has_option (x_cSection, "channel")):
            x_cChannel = x_cfg.get (x_cSection, "channel")

    if (x_cMode == "test"):
        '''Test mode, just show what may have been sent'''
        sys.stderr.write ("Test mode enabled. Not sending anything.\n\n")
        sys.stderr.write ("Section .... {}\n".format (x_cSection))
        sys.stderr.write ("URL ........ {}\n".format (x_cURL))
        sys.stderr.write ("Text ....... {}\n".format (x_cText))
        sys.stderr.write ("Channel .... {}\n".format (x_cChannel))

    #Time to post
    payload = {'text': x_cText}
    if (len (x_cChannel) > 0):
        payload ['channel'] = x_cChannel
    payload_json = json.dumps (payload).encode ('utf-8')

    x_HTTP = Request (x_cURL, payload_json)
    x_HTTP.method = "POST"
    x_HTTP.add_header ('Content-Type', 'application/json; charset=utf-8')
    x_Result = urlopen (x_HTTP).read().decode()
    
    #If you want to check the result, knock yourself out :)
    #print(x_Result)

    sys.exit (0)

#end of file "mmsend.py"
