# Tomo ETL Project

This project contains ETL scripts used in tomography project.



## How to Run
First, make sure to have installed Anaconda then from Anaconda Prompt run

```sh
conda env create -f environment.yml
```

This will create new environment named `tomo` and install all dependencies used in this project.

Then activate the `tomo` environment,

```sh
conda activate tomo
```

and run Jupyter Lab

```sh
jupyter-lab
```

Run the notebook or run Python scripts from the terminal.

## ETL File Monitor

Run 
```sh
python etl-listener.py <path> 
``` 
to monitor path directory which data reside in. It will trigger etl process to its corresponding data product type
and notify its result to a Telegram group chat.