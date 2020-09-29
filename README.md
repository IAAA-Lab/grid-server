# grid-server
Backend for grid-field

## Python libraries

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies from the requirements.txt file.
 It is recommended to create a separate Python3 virtual environment first to avoid complexities and dependencies issues. 

For example, tested in macOS 10.15.4:

- Create a virtual environment: `python3 -m venv ./venv/backend-grid-field-env`. You may need to install the 
`python3-venv` package. Make sure to create your environment inside of a venv or env directory, 
like shown, so git will ignore it.
- Activate the virtual environment: `source ./venv/backend-grid-field-env/bin/activate`.
- Install the requirements in your virtual environment: `pip install -r requirements.txt`.
 You may need to install the `libpq-dev` package in your system.
 
 Besides this, installing GDAL and the python bindings may be a little tricky. For instance, in Ubuntu 20.04 I have needed to install gdal-bin, libgdal-dev, python3-gdal and libgdal26 (maybe not all of those were required) and then the right version of the GDAL package with pip (its version must be the one provided by the command `ogrinfo --version` in your system). But we need to clarify this and provide clearer instructions here.
 
 
## Install, start and stop MongoDB

The GitHub repository includes a docker-compose.yml file that references a docker image with MongoDB and a volume 
for the database data, so the changes in the database are not lost when you start and stop the Docker container.

Install [Docker Compose](https://docs.docker.com/compose/) in your computer. After that, you just need to run 
`docker-compose up` in the same directory as the docker-compose.yml file. This will download the MongoDB 
Docker image, only the first time, will create the volume, again only the first time, and will start the Docker 
container with MongoDB.

To stop the docker container, and remove it and the network, just run `docker-compose down`. This does not remove 
the volume, so the data in the database will not be lost; this is what you normally want. If you run 
`docker-compose down --volumes` then you will remove the volume, so the data in the database will be lost and 
you will have to restore the backup again as shown above for everything to work.

## Configuration & Usage

In the file mongodb_config.py, there are DB connection settings. By default, they point out to the database 
started by docker-compose and it should not be necessary to change it.

The application can be run simply by using executing the manage.py with Python as shown below.
By default, the application will be accessible at <http://127.0.0.1:8000/>.

```python
python manage.py runserver
```

## License
[European Union Public License v1.2](https://eupl.eu/1.2/en/).

Licensor: [Advanced Information Systems Laboratory](https://www.iaaa.es). Aragon Institute for Engineering Research, Universidad Zaragoza, Spain.
