<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6992/6992724.png" alt"" width=256>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/python-3.11-blue" alt=""></a>
  <a href="https://pypi.org/project/Django/4.1.2/"><img src="https://img.shields.io/badge/django-4.1.2-green" alt=""></a>
  <a href="https://github.com/unskvort/FMCG-price-monitoring-Django"><img src="https://img.shields.io/badge/version-0.1.0-lightgrey" alt=""></a>
</p>

<p align="center">
<a href="https://github.com/unskvort/FMCG-price-monitoring-Django/actions/workflows/storeCI.yml"><img src="https://github.com/unskvort/FMCG-price-monitoring-Django/actions/workflows/storeCI.yml/badge.svg" alt=""></a>
</p>

## About
Daily monitoring Fast Moving Consumer Goods prices in Russia

## Settings
`/src/dev.env`

## Setup

##### 1. Clone project
```
git clone https://github.com/unskvort/FMCG-price-monitoring-Django.git
```
##### 2. Create database volume
```
docker volume create postgres_store
```
##### 3. Run docker-compose file
```
cd FMCG-price-monitoring-Django/ && docker-compose up --build -d
```
