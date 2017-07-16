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


from concurrent import futures
from futurist import periodics

from bter.agent import plugin_base
from bter import pipeline
from bter import publish
from bter import utils
from stevedore import extension

logger = daiquiri.getLogger(__name__)

# 加载pipeline，区分不同的任务的间隔时间
#
#


class AgentManager(cotyledon.Service):
    def __init__(self, conf=None, namespaces=None):
        self.name = "agent"
        self.conf = conf
        self.conf_path = self.conf.get('DEFAULT', "conf_path")
        extensions = (self._extensions('poll', namespace, self.conf).extensions
                      for namespace in namespaces)
        self.extensions = list(itertools.chain(*list(extensions)))

        cfg_file = self.conf_path + "/pipeline.yaml"
        # TODO(mengalong): polling_manager 初始化的时候需要支持publisher的初始化
        self.polling_manager = pipeline.PipeLineManager(self.conf, cfg_file)

    def run(self):
        for item in self.extensions:
            logger.debug("the extension is:%s" % item.name)
            item.obj.get_samples()
        logger.info("start to run")

        self.start_polling_task()

    def start_polling_task(self):
        data = self.setup_polling_tasks()
        logger.debug("polling tasks is:%s" % data)

        self.polling_periodics = periodics.PeriodicWorker.create(
            [], executor_factory=lambda:
            futures.ThreadPoolExecutor(max_workers=10))

        for interval, polling_task in data.items():
            delay_time = 1

            @periodics.periodic(spacing=interval, run_immediately=False)
            def task(running_task):
                self.interval_task(running_task)

            # TODO(mengalong)：polling_task[0][0] 需要修改为适配模式，
            # 按照list进行遍历执行
            utils.spawn_thread(utils.delayed, delay_time,
                               self.polling_periodics.add, task,
                               polling_task)

        utils.spawn_thread(self.polling_periodics.start, allow_empty=True)

    def interval_task(self, tasks):
        # NOTE(sileht): remove the previous keystone client
        # and exception to get a new one in this polling cycle.
        # for task_obj in task:
        #     task.obj.get_samples()
        for task_obj in tasks:
            self.do_single_task(task_obj)

    def do_single_task(self, task):
        task_obj = task[0]
        task_source = task[1]
        task_publisher = task[2]

        logger.debug("task source is:%s" % task_source)
        logger.info("start to get data:%s" % task_obj.name)

        for samples in task_obj.obj.get_samples():
            task_publisher.publish_driver.record_metering_sample(samples)

    def setup_polling_tasks(self):
        polling_tasks = {}
        for source in self.polling_manager.sources:
            polling_task = None
            logger.debug("current source is:%s" % source)
            for pollster in self.extensions:
                if pollster.name in source.get('meters'):
                    polling_task = polling_tasks.get(source.get('interval'))
                    if not polling_task:
                        polling_task = []
                        polling_tasks[source.get('interval')] = polling_task
                    publisher_url = source.get('publishers')[0]

                    publisher_obj = publish.PublisherManager(self.conf,
                                                             publisher_url)
                    polling_task.append((pollster, source, publisher_obj))
        return polling_tasks

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
