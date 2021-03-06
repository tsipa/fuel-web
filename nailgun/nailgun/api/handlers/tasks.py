# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import web

from nailgun.api.handlers.base import BaseHandler
from nailgun.api.handlers.base import content_json
from nailgun.db import db
from nailgun.db.sqlalchemy.models import Task
from nailgun.logger import logger

"""
Handlers dealing with tasks
"""


class TaskHandler(BaseHandler):
    """Task single handler
    """

    fields = (
        "id",
        "cluster",
        "uuid",
        "name",
        "result",
        "message",
        "status",
        "progress"
    )
    model = Task

    @content_json
    def GET(self, task_id):
        """:returns: JSONized Task object.
        :http: * 200 (OK)
               * 404 (task not found in db)
        """
        task = self.get_object_or_404(Task, task_id)
        return self.render(task)

    def DELETE(self, task_id):
        """:returns: JSONized Cluster object.
        :http: * 204 (task successfully deleted)
               * 400 (can't delete running task manually)
               * 404 (task not found in db)
        """
        task = self.get_object_or_404(Task, task_id)
        force = web.input(force=None).force not in (None, u'', u'0')
        if task.status not in ("ready", "error") and not force:
            raise web.badrequest("You cannot delete running task manually")
        for subtask in task.subtasks:
            db().delete(subtask)
        db().delete(task)
        db().commit()
        if force:
            logger.info(
                u"Task with id={0} is forcefully deleted".format(task.id)
            )
        raise web.webapi.HTTPError(
            status="204 No Content",
            data=""
        )


class TaskCollectionHandler(BaseHandler):
    """Task collection handler
    """

    @content_json
    def GET(self):
        """May receive cluster_id parameter to filter list
        of tasks

        :returns: Collection of JSONized Task objects.
        :http: * 200 (OK)
               * 404 (task not found in db)
        """
        user_data = web.input(cluster_id=None)
        if user_data.cluster_id == '':
            tasks = db().query(Task).filter_by(
                cluster_id=None).all()
        elif user_data.cluster_id:
            tasks = db().query(Task).filter_by(
                cluster_id=user_data.cluster_id).all()
        else:
            tasks = db().query(Task).all()
        return map(
            TaskHandler.render,
            tasks
        )
