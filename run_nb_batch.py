import papermill as pm
import numpy as np
import multiprocessing
import os

configs = {
    "config_hello_world" : {"msg":"Hello World!","output_label":"hello_world"},
    "config_hello_internet" : {"msg":"Hello Internet!","output_label":"hello_internet"}
}

def run_papermill(notebook,config):
    # get name of notebook
    notebook_name = notebook.split('/')[-1].replace('.ipynb','')
    print('-------------------------------------------------')
    print(config)
    output_label = config["output_label"]
    output_dir = 'papermill_outputs/{}/{}'.format(notebook_name,output_label)
    # make output dir if need to
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = f'{output_dir}/{notebook_name}_{output_label}.ipynb'
    # rename existing file if need to
    if os.path.exists(output_path):
        os.rename(output_path,output_path.replace('.ipynb','_backup.ipynb'))
    # try run notebook using papermill
    try:
        pm.execute_notebook(notebook,output_path,parameters=dict(config=config))
    except Exception as e:
        print(e)

        
if __name__ == '__main__':

    # single or parallel
    run_mode = 'parallel'

    # what notebook to run
    notebook = 'notebooks/example.ipynb'

    # loop over each config
    for config in configs:

        if run_mode == 'parallel':
            p = multiprocessing.Process(
                target=run_papermill,
                args=(
                    notebook,
                    configs[config],
                )
            )
            p.start()
        else:
            run_papermill(notebook,configs[config])

    
    
    