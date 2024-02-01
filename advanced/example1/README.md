# Using Python Notebooks

## About

We will now recreate the same example [here](https://gitlab-p4n.aip.de/p4nreana/tutorial2023/-/tree/main/intermediate/example2) but using a Jupyter Notebook.

## Structure

The code is the same, so we start from loading the data from an S3 storage, save them in a pandas dataframe, and plot all sources in galactic coordinates.

The resulting figure is saved as an output.

## Running the example on REANA

Since we are using a Jupyter Notebook, the **reana.yaml** file will be a bit different; in particular, we need [papermill](https://papermill.readthedocs.io/en/latest/) which is a tool for parameterizing and executing Jupyter Notebooks.

```
inputs:
  files:
    - remote_data.ipynb
  parameters:
    notebook_in: remote_data.ipynb
    notebook_out: results/output_notebook.ipynb
    output_plot: results/galactic_plot.png
workflow:
  type: serial
  specification:
    steps:
      - environment: 'gitlab-p4n.aip.de:5005/p4nreana/reana-env:py311-astro.9845'
        commands:
          - mkdir -p results
          - papermill ${notebook_in} ${notebook_out} -p output_file ${output_plot} -k python3
outputs:
  files:
    - results/galactic_plot.png
```

As usual, we upload the notebook itself as an input file.  
Then we define three parameters that will be used by papermill, i.e. the input and output notebooks and the path of the output plot.

The environment includes papermill and other astronomy libraries, and the commands make the results directory and call papermill. In this call, the `-p` flag is used to pass parameters to the notebook (check the differences between the input and output), while the `-k` flag avoids confilct between the notebook and reana kernels.

The output file is the plot.

## Running a Jupyter Notebook on REANA

After running the analysis through REANA with the usual commands, we can start a Jupyter Notebook by clicking on the 3 dots and selecting `Open Jupyter Notebook`. After waiting a few seconds, we can click on the new notebook image that should have appeared next to the workflow name.

Notice that this notebook runs in a different environment compared to the one specified in the yaml file, so we might need to reinstall some libraries (see the first commented cell in the notebook).

Alternatively, you can open the notebook from command line and specify a custom image, in this case:

`reana-client open -w adv-example1.1 -i gitlab-p4n.aip.de:5005/p4nreana/reana-env:py311-astro.9845 jupyter`

Notice you need to use the workflow name you chose when running the analysis (here "adv-example1") with the correct tag (the progressive number automatically added by REANA that you can see on the web interface next to the name).

You can open notebooks in both ways for all your workflows.

