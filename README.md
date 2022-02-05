# pyspinmanager
Maintain spinnaker application and pipeline

## Install
### Prerequirement
Install [spinnaker cli](https://spinnaker.io/setup/spin/)

### Install python module
```bash
pip install git+https://github.com/allanhung/pyspinmanager.git
```

### Run with docker
```bash
docker build -t spin .
docker run -d --name=spin --rm -v $(pwd):/apps spin
docker exec -ti spin bash
```

## Usage
### Configure pyspinmanager
The configuration file doesn't exist yet, after you installpyspinmanager. You need to create it in your working dir.
example:
```bash
environment:
- develop
- staging
- production

application_setting:
  ownerEmail: owner@personal.com
  cloudProvider:
  - kubernetes

pipeline_setting:
  default:
    artifactAccount: artifactoryAccount
    gitOwner: personal
    helmRepository: https://myhelm.repo.com/repository
    maintainer: maintainer
    notifyEmailAddr: alert@personal.com
    spinnakerUri: https://spinnaker.personal.com
  environment:
    develop:
      branch: master
      provider: develop
      releaseName: develop-release
      triggerEnabled: "true"
      valueFile: values.develop.yaml
    staging:
      branch: tags
      provider: staging
      releaseName: staging-release
      triggerEnabled: "true"
      valueFile: values.staging.yaml
    production:
      branch: tags
      provider: production
      releaseName: production-release
      triggerEnabled: "false"
      valueFile: values.production.yaml
  application:
    app1:
      releaseName: app1-release
    app2.develop:
      releaseName: app2-release
```
There are three levels in pipeline_setting. Application setting will override environment setting and default setting.
Environment setting will override default setting.
Here are the outputs
* app1 develop setting:
```bash
appName: app1
artifactAccount: artifactoryAccount
branch: master
env: develop
gitOwner: personal
gitRepo: app1
helmRepository: https://myhelm.repo.com/repository
maintainer: maintainer
notifyEmailAddr: alert@personal.com
provider: develop
releaseName: app1-release
spinnakerUri: https://spinnaker.personal.com
triggerEnabled: 'true'
valueFile: values.develop.yaml
```
* app1 staging setting:
```bash
appName: app1
artifactAccount: artifactoryAccount
branch: tags
env: staging
gitOwner: personal
gitRepo: app1
helmRepository: https://myhelm.repo.com/repository
maintainer: maintainer
notifyEmailAddr: alert@personal.com
provider: staging
releaseName: app1-release
spinnakerUri: https://spinnaker.personal.com
triggerEnabled: 'true'
valueFile: values.staging.yaml
```
* app2 develop setting:
```bash
appName: app2
artifactAccount: artifactoryAccount
branch: master
env: develop
gitOwner: personal
gitRepo: app2
helmRepository: https://myhelm.repo.com/repository
maintainer: maintainer
notifyEmailAddr: alert@personal.com
provider: develop
releaseName: app2-release
spinnakerUri: https://spinnaker.personal.com
triggerEnabled: 'true'
valueFile: values.develop.yaml
```
* app2 staging setting:
```bash
appName: app2
artifactAccount: artifactoryAccount
branch: tags
env: staging
gitOwner: personal
gitRepo: app2
helmRepository: https://myhelm.repo.com/repository
maintainer: maintainer
notifyEmailAddr: alert@personal.com
provider: staging
releaseName: staging-release
spinnakerUri: https://spinnaker.personal.com
triggerEnabled: 'true'
valueFile: values.staging.yaml
```

### Generate application list by scan spinnaker server
```bash
pyspinmanager application scan -g http://localhost:8084
```
It will generate application list into config with section appInUse and appUnUse.
* appInUse: application pipeline has been excuted before.
* appUnUse: application pipeline never been excuted.
 
### Create pipeline
* create pipeline with given application name (--app)
* create pipeline with given application list from applist config (--applist)
```bash
Usage:
  pyspinmanager pipeline create (--env=<ENV>) (--app=<APP> | --applist=<APPLIST>) [-t=<TEMPLATE>] [-c] [-f] [-g=<GATEEP>] [--cookieheader=<COOKIEHEADER>]

Options:
  -h, --help                              Show this screen.
  --env=<ENV>                             Pipeline environment
  --app=<APP>                             Pipeline application name
  --applist=<APPLIST>                     Pipeline application name list from applist in config
  -c, --create-application                Create application if not exists
  -f, --force-update                      Force create/update pipeline
  -t=<TEMPLATE>, --template=<TEMPLATE>    Specify pipeline template
  -g=<GATEEP>, --gate-endpoint=<GATEEP>   Spinnaker gate endpoint [default http://localhost:8084]
  --cookieheader=<COOKIEHEADER>           Configure cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2)
```  

### Sync pipeline
* It will get application list (appInUse) from source spinnaker server and create pipeline under the application in destination spinnaker server with destination server config.
```bash
pyspinmanager pipeline sync (--src-gate-endpoint=<SRCGATEEP>) (--dst-gate-endpoint=<DSTGATEEP>) [--src-cookieheader=<SRCCOOKIEHEADER>] [--dst-cookieheader=<DSTCOOKIEHEADER>]

Options:
  --src-gate-endpoint=<SRCGATEEP>         Source spinnaker gate endpoint
  --src-cookieheader=<COOKIEHEADER>       Source cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2)
  --dst-gate-endpoint=<DSTGATEEP>         Destination spinnaker gate endpoint
  --dst-cookieheader=<COOKIEHEADER>       Destination cookie headers for gate client as comma separated list (e.g. key1=value1,key2=value2)
```

### Reference
* [Okta SAML to authenticate with Spinnaker](https://github.com/spinnaker/spin/pull/205)
