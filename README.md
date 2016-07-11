# Query workload analysis tools

A set of scripts that allow us to extract queries from logs, have sql server explain them and then analyze the results.

Built for the SDSS sky survey and SQLShare logs.

## Install

I suggest, you use a virtual environment.

Activate your virtual env and then install freetds and the dependencies.

### First, install freetds

Mac os

```bash
brew install freetds freetype
```

Ubuntu

```bash
sudo apt-get install freetds-dev libfreetype6-dev
```

### Then install the tools

```bash
pip install -r requirements.txt
pip install -e .  # or `python setup.py develop` if you are a developer
```

If you want to use postgres instead of sqlite, you will need to install a driver (such as `psycopg2`).

Create a copy of the config file and set the password.

```bash
cp default.ini default.ini.local
vim default.ini.local
```

## Run

You should be able to run `qwla --help`.

## Views/ copies
Please skip these instructions if you are only interested in SQLShare workload analysis.

To speed up analysis, a few views should be created. Since postgres <9.3 does not support materialized views, we can also make copies. 

```sql
CREATE TABLE logs AS SELECT * FROM everything WHERE db='BestDR5';
ALTER TABLE logs ADD COLUMN has_plan boolean NOT NULL DEFAULT false;

-- logs distinct by query
CREATE TABLE distinctlogs AS SELECT min(id) id, query, count(*) count FROM logs WHERE NOT error GROUP BY query;

-- distinct logs explained (which is a subset of the rows of distinctlogs) with count from distinctlogs
CREATE VIEW explained AS SELECT logs.*, distinctlogs.count FROM logs, distinctlogs WHERE logs.has_plan AND logs.id = distinctlogs.id;

-- view with all logs from bestdr5 but explained
CREATE VIEW logs_explained AS SELECT logs.query, logs.time_start, explained.plan FROM logs, explained WHERE logs.query = explained.query;

-- logs distinct by query template
CREATE VIEW uniqueplans AS SELECT * FROM logs WHERE id in (SELECT min(id) id from explained GROUP BY simple_plan);
```


## Trubleshooting

If you get an error on a mac like `/usr/local/include/ft2build.h:56:10: fatal error: ‘freetype/config/ftheader.h’ file not found`, create a symlink to freetype: `ln -s /usr/local/opt/freetype/include/freetype2 /usr/local/include/freetype`.

## Uses

* [dataset](http://dataset.readthedocs.org/en/latest/) to work efficiently with data
* [SqlAlchemy](http://www.sqlalchemy.org/) to abstract from the database
* [docopt](http://docopt.org/) for the command line interface
* [pymssql](https://github.com/pymssql/pymssql) to connect to ms sql server
