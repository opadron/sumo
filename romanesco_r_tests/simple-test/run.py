
import romanesco
import celery

celeryapp = celery.Celery('romanesco',
    backend='mongodb://localhost/romanesco',
    broker='mongodb://localhost/romanesco')

simple = {
    "inputs": [],
    "outputs": [{"name": "output", "type": "number", "format": "number"}],
    "script": "output = 4",
    "mode": "r"
}
print romanesco.run(simple)

async_result = celeryapp.send_task("romanesco.run", [simple])

## {
##     "inputs": {
##         "a": {"format": "objectlist", "data": [{"aa": 1, "bb": 2}]},
##         "b": {"format": "objectlist", "data": [{"aa": 3, "bb": 4}]}
##     },
##     "outputs": {
##         "c": {"format": "objectlist.json", "uri": "file://output.json"}
##     }
## })

print async_result.get()

tableio = {
    "inputs": [{"name": "input", "type": "table", "format": "r.dataframe"}],
    "outputs": [{"name": "output", "type": "table", "format": "r.dataframe"}],
    "script": "output = input",
    "mode": "r"
}
print romanesco.run(
    tableio,
    {'input': {'format': 'csv', 'data': 'a,b,c\n1,2,3'}},
    {'output': {'format': 'csv'}})

columnadd = {
    "mode": "r",
    "name": "Add columns",
    "inputs": [
        {
            "format": "r.dataframe",
            "name": "input",
            "type": "table"
        },
        {
            "format": "text",
            "name": "columnOne",
            "type": "string"
        },
        {
            "format": "text",
            "name": "columnTwo",
            "type": "string"
        },
        {
            "format": "text",
            "name": "outputColumn",
            "type": "string"
        }
    ],
    "outputs": [
        {
            "format": "r.dataframe",
            "name": "output",
            "type": "table"
        }
    ],
    "script": """

# Add some columns
output = input
output[,outputColumn] = input[,columnOne] + input[,columnTwo]

"""
}

print romanesco.run(
    columnadd,
    {
        'input': {'format': 'csv', 'data': 'a,b,c\n1,2,3\n4,5,6'},
        'columnOne': {'format': 'text', 'data': 'a'},
        'columnTwo': {'format': 'text', 'data': 'c'},
        'outputColumn': {'format': 'text', 'data': 'x'}
    },
    {'output': {'format': 'objectlist'}}
)

