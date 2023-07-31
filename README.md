# ctrl-f

### Demo
[![Demo](https://github.com/SemiXQ/ctrl-f/blob/master/demo-screenshot.png)](https://github.com/SemiXQ/ctrl-f/blob/master/demo.mp4)


### Environment Set Up
(1) Create a python 3.9 environment in Anaconda, and the python version I used is python 3.9.13.
```Anaconda prompt
conda create -n py39 python=3.9
conda activate py39
```
(2) If the following libraries are not installed in the environment by default, then install them.
```command line
pip install flask
pip install flask_cors
pip install nltk
pip install sqlalchemy
pip install marshmallow
pip install mysqlclient
```
Here, I didn't use MySQL database in this project, but I decided to keep the codes for connecting MySQL database and building table for future usage if needed. So, I suggests to install `sqlalchemy, marshmallow, mysqlclient` libraries here, in case any issues occur without installing them. Besides, nltk is used to tokenize the sentences in the document.

(3) Run back-end Flask server with the following command, after git cloning this repo.
```command line
cd ctrl-f/back-end/src
flask run
```

(4) Set up and run front-end Angular server. Please make sure that `npm` and `node.js` are installed, and the version of node.js >= 8. I used npm 9.5.1 and node.js v18.16.0.
```command line
npm install -g @angular/cli
npm install rxjs
cd ctrl/frontend
ng serve
```

(5) Open http://localhost:4200/ and play around.
