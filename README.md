# cf-HelloWorld
A Hello World Cloud Foundry Example written with Python and the Flask Framework


## Requirements
* Cloud Foundry CLI: https://github.com/cloudfoundry/cli/releases
* GIT: https://git-scm.com/downloads

## Instructions
* Clone this repo: `git clone https://github.com/vchrisb/cf-HelloWorld.git`
* Open a shell and change into the `cf-HelloWorld` folder
* Login to Cloud Foundry: `cf login`
  * if using Pivotal Web Services use `api.run.pivotal.io` as the target
* Modify the application name in `manifest.yml` to be unique
* push the application to Cloud Foundry with: `cf push`


## Inject failure

Access `https://<app url>/fail/ready` to fail readiness for a random instance for one minute, or access fail a specific app:

```
curl https://<app url>/fail -X POST "X-Cf-App-Instance":"APP-GUID:INSTANCE-INDEX-NUMBER"
```

To fail liveness access `https://<app url>/fail/live`

## Concourse

This repo also contains a Concourse Pipeline.
