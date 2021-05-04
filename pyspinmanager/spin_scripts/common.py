#!/usr/bin/env python

from jinja2 import Template
import collections
import shlex, subprocess
import yaml
import jq
import json
import os
import re
import pyspinmanager
from copy import deepcopy

pipelineTemplate = 'pipeline.json.j2'

def getTemplateDir():
    return os.path.join(os.path.dirname(pyspinmanager.__file__), "spin_templates")

def render_template(template_str, template_dict, output_file):
    output_str = Template(template_str).render(template_dict) if template_dict else template_str
    # to save the results
    if output_file:
        with open(output_file, "w") as f:
            f.write(output_str+'\n')
    else:
        return output_str

def read_template(filename):
    with open(filename, 'r') as f:
        return '\n'.join(f.read().splitlines())

def convertUnicodeToString(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convertUnicodeToString, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convertUnicodeToString, data))
    else:
        return data

def runCommand(cmd):
    args = shlex.split(cmd)
    return subprocess.check_output(args, stderr=subprocess.STDOUT)
    
def pyjq(inputs, rule):
    return jq.compile(rule).input(inputs).all()

def loadconfig(inputfile):
    with open(inputfile, "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

def saveconfig(data, filename):
    with open(filename, "w") as yamlfile:
        yaml.dump(data, yamlfile)

def getConfig(gatewayEndpoint):
    domain = re.findall('://([\w\-\.]+)', gatewayEndpoint)[0]
    return os.path.join(os.getcwd(), "config_%s.yaml" % domain)

def getAppList(gatewayEndpoint):
    cmd = "spin application list --gate-endpoint %s" % gatewayEndpoint
    apps = json.loads(runCommand(cmd))
    return pyjq(apps, ".[].name")

def appExists(appName, gatewayEndpoint, appList=None):
    if not appList:
        appList = getAppList(gatewayEndpoint)
    return (appName in appList)

def createApplication(appName, ownerEmail, cloudProvider, gatewayEndpoint):
    cmd = "spin application save --application-name %s --owner-email %s --cloud-providers %s --gate-endpoint %s" % (appName, ownerEmail, cloudProvider, gatewayEndpoint)
    common.runCommand(cmd)

def getPipelineList(appName, gatewayEndpoint):
    cmd = "spin pipeline list --application %s--gate-endpoint %s" % (appName, gatewayEndpoint)
    pipelines = json.loads(runCommand(cmd))
    return pyjq(pipelines, ".[].name")

def pipelineExists(appName, env, gatewayEndpoint, appList=None):
    if not appList:
        appList = getAppList(gatewayEndpoint)
    if appName not in appList:
        return False
    pipelineList = getPipelineList(appName, gatewayEndpoint)
    return (("iac-%s" % env) in pipelineList)

def createPipeline(piplineFile, gatewayEndpoint):
    cmd = "spin pipeline save --file %s --gate-endpoint %s" % (pipelineFile, gatewayEndpoint)
    runCommand(cmd)

def generate_pipeline_setting(appName, env, config):
    context = deepcopy(config.get('default', {}))
    context.update(config.get('environment', {}).get(env, {}))
    context.update(config.get('application', {}).get(appName, {}))
    context.update(config.get('application', {}).get(("%s.%s" % (appName, env)), {}))
    context['appName']=appName
    context['env']=env
    if 'gitRepo' not in context.keys():
        context['gitRepo'] = appName
    return context
