# README: TRI-AD Coding Challenge

The solution was implemented in Python.  As such the zip file can be extracted in a local directory and the app can be run from the command line.

## 1. Run from extracted Zip file:

* To Run the app from the command line in the root of the directory where you extracted the zip file:
  * Make sure you have Python 3.8 installed.  To check `python --version` on command line. 
  * Create the virtual environment: `python -m venv env`
  * Install the required packages: `pip install -r requirements.txt`
  * One the command line type: `python LargestValues/LargestValues.py` 
    * This will give you the list of commands or different algorithms you can run:
  ``` 
  $ python LargestValues/LargestValues.py -h
  Usage: LargestValues.py [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  Options:
    -h, --help  Show this message and exit.

  Commands:
    files-on-disk-merge
    memory-merges
    nway-memory-merges
    single-priority-queue
  ```
  * For each command/algorithm you can get more help by using the command name and -h flag, this will give you the different options for the command.  For example:
  ```
  $ python LargestValues/LargestValues.py files-on-disk-merge -h
  Usage: LargestValues.py files-on-disk-merge [OPTIONS]

  Options:
    --url TEXT              URL location for the data file
    --x INTEGER             Number of Largest Values to get from data file
    --chunk_size INTEGER    Size of chunk to retrieve from remote file and
                            process at a time in blocks of 1024 bytes.

    --offset_bytes INTEGER  Bytes to skip in start of input file
    --dir TEXT              Where to save the file segments.
    -h, --help              Show this message and exit.
  ```
  * To run the app using the __files-on-disk-merge__ algorithm, which is the __external sort__ algorithm you can type:
  ```
  $ python LargestValues/LargestValues.py files-on-disk-merge 
  ```
  This will run the algorithm using the default options which are:
  ```
  URL:  https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/  spacemaps_technical_challenge.txt
  X-largest-values:  10
  Chunk size in Blocks of 1024 bytes:  8
  offset_bytes: 500
  dir: out
  ```
  * You can also specify each of the options manually, for example:
  ```
  $ python LargestValues/LargestValues.py files-on-disk-merge --url http://127.0.0.1:5500/test_data/spacemaps_technical_challenge_100.txt --chunk_size 2
  ```
  
  above we specified a local URL and chunk size of 2 blocks.

  * `python LargestValues/LargestValues.py --help` 
  
  for help on usage, shows how to set options

### Testing app:
#### Without integration tests:
* Run the pytest on the app from the command line in the directory where LargestValues.py module is:
  * `pytest --without-integration`
  * `pytest --without-integration -v` for more verbose output

### With integration tests:
* To run with integration tests you must have a local webserver such as Apache or Nginx running. Note http.server from python distrubtion cannot be used, as it does not allow to get the stream in chunks. 
* Test files for the integration reside in /test_data directory. 


## 2. Run app from a Dockerized container:
  * Make sure you have docker installed. To check `docker --version`
  * From the root directory of the app, run the following:
    * `docker build --rm -f Dockerfile -t triadchallenge:latest .`

    This should build the docker image, that you can now run:
* Run the app inside the docker container 
  * Run default configuration, this will give you the various options, same as when you ran the extracted app. 
  
    `docker run --rm -it triadchallenge:latest` 
  * `docker run --rm -it triadchallenge:latest --help` 
    
    for help on usage, shows how to set options
  * For example to run __nway-merge-sort__ algorirhm Run with default options:
    
    `docker run --rm -it triadchallenge:latest nway-memory-merges` 

  * Or you can specify different options, for example if you want to run __single-priority-queue__ algorithm with a specific url and x = 5 with chunk_size of 8 blocks:
  
     `docker run --rm -it triadchallenge:latest single-priority-queue --url https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt --x 5 --chunk_size 8` 

### Testing App inside Docker container
#### Without integration tests
* Run the pytests inside docker container
  * `docker run --rm -it --entrypoint "pytest" triadchallenge:latest --without-integration`

**Note** Cannot run intergration tests inside the container, as it does not include a webserver. 

## Notes on Implementation

* This challenge would be from a class of problems classified as online-optimization. We don't have the entire data available in the start and are streaming the data as we process it.  https://en.wikipedia.org/wiki/Online_algorithm 

* The nature of the data could also dictate which algorithm should be chosen.  Running `value_frequency.py` on the data it seems the given data is somewhat evenly distributed.  So a non-comparison `counting algorithm` can also be considered to sort the data.  However here are mainly interested in returning the X largest values not necessarily sorting and we cannot make guesses of rest of data if it is in billions of records , compared to the 2000 records given.
  
