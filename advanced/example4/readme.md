# EvapMass - Photoevaporation driven evolution model
## About 
[EvapMass](https://github.com/jo276/EvapMass?tab=readme-ov-file) uses the photo-evaporation driven evolution model of [Owen & Wu 2013,2017](https://academic.oup.com/mnras/article/491/4/5287/5663631?login=true) to predict the minimum masses of mini-Neptunes in multi-planet systems to be consistent with the photo-evaporation model.  
This is an example jupyter notebook which can be run in REANA for the planetary system modelling (`Evap_notebook.ipynb`) .One can find the predicted minimum mass with the mean values of the stellar and planetary parameters or do a Monte Carlo sampling 1000 times and the minimum mass is then given as a 95% upper-limit (unless otherwise stated).
## Structure  
Our Jupyter Notebook(`Evap_notebook.ipynb`)contains the necessary steps for running the "Evapmass" package.Jupyter Notebook automatically includes and utilizes custom-made Python libraries stored in separate Python files (e.g., `OJ12_eff_interpolator.py`, `f_constants.py`, `mass_loss.py`, etc.).
## Running EvapMass on REANA
Since we are using a Jupyter Notebook, the **reana.yaml** file will be a bit different; in particular, we need [papermill](https://papermill.readthedocs.io/en/latest/) which is a tool for parameterizing and executing Jupyter Notebooks.
```
inputs:
  files:
    - OJ12_eff_interpolator.py
    - eff_shape_file.npy
    - f_constants.py
    - mass_loss.py
    - microphysics_params.py
    - planet_structure.py
    - solve_for_masses.py
    - Evap_notebook.ipynb
  parameters:
    notebook_in: Evap_notebook.ipynb
    notebook_out: results/output_notebook.ipynb
    output_plot: results/ProbaDensity_MinimumCoreMass.png
     
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
    - results/ProbaDensity_MinimumCoreMass.png
```
- The input file is the jupyter notebook. we are only iterating it for 100 times to make the execution faster and demonstrate the functionality. You can vary it accordingly as per your accuracy  requirement.


- By defining the three parameters which is used by papermill,ie.the input and output notebooks and the path of the output plot.
- The environment includes papermill and other astronomy libraries, and the commands make the results directory and call papermill. In this call, the `-p` flag is used to pass parameters to the notebook (check the differences between the input and output).
- `-k python3` argument is to explicitly set the kernel to Python 3 when running the Jupyter Notebook using the papermill tool. This ensures that the notebook code is executed in a Python 3 environment, and any dependencies or libraries specified for Python 3 are used during the execution.
- The output will be the produced plot.

## Running a Jupyter Notebook on REANA 
After running the analysis through REANA with the usual commands, we can start a Jupyter Notebook by clicking on the 3 dots and selecting `Open Jupyter Notebook`. After waiting a few seconds, we can click on the new notebook image that should have appeared next to the workflow name.

