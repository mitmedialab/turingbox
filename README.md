![alt text](https://github.com/mitmedialab/turingbox/blob/master/front-end/static/img/logo.png "Logo Title Text 1")

This is the development repository for the Turing Box platform. It is broken into several components.

## concept
concept contains functional specs to be implemented and past identities. 

## front end
the `front-end` folder contains the code used for the front end of the platform (visualized in the wireframes in `concept/functional_specs.pdf`). It contains a file `app.py` that is used to run the flask server that serves the front end. 
The `templates` folder contains the HTML templates for the different pages enumerated in the wireframes. `static` contains all the static images and graphics for the front end. (`front-end/static/img` contains all the assets for the turing box project thus far). The front end can be accessed by `cd`ing into the `front-end` folder and running

```python app.py```

then going to `http://localhost:8888/` in the browser.

## api
the `api` folder contains the code for the api, backend and databases. It is also a flask server called `applicaiton.py`.

## tasks
`tasks` is a general folder containing the stimuli, algorithms and intermediary work for the specific tasks.
