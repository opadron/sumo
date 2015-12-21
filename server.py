
import os
import os.path

import cherrypy

from girder.api import access
from girder.api.describe import Description, describeRoute
from girder.api.rest import filtermodel, loadmodel, Resource, RestException
from girder.constants import AccessType, ROOT_DIR, STATIC_ROOT_DIR, SettingKey
from girder.utility.model_importer import ModelImporter

DEFAULT_SCRIPT = '\n'.join((
    '',
    'cl <- kmeans(input, num_clusters)',
    'centers <- cl$centers',
    'clusters <- cl$cluster',
    '',
    'cat("CENTERS\n\n")',
    'cat(centers)',
    '',
    'cat("\n\nCLUSTERS\n\n")',
    'cat(clusters)',
    ''))

class Sumo(Resource):
    # NOTE(opadron): 'tools.staticdir.dir' is set in load()
    _cp_config = {'tools.staticdir.on': True,
                  'tools.staticdir.index': 'index.html'}

    def __init__(self, info):
        super(Sumo, self).__init__()
        self.resourceName = 'sumo'
        self.route('POST', (), self.testSumo)

    @access.user
    # @loadmodel(map={'fileId': 'file'}, model='file', level=AccessType.READ)
    # @filtermodel(model='job', plugin='jobs')
    @describeRoute(
        Description('DESCRIPTION')
        .notes('NOTE')
        .param('itemId', 'Item ID.', required=True)
        .param('targetId', 'Destination ID', required=True)
        .param('numClusters', 'Number of clusters to compute',
            required=False, dataType=int, default=2)
        .errorResponse()
        .errorResponse('SOMETHING WENT WRONG', 403))
    def testSumo(self, params):
        self.requireParams(('itemId', 'targetId', 'numClusters'), params)

        itemId = params['itemId']
        targetId = params['targetId']
        numClusters = params['numClusters']

        user = self.getCurrentUser()
        apiUrl = os.path.dirname(cherrypy.url())
        script = cherrypy.request.body.read().decode('utf8') or DEFAULT_SCRIPT

        task = {
            "name": "make_cluster",
            'mode': 'r',
            'script': script,
            "inputs": [{ "name": "input",
                         "type": "table",
                         "format": "r.dataframe"},
                       { "name": "num_clusters",
                         "type": "number",
                         "format": "number",
                         "default": 2 }],
            "outputs": [{ "name": "centers",
                          "type": "r",
                          "format": "object"},
                        { "name": "clusters",
                          "type": "r",
                          "format": "object"}]
        }

        inputs = {
            "input": {
                "format": "csv",
                # 'url': '%s/item/%s/download' % (apiUrl, itemId)

                'data': '''
"x","y"
0.401089309125143,0.0932267834345228
0.0588538927489085,0.0581234692020521
-0.127401240812728,-0.266999401503772
-0.207077822077832,-0.323331148677029
0.152380531030116,0.208295446247806
0.201024355118666,0.361835839219674
-0.0370660419096185,-0.115622642746299
0.667037847254103,0.22328903274202
-0.313307957423401,0.111772877191979
-0.0439664467651717,-0.346324683553122
0.535310760373759,0.482439901625766
-0.163028362098214,-0.40892632238594
0.14667761411311,0.0699416056853418
-0.206802592363292,-0.465371684795881
-0.305905943306259,0.101294798009161
0.187307135540352,0.394613493565055
0.0583214572833207,0.0349721310513246
0.24147269156292,-0.126952404670495
0.0940415830811658,0.382239439875184
0.178903094428267,-0.254466270708026
0.00202836456200715,-0.0178366437087949
-0.0183303121901293,0.261509921295019
0.0239307729374905,-0.516800232005863
-0.196751381351773,-0.286664085571125
0.166967449792933,0.0782822714922736
0.230838218810671,0.53605127682514
-0.0509477233899627,0.349407049616907
-0.0216736804158875,-0.112530234078453
-0.155710520892646,0.831425071378561
-0.133343381225083,-0.0436246868604638
0.247909990111001,-0.578632919994798
0.186647146338878,0.0972689262906421
-0.0196441182421947,0.282679139730599
-0.314388433204179,-0.522240786269683
-0.0706757866833151,-0.147204043562843
0.133381053355749,0.123561866797884
0.395071642749567,-0.656402265609073
-0.0187803910287926,0.0451285131691386
0.457580446266957,-0.284996260361111
-0.122562033478165,0.0873359274658461
0.00220849900987085,0.0262064449999412
-0.056979081845712,-0.303443107195455
0.389015806011756,-1.03843625713284
0.198108713776346,0.380567962832471
-0.294763636594877,-0.412950108836883
0.114734136293663,-0.0408996412261779
0.405885684027256,-0.382097734164595
0.252296550668177,0.338459862277215
-0.049057843615625,0.520087957249213
-0.438713366932163,0.100216052298467
1.06919366569278,1.20127489188804
1.22582383227161,0.952582432867629
1.02257056832182,1.03274117846373
1.12951579664005,0.90265348832187
0.69801118063455,0.821522483863031
0.946859695975808,1.28577756050675
0.620216566933443,1.03209029951595
0.0954957596585334,0.705618641547646
0.830197429234343,1.60277655861088
0.658090116105469,0.889642809433455
0.863391817734969,0.980073377714315
1.12866599469756,0.672687467553859
1.40278627735705,0.764386932099414
1.07033810505701,1.20340497155712
1.07909359141661,0.875384962043568
1.16757441537817,1.15998026280043
0.800802995736284,1.16983264942935
1.04862747737485,0.855098555471798
0.392745579002082,0.844933786157224
0.451197889464629,0.561162247019946
1.01213500983163,1.07333395430149
0.521582509964949,1.54231755698809
0.883336658113926,1.53456125152481
0.719298798855653,0.991031735753554
1.11116971468581,0.934655615839529
1.24535894315702,1.36321819383595
1.3656191580976,1.06844908270417
1.67709430068352,0.277477099293794
0.840354711175984,1.28374116764295
0.891291206527091,0.667731896656437
0.924330237540833,0.72697161958999
1.24593202878701,1.52894486992457
0.833749833129288,1.46091692529246
1.01807215931286,1.44996107546632
1.10772345769112,0.883030496761835
1.162786385515,1.48149456132493
0.913124096551306,0.593812341414097
0.747174502977557,0.818315970582431
1.37676036832639,1.10934555103688
0.920788723860721,1.24571384429887
1.10368858644784,1.02254517990994
0.623675447298549,0.651224530307062
0.679179285262806,1.12039851016465
0.766596728596084,0.683766419325952
1.21712606178002,0.70039297726092
1.30914292651947,1.08871729443401
1.07328483864449,1.60234035064846
1.05938897504172,1.28695888054301
0.855008664364813,0.886226110647941
0.86064269390777,1.01869525701553
'''
            },
            "num_clusters": {
                "format": "number",
                "data": int(numClusters)
            }
        }

        outputs = {
            "centers": { "format": "serialized" },
            "clusters": { "format": "serialized" }
        }

        job = self.model('job', 'jobs').createJob(
            'sumo test', 'romanesco', user=user, handler='romanesco_handler',
            kwargs={
                'task': task,
                'inputs': inputs,
                'outputs': outputs,
                # 'auto_convert': False,
                # 'validate': False
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

def load(info):
    Sumo._cp_config['tools.staticdir.dir'] = os.path.join(
        info['pluginRootDir'], 'static')

    info['apiRoot'].sumo = Sumo(info)

    # Move girder app to /girder, serve sumo app from /
    (
        info['serverRoot'],
        info['serverRoot'].girder
    ) = (
        info['apiRoot'].sumo,
        info['serverRoot']
    )

    info['serverRoot'].api = info['serverRoot'].girder.api
    info['serverRoot'].girder.api

    # events.bind('model.challenge_phase.validate', 'covalic', validatePhase)

