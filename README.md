# coronavirus-json converter

Converts selected zip codes of nychealth's coronavirus-data repo into formatted JSON files.

## Requirements

- Python 3
- Gitpython module
- Selected restaurant data CSV.

## Installation

- Install Python 3
- Install Gitpython using pip. Run the following in cmd/terminal:
    - Windows:
    ```
    py -m pip install gitpython
    ```
    - macOS/Linux:
    ```
    pip3 install gitpython
    ```
- Restaurants's CSV file is located in `data/restaurants_recoded.csv`.
    - Zip codes are in the 2nd column. The zipcode is the last substring when space-delimited.
        - Ex: `123 Fake St. New York, NY 12345` would yield the substring `12345`

## Usage

- Run `main.py`.
- Find your outputted JSON files in `covid_latest.json` and `covid_week_old.json`.