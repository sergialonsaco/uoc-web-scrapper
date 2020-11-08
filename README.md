![Linter](https://github.com/sergialonsaco/uoc-web-scrapper/workflows/Linter/badge.svg?branch=develop)

## Descripción

Esta práctica se ha realizado siguiendo el contenido de la assignatura _Tipología y ciclo de vida de los datos_ del M.Sc de Data Science por la [UOC](https://www.uoc.edu)

## Team

Esta práctica ha sido desarrollada individualmente por Sergi Alonso Badia.

## Code

El código de la práctica se divide principalmente en dos carpetas:
- En la carpeta src encontramos el codigo base para realizar el scrapping.
    - **src/main.py**: Fichero que importa la clase ScrapeQuotes, ejecuta el scrapping y genera un dataset. 
    - **src/scrape.py**: Fichero donde se encuentra la clase ScrapeQuotes con la implementación para el web scrapping.
- En la carpeta **.github/workflows** se encuentran los archivos correspondientes a las pipelines de CI/CD.
    - **lint.yaml**: Continene una pipeline que realiza un Linting sobre los archivos que se añadan
    - **release.yaml**: Ejecuta el codigo del scrapping (src/main.py) y sube el dataset generado (csv) en las Releases de Github.


## Release & Dataset

En esta práctica se ha automatizado la generación del dataset usando las herramientas disponibles en Github.
En concreto, usando [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions) se ha desarrollado un workflow que ejecuta el webscrapping y genera el dataset. 

Una vez generado,
el workflow genera un tag en la main branch la version del codigo (src/__init__.py) y genera una [Release](https://docs.github.com/en/free-pro-team@latest/github/administering-a-repository/managing-releases-in-a-repository), en la qual el workflow se encarga de añadir el dataset con el formato: dataset_<version>.csv 
