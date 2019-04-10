# Puma - Job Offers Scaping

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

