
import cherrypy
import os

from girder.api import access
from girder.api.describe import Description
from girder.api.rest import Resource
from girder.constants import ROOT_DIR, STATIC_ROOT_DIR
from girder.utility.model_importer import ModelImporter

DEFAULT_FILE = 'file://' + os.path.join(ROOT_DIR, 'plugins', 'sparktest',
                                        'FL_insurance_sample.csv')
DEFAULT_SCRIPT = \
"""
# Filter to get only the records from Clay county
textFile = sc.textFile(file)
clayCounty = textFile.filter(lambda line: 'clay county' in line.lower())

print('TOTAL = %d' % clayCounty.count())
import pprint
pprint.pprint(clayCounty.collect())
"""

class CustomAppRoot(ModelImporter):
    """
    The webroot endpoint simply serves the main index HTML file of covalic.
    """
    exposed = True

    indexHtml = None

    vars = {
        'apiRoot': '/api/v1',
        'staticRoot': '/static',
        'title': 'Covalic'
    }

    def GET(self):
        if self.indexHtml is None:
            self.vars['pluginCss'] = []
            self.vars['pluginJs'] = []

            builtDir = os.path.join(
                STATIC_ROOT_DIR, 'clients', 'web', 'static', 'built', 'plugins')
            plugins = self.model('setting').get(SettingKey.PLUGINS_ENABLED, ())

            for plugin in plugins:
                if os.path.exists(os.path.join(builtDir, plugin,
                                               'plugin.min.css')):
                    self.vars['pluginCss'].append(plugin)
                if os.path.exists(os.path.join(builtDir, plugin,
                                               'plugin.min.js')):
                    self.vars['pluginJs'].append(plugin)
            self.indexHtml = mako.template.Template(self.template).render(
                **self.vars)

        return self.indexHtml



class Sumo(Resource):
    def __init__(self):
        self.resourceName = 'sumo'

        self.route('POST', (), self.testSparkTask)

    def testSparkTask(self, params):
        user = self.getCurrentUser()

        apiUrl = os.path.dirname(cherrypy.url())

        script = cherrypy.request.body.read().decode('utf8') or DEFAULT_SCRIPT

        task = {
            'mode': 'spark.python',
            'script': script,
            'inputs': [{
                'id': 'file',
                'type': 'string',
                'format': 'string'
            }]
        }

        inputs = {
            'file': {
                'mode': 'inline',
                'format': 'string',
                'data': params.get('file', DEFAULT_FILE)
            }
        }

        job = self.model('job', 'jobs').createJob(
            'spark test', 'romanesco', user=user, handler='romanesco_handler',
            kwargs={
                'task': task,
                'inputs': inputs,
                'auto_convert': False,
                'validate': False
            }
        )

        jobToken = self.model('job', 'jobs').createJobToken(job)

        job['kwargs']['jobInfo'] = {
            'method': 'PUT',
            'url': '/'.join((apiUrl, 'job', str(job['_id']))),
            'headers': {'Girder-Token': jobToken['_id']},
            'logPrint': True
        }

        job = self.model('job', 'jobs').save(job)

        self.model('job', 'jobs').scheduleJob(job)

        return self.model('job', 'jobs').filter(job, user)
    testSparkTask.description = (
        Description('Spark+romanesco test')
        .param('body', 'The script to execute', required=False,
               paramType='body', default=DEFAULT_SCRIPT)
        .param('file', 'Path to the text file.', required=False,
               default=DEFAULT_FILE))

def load(info):
    info['apiRoot'].sumo = Sumo()

    # Move girder app to /girder, serve covalic app from /
    info['serverRoot'], info['serverRoot'].girder = (CustomAppRoot(),
                                                     info['serverRoot'])

    info['serverRoot'].api = info['serverRoot'].girder.api
    del info['serverRoot'].girder.api

    # events.bind('model.challenge_phase.validate', 'covalic', validatePhase)

