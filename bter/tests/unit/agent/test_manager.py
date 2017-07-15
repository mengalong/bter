import ConfigParser
from bter import service

from bter.agent import manager

if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    service.service_prepare(config_file="/Users/mengalong/code/git/bter/etc/bter/bter.ini", conf=conf)

    namespaces = conf.get('DEFAULT', 'namespaces').split(',')
    manager = manager.AgentManager(conf, namespaces)
    for item in manager.extensions:
        print("get the extension:%s" % item.name)
        print item.obj.get_samples()

