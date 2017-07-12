#!/usr/bin/env python

# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the author be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# Copyright (c) 2008 Greg Hewgill http://hewgill.com
#
# This has been modified from the original software.
# Copyright (c) 2011 William Grant <me@williamgrant.id.au>
#
# This has been modified from the original software.
# Copyright (c) 2016 Google, Inc.
# Contact: Brandon Long <blong@google.com>

from __future__ import print_function

import logging
import re
import sys

import dkim

logging.basicConfig(level=10)

if len(sys.argv) != 4:
    print("Usage: arcsign.py selector domain privatekeyfile", file=sys.stderr)
    sys.exit(1)

if sys.version_info[0] >= 3:
    # Make sys.stdin and stdout binary streams.
    sys.stdin = sys.stdin.detach()
    sys.stdout = sys.stdout.detach()

selector = sys.argv[1].encode('ascii')
domain = sys.argv[2].encode('ascii')
privatekeyfile = sys.argv[3]

message = sys.stdin.read()

# Pick a cv status
cv = dkim.CV_None
if re.search('arc-seal', message, re.IGNORECASE):
  cv = dkim.CV_Pass

#try:
sig = dkim.arc_sign(message, selector, domain, open(privatekeyfile, "rb").read(),
               domain + ": none", cv)
for line in sig:
  sys.stdout.write(line)
sys.stdout.write(message)
#except Exception as e:
#    print(e, file=sys.stderr)
    #sys.stdout.write(message)
