# OpenDayLight Controller

We will be using [Opendaylight Nitrogen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.tar.gz) in this project.

![alt text](https://en.wikipedia.org/wiki/OpenDaylight_Project#/media/File:OpenDaylight_logo.png)


To install OpenDayLight Controller run the following command:
```bash
wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.tar.gz
tar –cvzf karaf-0.7.3.tar.gz 
sudo apt-get install openjdk-8-jdk  
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
```

To start OpenDayLight we need to install some features in OpenDayLight. To install mentioned features follow these steps:
```bash
feature:install odl-dluxapps-applications
feature:install odl-restconf-all
feature:install odl-l2switch-all
feature:install odl-openflowplugin-flow-services-rest
```
Then start the ODL controller:
```bash
./karaf-0.7.3/bin/start
# To test ODL functionality
./karaf-0.7.3/bin/status
```
You can access ODL web GUI from this [link](http://localhost:8181/index.html#/login) and the defualt username and password is 'admin'.