* `single-priority-queue` is the best alogirthm for a very large remote file (N is very large) and a small number of *x-largest values* would be to choose the option.  As we stream the data we keep a Max Heap of x-largest values.  We compare the streaming N numbers with the top of the heap and if it is greater we insert it into the fixed size heap in logX time. So time complexity is NlogX. While space is O(X) which is the size of the heap.
  
  However when x is very small compared and N (lets say 100 compared to Billion) then after some streaming of remote data (lets say 10,000 values) there will be very few merges in the heap. So NlogX will approch N. 

  For more information one can reference : https://en.wikipedia.org/wiki/Continuous_uniform_distribution#Order_statistics
  
* `files-on-disk-merge`, In case of a very large N, let's say 100 billion, and very large X-largest records nearly 10 billion, where both may not fit in RAM the __external-sort__ algorithm , this should be used.  However this assume very large storage or disk space which is larger than total number of records.  But this algorithm can also be parallelized.  

  This external sort uses a Max Priority Queue to merge K sorted file segements.  The Max priority queue points to the top record of each k segement.  It takes the top record and puts it in a result file, then read the next value from that segement and puts in back into Max priority queue.  It keeps repeating until we get the top X values then we can stop.  This is in addition to Timsort (time: MlogM) sorting for each file segment, where M is the number of values in each block.  And if we have K blocks then the first sorting of K segements will take time: KMlogm.  Then we have time: XlogK to get the X largest values.  In the 2nd part the space (RAM) requirement is not more then the number of segements (K).  So total time: KMlogM + XlogK.  And RAM space: K which is just a pointer to each segement. 

* `nway-memory-merges` uses a heapq to merge k-segements (n is k here) at a time.  This also first used Timsort to sort each segement time: O(mlogm) whre m is size of segement.  If N is the total number of elements then merging all segements will be performed in N(logk) time. So total time is O(Nlogm) + O(Nlogk).  While for space we will need to first load all N in RAM and in addition to K which is the size of the heap.  space O(N)+O(K)

* `memory-merges` uses a 2-way iterative merge on k-segments as they are streamed from the remote server.  The incoming chunks (of size m) are first sorted (using pythong default Timsort time: O(mlogm) space: O(m)) and then heapq merged with the resultant chunk (of x-largest values) as it is streamed from remote server.  This saves on local storage space and RAM. For each heap merge time: O(m+x) , space O(m+x), however for all the chunks p, such that m*p = n. So total would be O(mlogm) to sort each chunk and O(n*x) to merge all chunks.  Time: O(mlogm) + O(nx), this is not optimal but x maybe very small compared to n and m andspace requirements is only O(m+x) and it is being merged as the array is being streamed. Also no additional disk space is required.


* Heapsort used in the single priority queue and the is not stable.  So two records / keys having the same value maybe returned in different order.  But since in the requirements output does not need to be in any particular order both answers should be correct. 

* More test coverage needs to be added.  
  
* There seems to be some bug with pytest when comparing results with stdout.  The pytest captured output (capsys.out) is not the same as the output from the actual program.  However there is no error in output from the algorithms (as far as I can tell)

* Exception handling has not been implemented, so some robustness is lacking. Though a program written in python is inherenty more robust. 
  
* Logging has not been implemented.
  
* The remote file is streamed in chunks of 1024 bytes.  This is more robust then trying to read the entire file at once.  However this needs to be further improved by doing restarts on connection breaks from where the file has stopped streaming. 

* For online algorithms of this challenge, this maybe a summary of algorithms that can be used given random data. 
  
**Different cases and algorithms**

| Case | N (Total Records) | X (largest records) | Solution                                                          | Time Complexity  | Space Complexity | Storage | RAM    | Comments |
|------|-------------------|---------------------|-------------------------------------------------------------------|------------------|------------------|---------|--------|----------|
| A    | 100 Billion       | 10 Billion          | Mutli-node External Sort? Hadoop?                                 |                  |                  | 2 TB    | 240 GB |          |
| B    | 10 Billion        | 10 Billion          | External Sort, merge chunks on disk using a heap                  | O(NLogX)         |                  | 240 GB  | 240 GB |          |
| B    | 10 Billion        | 1 Billion           | External Sort, in-memory heapq.merge()                            | O(NlogX)         | O(X)             | 240 GB  | 24 GB  |          |
| C    | 10 Billion        | 100                 | Priority Queue, max heap and compare with each N from file chunks | O(NlogX), O(N)             | O(1)             | 240 GB  | 1 MB   |          |
| D    | 1 Billion         | 1 MIllion           | Priority Queue, Merge sort or Counting sort in memory             | O(NlogX), O(N)   |                  | 24 GB   | 24 MB  |          |
| E    | 1 Billion         | 100                 | Priority Queue, max heap and compare with each N in memory        | O(NlogX) -> O(N) | O(1)             | 24 GB   | 1 MB   |          |
| F    | 1 Million         | 100                 | Priority Queue, max heap and compare with each N in memory        | O(NlogX) -> O(N) |                  |         |        |          |
| G    | 1000              | 5                   | Priority Queue, max heap and compare with each N in memory        | O(NlogX)         |                  |         |        |          |