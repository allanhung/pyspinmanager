#!/usr/bin/env python

"""
Spinnaker application maintaince

Usage:
  pyspinmanager application scan [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]
  pyspinmanager application create (--appname=<APPNAME>) [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]

Options:
  -h, --help                              Show this screen.
  -g=<GATEEP>, --gate-endpoint=<GATEEP>   Spinnaker gate endpoint [default http://localhost:8084]
  --cookieheader=<COOKIEHEADER>           Configure cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2) 
  --appname=<APPNAME>                     Application name that you want to create with
"""

from docopt import docopt
import os
import pyspinmanager.spin_scripts.common as common
from tqdm import tqdm

def scan(args):
    configFile = common.getConfig(args['--gate-endpoint'])
    config = common.loadconfig(configFile)
    appInUse = config.get("appInUse", [])
    appUnUse = config.get("appUnUse", [])
    appAll = appInUse + appUnUse
    print("scan application from spinnaker api.")
    applist = common.getAppList(args['--gate-endpoint'], args['--cookieheader'])
    for app in tqdm(applist):
        executeCount = common.getAppExcutionCount(app, args['--gate-endpoint'], args['--cookieheader'])
        if executeCount:
            appInUse.append(app)
        else:
            appUnUse.append(app)
    config["appInUse"] = sorted(list(set(appInUse)))
    config["appUnUse"] = sorted(list(set(appUnUse)))
    common.saveconfig(config, configFile)

def create(args):
    configFile = common.getConfig(args['--gate-endpoint'])
    config = common.loadconfig(configFile)
    appSetting = config['application_setting']
    if common.appExists(args['--appname'], args['--gate-endpoint'], args['--cookieheader']):
        print('Application %s already exists!' % args['--appname'])
    else:
        common.createApplication(args['--appname'], appSetting['ownerEmail'], ",".join(appSetting['cloudProvider']), args['--gate-endpoint'], args['--cookieheader'])
