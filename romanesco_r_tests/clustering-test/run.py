
import os.path
import celery
import romanesco

celeryapp = celery.Celery('romanesco',
    backend='mongodb://localhost/romanesco',
    broker='mongodb://localhost/romanesco')

make_cluster = {
    "name": "make_cluster",
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
                  "format": "object"}],

    "script": open("make_cluster.R").read(),
    "mode": "r"
}

kwargs = {
    "inputs": {
        "input": {
            "format": "csv",
            "data": open("clusters.csv").read()
            # "path": os.path.abspath("clusters.csv")
        },
        "num_clusters": {
            "format": "number",
            "data": 2
        }
    },

    "outputs": {
        "centers":  { "format": "serialized" },
        "clusters": { "format": "serialized" }
    }
}

async_result = celeryapp.send_task(
    "romanesco.run",
    [make_cluster],
    kwargs)

print async_result.get()

