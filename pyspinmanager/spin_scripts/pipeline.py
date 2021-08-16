#!/usr/bin/env python

"""
Pipeline maintaince

Usage:
  pyspinmanager pipeline get (--env=<ENV>) (--app=<APP>) [-o] [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]
  pyspinmanager pipeline create (--env=<ENV>) (--app=<APP> | --appkey=<APPKEY>) [-t=<TEMPLATE>] [-c] [-f] [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]
  pyspinmanager pipeline delete (--env=<ENV>) (--app=<APP> | --appkey=<APPKEY>) [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]
  pyspinmanager pipeline sync (--src-gate-endpoint=<SRCGATEEP>) (--dst-gate-endpoint=<DSTGATEEP>) [--src-cookieheader=<SRCCOOKIEHEADER>] [--dst-cookieheader=<DSTCOOKIEHEADER>]
  pyspinmanager pipeline status (--app=<APP> | --appkey=<APPKEY>) [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]

Options:
  -h, --help                              Show this screen.
  --env=<ENV>                             Pipeline environment
  --app=<APP>                             Pipeline application name
  --appkey=<APPKEY>                       Pipeline application name list from key in config
  -c, --create-application                Create application if not exists
  -f, --force-update                      Force create/update pipeline
  -t=<TEMPLATE>, --template=<TEMPLATE>    Specify pipeline template
  -o, --output                            output to file
  -g=<GATEEP>, --gate-endpoint=<GATEEP>   Spinnaker gate endpoint [default http://localhost:8084]
  --cookieheader=<COOKIEHEADER>           Configure cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2) 
  --src-gate-endpoint=<SRCGATEEP>         Source spinnaker gate endpoint
  --src-cookieheader=<COOKIEHEADER>       Source cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2) 
  --dst-gate-endpoint=<DSTGATEEP>         Destination spinnaker gate endpoint
  --dst-cookieheader=<COOKIEHEADER>       Destination cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2) 
"""

from docopt import docopt
import os
import pyspinmanager.spin_scripts.common as common
from tqdm import tqdm
import numpy
import yaml
import json

def create(args):
    configFile = common.getConfig(args['--gate-endpoint'])
    config = common.loadconfig(configFile)
    appSetting = config['application_setting']
    pipelineTemplate = ""
    if args['--template']:
      pipelineTemplate = os.path.join(os.getcwd(), args['--template'])
    else:
      pipelineTemplate = os.path.join(common.getTemplateDir(), common.pipelineTemplate)
    appList = config[args['--appkey']] if args['--appkey'] else [args['--app']]
    currentAppList = common.getAppList(args['--gate-endpoint'], args['--cookieheader'])
    for app in tqdm(appList):
        if args['--force-update'] or not common.pipelineExists(app, args['--env'], args['--gate-endpoint'], args['--cookieheader'], currentAppList):
            if args['--create-application'] and not common.appExists(app, args['--gate-endpoint'], args['--cookieheader'], currentAppList):
                common.createApplication(app, appSetting['ownerEmail'], ",".join(appSetting['cloudProvider']), args['--gate-endpoint'], args['--cookieheader'])
            pipelineFile = os.path.join(os.getcwd(), "%s_%s.json" % (app, args['--env']))
            common.render_template(common.read_template(pipelineTemplate), common.generate_pipeline_setting(app, args['--env'], config['pipeline_setting']), pipelineFile)
            common.createPipeline(pipelineFile, args['--gate-endpoint'], args['--cookieheader'])
        else:
            print("Skip pipeline %s in application %s due to exists!" % ("iac-%s" % args['--env'], app))

def delete(args):
    configFile = common.getConfig(args['--gate-endpoint'])
    config = common.loadconfig(configFile)
    appList = config[args['--appkey']] if args['--appkey'] else [args['--app']]
    currentAppList = common.getAppList(args['--gate-endpoint'], args['--cookieheader'])
    for app in tqdm(appList):
        if common.pipelineExists(app, args['--env'], args['--gate-endpoint'], args['--cookieheader'], currentAppList):
            common.deletePipeline(app, "iac-%s" % args['--env'], args['--gate-endpoint'], args['--cookieheader'])
        else:
            print("Skip delete pipeline due to application %s or pipeline %s not exists!" % (app, "iac-%s" % args['--env']))

def get(args):
    pipleineContext = common.getPipeline(args['--app'], args['--env'], args['--gate-endpoint'], args['--cookieheader'])
    if args['--output']:
      with open("%s-%s.json" % (args['--app'], args['--env']), "w") as write_file:
        json.dump(pipleineContext, write_file, indent=2)
    else:
        print(json.dumps(pipleineContext, indent=2))

def sync(args):
    srcConfigFile = common.getConfig(args['--src-gate-endpoint'])
    dstConfigFile = common.getConfig(args['--dst-gate-endpoint'])
    srcConfig = common.loadconfig(srcConfigFile)
    srcAppInUse = srcConfig.get("appInUse", [])
    dstAppList = common.getAppList(args['--dst-gate-endpoint'], args['--dst-cookieheader'])
    dstEnvList = dstconfig["environment"]
    dstAppSetting = dstconfig["application_setting"]
    notExistApp = numpy.setdiff1d(srcAppInUse, dstAppList)
    print('Create non exist application in %s' % args['--dst-gate-endpoint'])
    for app in tqdm(notExistApp):
        common.createApplication(app, srcAppSetting['ownerEmail'], ",".join(srcAppSetting['cloudProvider']), args['--dst-gate-endpoint'], args['--dst-cookieheader'])
    print('Create pipeline in %s' % args['--dst-gate-endpoint'])
    for app in tqdm(srcAppInUse):
        for env in dstEnvList:
            pipelineFile = os.path.join(os.getcwd(), "%s_%s.json" % (app, args['--env']))
            common.render_template(common.read_template(pipelineTemplate), common.generate_pipeline_setting(app, args['--env'], config['pipeline_setting']), pipelineFile)
            common.createPipeline(pipelineFile, args['--dst-gate-endpoint'], args['--dst-cookieheader'])
    print("Completed!")

def status(args):
    tmpDict = {}
    configFile = common.getConfig(args['--gate-endpoint'])
    config = common.loadconfig(configFile)
    appList = config[args['--appkey']] if args['--appkey'] else [args['--app']]
    for app in tqdm(appList):
        triggerStatus = common.getPipelineTriggerStatus(app, args['--gate-endpoint'], args['--cookieheader'])
        pipelineStatus = common.getPipelineStatus(app, args['--gate-endpoint'], args['--cookieheader'])
        tmpDict[app] = {}
        for k, v in triggerStatus.items():
            v.update(pipelineStatus.get(k, {"lastExecutiontime": None}))
            tmpDict[app].update({k: v})
    print(yaml.dump(tmpDict))
