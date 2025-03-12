# Challenge Hippo 
____________________

# About the coding exercise
#### GOAL 1: Read data stored in JSON files
Read pharmacy, claims and reverts from the provided files in your entry point.
Some events may not comply with the provided schema. You can use the library of your choice to perform the JSON parsing.
We are only interested in events from Pharmacy dataset.

> The solution for this exercise you can find in the `goal_one.py` file located inside of the folder `src`

#### GOAL 2: Calculate metrics for some dimensions
We want to check how some metrics perform depending on a few dimensions.
Metrics: Count of claims, Count of reverts, Average unit price, Total price
Dimensions: npi, ndc

> The solution for this exercise you can find in the `goal_two.py` file located inside of the folder `src`.

#### GOAL 3: Make a recommendation for the top 2 Chain to be displayed for each Drug.
Make a recommendation for the top 2 Chain to be displayed for each Drug.
The business team wants to understand Drug unit prices per Chain.
To measure performance, we will check the chain that, on average, charges less
per drug unit. Please, write the output to a JSON file.

> The solution for this exercise you can find in the `goal_three.py` file located inside of the folder `src`.

#### GOAL 4: Understand Most common quantity prescribed for a given Drug
Understand Most common quantity prescribed for a given Drug.
The business team wants to know what is the Drug most common quantity
prescribed to negotiate prices discounts. Please, write the output to a JSON file.

> The solution for this exercise you can find in the `goal_four.py` file located inside of the folder `src`.

# The repository's structure

```text
challenge_hippo/
├── analisys/
│ |  └── claims_table_report.html
├── database/
│ |  └── hippo.db
├── input/
│ |  └── claims/
│ |     ├── output-2f620de6-8807-47bd-8034-13eec976c826.json
│ |  └── pharmacies/
│ |     ├── output-09482089-7f1b-4d36-a21f-4652ed460166.csv
│ |  └── reverts/
│ |     ├── output-1d5d70e3-d417-4fea-970d-95c04c64e0d5.json
├── output/
│ |  ├── metrics.json
│ |  ├── most_common_quantities.json
│ |  └── top_chains.json
├── src/
│ |  ├── goal_four.py
│ |  ├── goal_one.py
│ |  ├── goal_three.py
│ |  └── goal_two.py
├── .gitignore
├── eda.py
├── hippo.py
├── LICENSE
├── README.md
├── requirements.txt
└── setup_project.sh
```

**Overview**
- A pasta `analisys`, contém um relatório de análise exploratória dos dados (EDA), gerado pelo script `eda.py`, localizado no diretório raiz do projeto. 
- A pasta `database`, contém um database olap (DuckDB), gerado pelo script `goal_one.py`, localizado no diretório `src`. 
- A pasta `input`, contém os arquivos CSV/JSON. Estes arquivos são derivados do arquivo comprimido `data.tar.gz`, que devem ser movidos ou copiados para dentro desta pasta depois de serem descomprimidos. Estes arquivos são usados pelo script `goal_one.py` para a criação do database que está localizado na pasta `database`. 
- A pasta `output`, contém os arquivos JSON, que são os resultados dos exerícios 2, 3, 4, e são gerados pelos scripts `goal_two.py`, `goal_three.py`, `goal_four.py`. Estes scripts podem ser encontrados dentro do diretório `src`. 
- A pasta `src`, contém os scripts python, criados para resolver os exerícios 1, 2, 3, 4 deste desafio e gerar os resultados esperados que estão localizados dentro do diretório `output`. 


# How does it work

**Get the code repository**:

**Make the script executable**: In your terminal, navigate to the `challenge_hippo` directory (root) and run.

```shell
chmod +x setup_project.sh
```

**Run the script**: Execute the script to create the folders and set up the virtual environment.

```shell
./setup_project.sh
```

This script will:

- Create the analisys, database, input, and output folders.
- Create a virtual environment named `.venv`.
- Activate the virtual environment `.venv`.
- Install python packages.
