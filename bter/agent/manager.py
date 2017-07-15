# coding=utf8
#  Copyright 2017~ mengalong <alongmeng@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import cotyledon
import daiquiri
import itertools

from bter.agent import plugin_base
from stevedore import extension

logger = daiquiri.getLogger(__name__)

# 加载pipeline，区分不同的任务的间隔时间
#
#
class AgentManager(cotyledon.Service):
# class AgentManager():
    def __init__(self, conf=None, namespaces=None):
        self.name = "agent"
        self.conf = conf
        extensions = (self._extensions('poll', namespace, self.conf).extensions
                      for namespace in namespaces)
        self.extensions = list(itertools.chain(*list(extensions)))

    def run(self):
        for item in self.extensions:
            logger.debug("the extension is:%s" % item.name)
            item.obj.get_samples()
        logger.info("start to run")

    @staticmethod
    def _get_ext_mgr(namespace, *args, **kwargs):
        def _catch_extension_load_error(mgr, ep, exc):
            # Extension raising ExtensionLoadError can be ignored,
            # and ignore anything we can't import as a safety measure.
            if isinstance(exc, plugin_base.ExtensionLoadError):
                logger.exception("Skip loading extension for %s", ep.name)
                return

            logger.error("Failed to import extension for %(name)r: %(error)s",
                      {'name': ep.name, 'error': exc})
            if isinstance(exc, ImportError):
                return
            raise exc
        logger.debug("start to load the extensions:%s" % namespace)
        return extension.ExtensionManager(
            namespace=namespace,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds=kwargs,
            on_load_failure_callback=_catch_extension_load_error,
        )

    def _extensions(self, category, agent_ns=None, *args, **kwargs):
        namespace = ('bter.%s.%s' % (category, agent_ns) if agent_ns
                     else 'bter.%s' % category)
        return self._get_ext_mgr(namespace, *args, **kwargs)