## Overview

A Docker based build environment and UI for building a [DC/OS local universe](https://docs.mesosphere.com/1.10/administering-clusters/deploying-a-local-dcos-universe/#deploying-a-local-universe-containing-selected-packages).

Designed to be run (for now) outside of DC/OS itself. Recommended to run either on your laptop/desktop, or on a [Bootstrap node](https://docs.mesosphere.com/1.10/installing/oss/custom/system-requirements/#bootstrap-node).

Please note: This does not utilise Docker in Docker (dind), it uses sibling containers and connects to your host's Docker daemon using the sock file. If you have an existing Docker container running and registered as `/registry`, it will remove it. If you intend to run this on a jump host or bootstrap server with an existing Docker registry, please check its name.

This is preview quality, it's only been tested using Docker and Chrome on OSX, so if you hit an issue, please raise an issue.

This is a [DC/OS Community](https://dcos.io/community/) project and is not supported or warrantied by Mesosphere.

![screenshot](https://raw.githubusercontent.com/aggress/mesosphere-dcos-universe-builder/master/web/static/images/screenshot.png)


## Usage

### Use Cases

1. You need to provide a subset of the full Catalog/Universe to your users
2. Your DC/OS cluster is air gapped from the Internet, requiring all package assets to be available on the cluster itself

You'll most likely have a bootstrap node or jump host to your DC/OS cluster. If that also has Internet access, then this is the best place to host this tool, as it can pull down the packages and the final build assets may be close to the target DC/OS cluster, which'll cut down on the time it'll take to transfer them over.

Once the assets are built and if your network allows, you could `curl` them directly from your masters using the DC/OS cli.

`$ dcos node ssh --master-proxy --leader "curl -o /tmp/local-universe.tgz http://<bootstrap node>:5001/local-universe.tar.gz"`

If that option is not possible, then it can be run on any machine like your laptop/desktop with Docker running, which is supported on all major OSes.

### Prerequisites

- Git
- Docker daemon active

1. `$ git clone git@github.com:aggress/mesosphere-dcos-universe-builder.git`
1. `$ cd mesosphere-dcos-universe-builder`
1. Run the Docker container `$ scripts/run.sh`
1. Open `http://127.0.0.1:5001` in your web browser. scripts/run.sh can be amended to change the IP the UI is available on, if running on an external server, otherwise you can SSH port forward to access it
1. Select the DC/OS version and packages you wish to add and build
1. Click on `BUILD`, note build time will vary depending on the number of packages
1. Download the presented `local-universe.tgz` which could be between 500MB-3GB, plus the systemctl service files
1. Either click `SHUTDOWN` or run `$ docker kill /builder`
1. scp to your DC/OS masters' /tmp dir
1. Publish to your target DC/OS cluster. I use a simple [Ansible playbook](https://github.com/aggress/mesosphere-dcos-toolbox/blob/master/ansible/playbooks/deploy-local-universe-from-masters.yaml). See Publishing.


## Design

The goal was to provide a nice usable UI for selecting packages, build the local-universe, then a simple Ansible playbook to pubish, thereby removing many many manual steps.

The UI's based around [https://selectize.github.io/selectize.js/](selectize.js) which provides a rich drop down box for choosing packages, this is populated from the Universe itself so is always up to date.

Typing the first few characters of a package name returns a subset of the entire Universe list, allowing you to search for packages easily. It's best used if you type the name then the first number of the version, like `spark:2` as that'll return the latest versions. 

### Components

- Docker
- Git
- Flask
- Bash
- Python
- html/css/js
- selectize.js
- jquery

### Flow

1. run.sh helper script executes
2. Git clones the [DC/OS universe](https://github.com/mesosphere/universe)
3. make base
3. builder-list.py traverses the universe repository to make a list of every package
4. Inject it into the selectize drop down box
5. Flask runs `builder-web.py`
6. index.html rendered from base.html template and published on `127.0.0.1:5001`
7. `selectize.js` makes the package selection shiny
8. Build button POSTs back to `builder-web.py /`
9. Extracts the packages from the MultiDict into a comma separate string
10. Calls `run.sh make-universe` to build the local universe
11. Outputs assests including `local-universe.tgz`
12. `result.html` displays links to the assets to download

## Publishing

### Requires

- Ansible installed locally
- Direct SSH access to DC/OS nodes

This automates the [steps documented here](https://docs.mesosphere.com/1.10/administering-clusters/deploying-a-local-dcos-universe/)

1. `$ git clone git@github.com:aggress/mesosphere-dcos-toolbox.git`
1. `$ cd mesosphere-dcos-toolbox/ansible`
1. Edit `hosts` and replace `master` with a list of your DC/OS masters, each on a new line
1. Run `$ ansible-playbook -i hosts -b -u <username> playbooks/deploy-local-universe-from-masters.yaml`

## Todo

1. Better validation on failure, if the build fails, you'll need to check the Docker stdout
2. Change /registry to something safer
3. A css loader/spinner rather than relying on the browser waiting notification in the status bar
4. Test running on DC/OS itself as a Marathon task
5. Replace run.sh with Python 
6. Testing on other browsers, OSes