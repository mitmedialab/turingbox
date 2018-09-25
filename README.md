![alt text](https://github.com/mitmedialab/turingbox/blob/master/front-end/static/img/examineImage.png "Logo Title Text 1")

This is the development repository for the Turing Box platform. Its current form is run locally in a development mode using two flask servers. Futue work would host these servers to make the platform accessible over an internet connection.

# vision
An overview of the Turing Box platform, as well as some examples of the demo in action, as shown [here](https://docs.google.com/presentation/d/1As4fFC1Z7RgT94dumT4iCsqcmibJD2voyk3aif7odWs/edit?usp=sharing). The platform allows users to assemble three types of assets together to form a Box: 1) stimuli (i.e. dataset X, with sensitive attributes Z), 2) algorithms (i.e. a function f : x,z -> y^), and a metric (m : x,z,y,y^ -> R). A box then allows you analyze the context further for instances of algorithmic bias or novel examples of machine behavior. 

![alt text](https://github.com/mitmedialab/turingbox/blob/master/concept/data_flow.png "Logo Title Text 1")

The current platform supports three examples:
1. Computer Vision: The models weights project
2. Risk Assesment: The COMPAS algorithm (replicating the [ProPublica study](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing))
3. Natural Language Processing: Detecting stylistic bias adapted from [Shen and Fratamico et al.] (http://www.fatml.org/media/documents/darling_or_babygirl_stylistic_bias.pdf)

# installation
This codebase was developed and tested for Python 3.6.4. To begin, install the necessary libraries with pip, ```pip3 install -r requirements.txt```.

Make sure [PostgresSQL is installed](https://www.postgresql.org/download/macosx/), as that is the underlying database structure the codebase uses.

### front end
the `front-end` folder contains the code used for the front end of the platform (visualized in the wireframes in `concept/functional_specs.pdf`). It contains a file `app.py` that is used to run the flask server that serves the front end. 
The `templates` folder contains the HTML templates for the different pages enumerated in the wireframes. `static` contains all the static images and graphics for the front end. (`front-end/static/img` contains all the assets for the turing box project thus far). The front end can be accessed by `cd`ing into the `front-end` folder and running

```python app.py```

then going to `http://localhost:8888/` in the browser.

### api
the `api` folder contains the code for the api, backend and databases. It is also a flask server called `application.py`. To access this backend, simply `cd` into the `api` folder and run

```python application.py```

The `api` folder also contains a jupyter notebook for the analysis part of the report page. To access this functionality,  `cd` into the `api` folder and run

```jupyter notebook```

`create_tables.py` should be run once before the user interacts with the platform. This script populates the databases with initial assets for interaction.

# architecture and development decisions
## concept
concept contains identities, design and wireframes used in ideation. 
## tasks
`tasks` is a general folder containing the stimuli, algorithms and intermediary work for the specific tasks.

## front-end
`app.py` is the flask app that does all the heaving lifting. It routes renders data from the api and the user to the templates. `access_api.ipynb` is a jupyter notebook used to debug data flow through the api. 

## api
`application.py` is the flask app that that controlls the flow of data between the front-end and the database. It has 7 methods which allow it route data to the front end:
1. **get_assets()** returns list of all assets in the database
2. **get_box()** given a box id, returns the data for a box to be rendered
3. **get_asset()** returns the information associated with a given asset
4. **ingest_asset()** adds an asset to the codebase
5. **launch_box()** using the stimulus/algorithm/metric triple, it generates a Compas Canonical Dataset on the fly and writes the box to the database.
6. **get_comcon** sends the .csv of the COMPAS Canonical dataset over CORS to render in the front end
7. **inget_comment** allows user to comment on Boxes by adding comment information to the database. 

`controller.py` contains all the core logic for each of these methods, and talks directly to the database. 

`create_tables.py` initializes the correct database schemes and injects initial assets into the correct databases. As discussed above in installation, this should be run as part of the configuration and setup. 

`utils.py` contains auxiliary functions used by the `analyze.ipynb` notebook and contains the core recursive Turing Box logic that allows correct scoping of each individual computation performed. 

`/assets/` contains the information regarding all the assets (mirrored by the databases). See below for how to ingest assets. 

#how to ingest assets
for standardization purposes, assets on Turing Box follow a specific formatting. 

### algorithms 
the python file for each algorithm contains core structure that allows it to be ingested into the Turing Box codebase. Each algorithm inherents the same structure but defines a local function `run_<algorithm_name>(input_array)` that takes as input the numpy array of a single row of a dataset, and performs some computation to yeild y_hat. The core Turing Box protocol will then take care of the rest (i.e. looping over the dataset, storing results, plugging in correct dataset, etc).

### stimulus
All stimulii in TuringBox are defined by the columns X, Z, Y, and Y_hat. 

### metrics
Metrics inherent from the Metric class defined in `api/utils.py`

### comcon 
The Turing Box protocols generate a COMPAS Canonical dataset and write it to this folder. It has a standardized naming convention which the databse uses to serve this dataset to the front end. 

