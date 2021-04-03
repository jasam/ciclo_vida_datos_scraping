# Web Scraping sobre Amazon
## Creación de un dataset para Price tracking sobre la oferta de ordenadores y tablets
### Descripción
Este proyeco ha sido desarrollado como solución a *"Práctica 1: Web Scraping"* 
de la asignatura *Tipología y ciclo de vida de los datos*, que pertenece al
Máster de Ciencia de Datos de la Universitat Politècnica de Catalunya.

Se ha realizado *web scraping* sobre el catálogo de Computadoras y Tablets de 
Amazon para crear un conjunto de datos que permita realizar *price tracking* sobre
dichos productos.

### Autores
El proyecto ha sido llevado a cabo por **Javier Samir Rey** e **Irene López Ruiz**.

### Directorios

+ `input_data`. Contiene el archivo `urls_to_scrape.csv` con la URL sobre la que 
empezar el _scraping_.

+ `output_data`. Carpeta donde se guardan los resultados del _scraping_. Contiene 
una carpeta con la fecha en la que se realizó el _scraping_. Dentro de ella se
encuentran:
  
  + `scraped_urls_data.csv`. Archivo CSV con las URL de todos los productos que
  se han analizado.
  
  + `product_complete_data.csv`. Dataset resultante con los datos para realizar
  el *price tracking*.
  
  + `\log`. Carpeta con ficheros JSON auxiliares para realizar el proceso.

+ `python`. Carpeta con la instalación de Python 3.8. Es importante no modificar
esta carpeta.

### Archivos

+ `DocumentacionProyecto.pdf`. Archivo PDF con una descripción detallada del dataset.

+ `config.json`. Archivo con las configuraciones necesarias para realizar el _scraping_.
Para más información, consultar `DocumentacionProyecto.pdf`.

+ `main.py`. Inicia y realiza todo el proceso de _scraping_. Para más información,
consultar `DocumentacionProyecto.pdf`.

+ `interface_class.py`. Clase que implementa métodos auxiliares para realizar las 
peticiones HTTP que se utilizan en el archivo principal `main.py`.

+ `helper_class.py`. Clase que implementa métodos auxiliares de lectura, escritura
y listado de archivos que se utilizan en el archivo principal `main.py`.

+ `start.bat`. Archivo Batch que llama a la ejecución del _scraping_. Para comenzar el
proceso solo se necesita **descargar todo este repositorio** y 
**hacer doble click en este archivo**. Para más información,
consultar `DocumentacionProyecto.pdf`.