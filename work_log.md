**Work Log for TRI-AD challenge**

The idea is to:
1. **Take in command line inputs**
    * **location of file.**
    * **X largest numbers to return.**
    * (?) Number of records in each file (this will depend on size of memory of your docker instance)
2. **Read in a section of a remote file**

3. **Sort and return X largest values**
    * So we do need to sort, but only X largest values. But this could very large? maybe even in millions or billions?
    * In a file or standard out? answer: standard out.  
    * If output is to be sent to standard out then it cannot be in billion?
    * Initially I thought this was just a mergesort problem, but it seems it's more likely implementation through a priority queue. 
    Because if the file is extremely large, would need to segment in smaller files and then merge all these files using a priority queue so we don't run out of memory. 
    * Consideration could be memory (space complexity), time complexity and storage requirement. 
    * If implementing on a single instance (not distributed), there could be two options:
        1. Copy the remote file to the single instance in sorted segments.  This assume there is available storage locally for the data.
        2. Storage on the instance is limited, so copy only part of the file sort merge the file locally and delete the segments which have been already sorted. 

4. **Dockerize the application**
    * Create a Dockerfile that will:
    * Install prerequisites
    * Build your application (if necessary)
    * Accept arguments
    * Execute your application
    * You may use any base image that is available publicly on Docker Hub

5. **Output needs to be sent to standard out.**

6. **Output does not need to be in any particular order**

7. **Take into account extremely large files.**

8. **Reducing data transfer.**
    * The only thing I think of here is while transferring file from AWS S3, if connection breaks we continue transfer from where the connection broke, not restart the connection from the start.  I see no other data transfer optimization as the last chunk of file may contain the max numbers we are looking for. 

9. **Testing**

10. **Graded on**
    * Correctness
    * Efficiency (memory, time complexity and data transfer)
    * Testing 
    * Documentation
    * Packaging


**Questions and Work Log**

* Are 3 and 6 contradictory? 
Or can we still Sort to get the largest numbers but then return X largest number IDs in unsorted list?

* Get size of file from amazon S3 to approximate size of file
File could have millions or billions or septillion records
Given the number of records that can be represented by a 20 digit hexadecimal key is 16^20 or 1.21x10^24
1.21 Septillion records. 
Each record can have a 32 bit numeric value.  

* Special useless case: If we are looking for 100 largest values and in the first file we get 100 numbers with max 32 bit values then we can stop. 

* reading the file skip first 499 bytes and start at 500

* don't forget logging, except handling and testing

* output is a unique list of ids associated with the X largest values.

* If all records are copied locally to N number of files, then there should be local storage large enough to handle all of data. 

* Python sorted() function uses Timsort algorithm which is a combination of mergesort and insertsort algorithms.  Go over these sorting algorithms for the interview.

* Added file mergesort but merging one file at a time.  But this is not optimal as the merged file grows and is written so storage requirement will be large.  So with the same storage requirement doing a n-way file mergesort will be faster. 

* If we are searching for 100 largest numbers then if each file size is 100, then when we merge with a new file segment we can discard values that are smaller than the values in the final file. This would reduce storage requirements.

* But what if we are searching for 100 max numbers in a file size of billions. In this case we don't want our file chunks to be 100. So at a minimum we want our file chunk sizes to be larger than the number of values we are looking for but not larger than what can be handled in the instance memory. 

* MapReduce, can also be used to sort each segment file on different instances.

* Now I am only saving in memory the top X dict items after merging, so this will not grow beyond X. 

* I think first implementation is done as I am using External Sort because requirement is to "take into account extremely large files."
    * https://en.wikipedia.org/wiki/External_sorting
    * Segmenting input file into chunks of manageable size which will manage space complexity and storage.
    * Sorting each file using sorted.
        * Python function 'sorted' using Timsort.  Timesort is Hybrid sorting algorithm, derived from mergesort and insertion sort and uses sequences of already sorted data to optimize the best time to O(n), however average O(nlogn) like mergesort.  Also Space complexity is same as mergesoft that is O(N).
    * Using priority queue heapq.merge() for merging 2 sorted files, keeping space complexity limited by only keeping the top X number of records. Time complexity of merging 2 sorted files is a special case of O(NlogK), where K is 2 and N are the total number of elements to be compared. So in this case Time complexity is O(n) while space complexity is O(K) as that is the number of elements in the heapq. 
    * Still need to implement a robust mechanism for getting remote file in chunks and retries in case of network failure.
    * Dockerize solution
    * Add exception handling, testing, logging.

* Write module for downloading file.  Will use boto3. (No will not use boto3 as it's pre-assigned url)
    * boto3 can use multiple threads for faster download. 
    * boto3 can download in chunks.
    * Does it download one chunk at a time (using multiple threads) or it downloads multiple chunks at the same time using multiple threads? 
    * Design wise I want to download each chunk, process the chunk (sort and merge) and then delete this chunk to save storage space. 
    * Its a presigned URL, not a S3 object, so cannot use boto3.  Can use regular python request. 

* I also need to dockerize the app today!!!!

* Looking at the data again, for the given sample the values from 0 to 1999 are distributed uniformly with a frequency from 0 to 4 throughout.  So a non-comparison sort algorithm like bucket sort maybe faster to merge compared to Timsort? Bucketsort can provide O(n) if values are evenly distributed but as bad as O(n^2) if only one bucket has all the values and linked list is used.
* Non-comparison sort algorithm like counting sort may also work for the given sample file as total records N = 2000 while the k = (max-min)+1 = 2001 as well.  However if N is very very large and k stays the same then counting sort may not work.  Since they have asked us to consider a very large file this may not work if k stays the same. 
* Use Partial Sort.  Let say we have 900 MB of data, get first 100MB, sort it and get the top X (lets say 100) numbers.  Get the next 100MB, sort it (bucket sort if evenly distributed) or default sort in Python (Timsort).  Now merge them with the already sorted top X numbers and keep the top X numbers again while discarding the rest. Repeat getting the next 100MB until data is exhausted. Ref: https://en.wikipedia.org/wiki/Partial_sorting
* Given we don't need to have the X largest number sorted then we can use the variant "Partition-based selection".  https://en.wikipedia.org/wiki/Selection_algorithm#Partition-based_selection
* But will Partition based selection work when doing external sorting given data maybe huge. 
  
