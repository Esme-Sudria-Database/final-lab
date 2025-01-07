# final-lab

## How to interact with the lab
### Run the lab
- `make start`

### Populate the databases
- `make populate-pg`
- `make populate-mongo`

> You need to run these two commands to have the data into each database

### Stop the lab
- `make stop`

### Get the Jupyter token
- `make get-jupyter-token`

> You need the token to access the Jupyter notebook



---------
ADITIONAL PART :
to generate pgsql data, use `poetry shell` and then `python3 generate_data/company_factory_data.py`