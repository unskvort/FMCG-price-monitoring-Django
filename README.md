<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6992/6992724.png" alt"" width=256>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/python-3.11-blue" alt=""></a>
  <a href="https://pypi.org/project/Django/4.1.2/"><img src="https://img.shields.io/badge/django-4.1.2-green" alt=""></a>
  <a href="https://github.com/unskvort/FMCG-price-monitoring-Django"><img src="https://img.shields.io/badge/version-0.1.3-lightgrey" alt=""></a>
</p>

<p align="center">
<a href="https://github.com/unskvort/FMCG-price-monitoring-Django/actions/workflows/acusCI.yml"><img src="https://github.com/unskvort/FMCG-price-monitoring-Django/actions/workflows/acusCI.yml/badge.svg" alt=""></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## About
Daily monitoring Fast Moving Consumer Goods prices in Russia

## Settings
Settings are in `/src/dev.env` and `/src/prod.env` respectively

## Setup

##### Clone project
```
git clone https://github.com/unskvort/FMCG-price-monitoring-Django.git
```
## Development version
```
cd FMCG-price-monitoring-Django/ && docker-compose -f docker-compose.dev.yml up -d --build
```
## Production version
```
cd FMCG-price-monitoring-Django/ && docker compose \
 -f docker-compose.prod.yml \
 -f docker-compose.override.yml up -d --build
```

##### Links
[minio: s3.localhost:7755](http://s3.localhost:7755)

[grafana: grafana.localhost:7755](http://grafana.localhost:7755)

[prometheus: localhost:9090](http://localhost:9090)

[mainapp: localhost:7755](http://localhost:7755)
