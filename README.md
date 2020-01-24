# PUMA Job Opening Analysis

## Description
This project was carried out in cooperation with business students of the University of Applied Science Nuremberg.  The goal was to analyze various job openings of the company PUMA. 

The following measures were taken to analyze the job openings:
- A web crawler was set up, which downloaded all data of the job openings and created corresponding screenshots 
- A scraper was implemented, which extracts all necessary information from the downloaded job openings.
- The collected information was saved in an Excel spreadsheet with the help of a Python script

## Setup

### Requirements

* Python 3.6
* Docker:
    * Splash: `docker run --rm -p 8050:8050 scrapinghub/splash`
* Pipenv: `pip install pipenv`

```bash
# after pull:
pipenv install

# enter pipenv shell:
pipenv shell

# install new python packages:
pipenv install <pip-package>
```


### Run a Spider

```bash
cd jobs
# list all available crawlers
scrapy crawl list
```

```bash
cd jobs
# run a crawler
scrapy crawl <name>
```

