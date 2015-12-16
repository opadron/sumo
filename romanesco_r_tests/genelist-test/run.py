
import celery

celeryapp = celery.Celery('romanesco',
    backend='mongodb://localhost/romanesco',
    broker='mongodb://localhost/romanesco')

value_file_to_heatmap = {
    "name": "value_file_to_heatmap",
    "inputs": [{ "name": "gene_list_values",
                 "type": "table",
                 "format": "r.dataframe"},
               { "name": "gene_list_ordering",
                 "type": "table",
                 "format": "r.dataframe"},
               { "name": "heat_map_type",
                 "type": "string",
                 "format": "text"}],
    "outputs": [{ "name": "gene_list_values_condensed",
                  "type": "table",
                  "format": "r.dataframe"},
                { "name": "heat_map_filename",
                  "type": "string",
                  "format": "text"}],

    "script": open("value_file_to_heatmap.R").read(),

    "mode": "r"
}

kwargs = {
    "inputs": {
        "gene_list_values": {
            "format": "tsv",
            "data": open("GeneList_16_replaced_values.txt").read()
        },
        "gene_list_ordering": {
            "format": "tsv",
            "data": open("e2f3b_16_median.txt").read()
        },
        "heat_map_type": {
            "format": "text",
            "data": "pdf"
        }
    },

    "outputs": {
        "gene_list_values_condensed": {
            "format": "csv"
        },
        "heat_map_filename": {
            "format": "text"
        }
    }
}

async_result = celeryapp.send_task(
    "romanesco.run",
    [value_file_to_heatmap],
    kwargs)

print async_result.get()

