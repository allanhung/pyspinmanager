#!/usr/bin/env python

"""
Pipeline maintaince

Usage:
  pyspinmanager pipeline create (--env=<ENV>) (--app=<APP> | --appkey=<APPKEY>) [-c] [-f] [-g=<GATEEP>]
  pyspinmanager pipeline sync (--src-gate-endpoint=<SRCGATEEP>) (--dst-gate-endpoint=<DSTGATEEP>)

Options:
  -h, --help                              Show this screen.
  --env=<ENV>                             Pipeline environment
  --app=<APP>                             Pipeline application name
  --appkey=<APPKEY>                       Pipeline application name list from key in config
  -c, --create-application                Create application if not exists
  -f, --force-update                      Force create/update pipeline
  -g=<GATEEP>, --gate-endpoint=<GATEEP>   Spinnaker gate endpoint [default http://localhost:8084]
  --src-gate-endpoint=<SRCGATEEP>         Source spinnaker gate endpoint
  --dst-gate-endpoint=<DSTGATEEP>         Destination spinnaker gate endpoint
"""

from docopt import docopt
import os
import pyspinmanager.spin_scripts.common as common
from tqdm import tqdm
import numpy
import yaml

def create(args):
    configFile = common.getConfig(args['--gate-endpoint'])
    config = common.loadconfig(configFile)
    appSetting = config['application_setting']
    pipelineTemplate = os.path.join(common.getTemplateDir(), common.pipelineTemplate)
    appList = config[args['--appkey']] if args['--appkey'] else [args['--app']]
    currentAppList = common.getAppList(args['--gate-endpoint'])
    for app in tqdm(appList):
        if args['--force-update'] or not common.pipelineExists(app, args['--env'], args['--gate-endpoint'], currentAppList):
            if args['--create-application'] and not common.appExists(app, currentAppList):
                common.createApplication(app, appSetting['ownerEmail'], ",".join(appSetting['cloudProvider']), args['--gate-endpoint'])
            pipelineFile = os.path.join(os.getcwd(), "%s_%s.json" % (app, args['--env']))
            common.render_template(common.read_template(pipelineTemplate), common.generate_pipeline_setting(app, args['--env'], config['pipeline_setting']), pipelineFile)
            common.createPipeline(pipelineFile, args['--gate-endpoint'])
        else:
            print("Skip pipeline %s in application %s due to exists!" % ("iac-%s" % args['--env'], app))

def sync(args):
    srcConfigFile = common.getConfig(args['--src-gate-endpoint'])
    dstConfigFile = common.getConfig(args['--dst-gate-endpoint'])
    srcConfig = common.loadconfig(srcConfigFile)
    srcAppInUse = srcConfig.get("appInUse", [])
    dstAppList = common.getAppList(args['--dst-gate-endpoint'])
    dstEnvList = dstconfig["environment"]
    dstAppSetting = dstconfig["application_setting"]
    notExistApp = numpy.setdiff1d(srcAppInUse, dstAppList)
    print('Create non exist application in %s' % args['--dst-gate-endpoint'])
    for app in tqdm(notExistApp):
        common.createApplication(app, srcAppSetting['ownerEmail'], ",".join(srcAppSetting['cloudProvider']), args['--gate-endpoint'])
    print('Create pipeline in %s' % args['--dst-gate-endpoint'])
    for app in tqdm(srcAppInUse):
        for env in dstEnvList:
            pipelineFile = os.path.join(os.getcwd(), "%s_%s.json" % (app, args['--env']))
            common.render_template(common.read_template(pipelineTemplate), common.generate_pipeline_setting(app, args['--env'], config['pipeline_setting']), pipelineFile)
            common.createPipeline(pipelineFile, args['--gate-endpoint'])
    print("Completed!")