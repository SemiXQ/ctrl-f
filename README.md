# ctrl-f

### Demo
This demo may not able to play in this page directly, you can click the picture, which will redirect to the link of video, then, you can download it and watch it.
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

If any issues occur, please contact me at xla344@sfu.ca. I'll help fix it.


### RESTful APIs
All the RESTful APIs are defined and implemented in `./back-end/src/app.py`
```python
# initialization of documents shown in front-end webpage
# it will use filename to find the file in ./back-end/src/doc folder
# if file found, it will send the text back in content as response with HTTP 200 status
# if file not found, it will send back a "file not found" error message with HTTP 404 status 
@app.route('/initial_text/<string:filename>', methods=['GET'])

# to search the text in the file
# it will use filename to find the file's dictionary, which is a word -> word's info mapping, in ./back-end/src/doc/docdicts folder
# if file found, it will send the search result as response with HTTP 200 status
# if file not found, it will send back a "file not found" error message with HTTP 404 status
# the json schema with type: {query_text: str, number_of_occurrences: int, occurences: List[Dict[str, object]]}
# the dictionaries in occurences: {"line": int, "start": int, "end": int, "in_sentence": str} 
@app.route('/search_text/<string:filename>/<string:searchContent>', methods=['GET'])

# This is not a RESTful API
# a initialization process executes before all the requests
@app.before_request
def before_request_handler()
```
In this project, I use `jsonify` method to build the json object in response, which will use "application/json" type in Chrome.

### Search and indexing design
**(1) The efficiency consideration for search / indexing (algorithm and data structure):**

In this project, I initialized the `word -> word infos` dictionary for each documents once and stored the dictionaries with a json-like format in files separately. 
The `word infos`includes information of each occurrency of the word in the documentation, where the `info` includes the line index, start column index, end column index and sentence index of the word's location in one occurrency. While, before I started the project, I considered to store the word infos in MySQl database, but I found that the current way to store it was more efficient, as it was `O(1)` time complexity to search by key in dictionary object. Besides, as nosql database also uses json-like data storage format, my current method is easy to transit to using nosql database for large-scale data.

As for searching, I splitted the search text into a list of words, and got their word infos from the dictionary. Then I took a intersect operation on the sets of sentence indexes where words occur, to find out the solution candidates, as the words should occurs together in a sentence. While, in the current code, there is an issue, which I mentioned in the test case 6. I thought that issue could be fixed by using start and end indexes of word to check if they did match and popout the unmatched candidates from the deque or stack (depending on how the candidates were stored in code). I will fix it in the future if I have time.

While, as for indexing, I thought Trie Tree algorithm could help if the scale of data is large. However, based on current data size, I thought the dictionary was efficient enough, as it could be time consuming if we stored the nodes of Trie Tree in the file and loaded it for searching text considering such small data size. (As each node in Trie Tree represents one char, 
if the word is long and the vocabulary is large, then the Trie Tree could have lots of layers and lots of nodes each layer(<= 52 considering upper and lower case without special characters)). I defined the Trie Tree in ./back-end/src/docdict/trietree.py, which is modified based on my previous practice of trie tree in leetcode practice. Due to the time limit, I didn't finish the whole functionalities of trie tree and the method to search considering the last word as a possible prefix. The idea is to use the keys (words) of dictionary to build the trie tree and get possible candidate words with its index in data storage (database or txt file) based on the prefix.

However, for the large data size, I think the most efficient way for searching is to create a 'n-gram -> phrase infos' dictionary directly, if the storage is adequate. While, to reduce the storage demand, it could be good to use semi-tokenization as what BERT does to generate the vocabulary.

**(2) To scale to larger texts:**

To scale to larger texts, we could move the `word -> word info` dictionary into MongoDB and horizontal scaling the database based on demand if the storage is running out.

**(3) To load and manage the texts:**

I'll create and initialize the `word -> word info` dictionary files for original documents in `./back-end/src/doc` folder before all the requests to flask app, 
if the dictionary file doesn't exist in `./back-end/src/doc/docdicts` folder. Then, I will load those dictionary files based on the file name in the request to get search result. The loaded data of dictionary file is a dictionary, which has the following format: `{"word_x": List[Dict[str, object]]}`, 
where the dictionary items inside the list have the following format: `{"line_idx": int, "start": int, "end": int, "sentence_idx":int}`. The list of sentences will be extracted by nltk library from text in original file at the beginning of text searching service.

### If deploy it to cloud service
We can deploy the front-end static file and containerized back-end dockerfile as two separate services onto cloud server. Besides, store the `word -> word info` dictionary into MongoDB, other than current txt file. I am sorry that I don't have much knowledge about how to build microservice on cloud platform, so I cannot get into details at this time, but I plan to learn it later.

### tests
I am sorry that I didn't add CI test cases due to the time. I tested the functionality manually with some test cases instead. The test cases I used are as follows:
``` plain text with a python styled comments
"Now is" # functionality test
"now is" # test for case sensitivity
"now i" # test for considering the last word as a prefix [TODO: feature]
"helloworld" # test if it works correctly when text not found in the file
"California" # test if it works correctly with a single word
"but one" # test if it works correctly without treating two words in the same sentence with different order (or even not as same as the searching phrase) as a candidate result [TODO: fix]
"" # empty search text, expect to return text not found  [TODO: fix] It would be better to be dealed with in another way, if I have time, I'll fix it in the future
" " # similar as above 
```
