write program that will read the data

The idea is to:
1. Take in command line inputs
    * location of file.
    * X largest numbers to return. 
    * (?) Number of records in each file (this will depend on size of memory of your docker instance)
2. Read in a section of a remote file

3. Sort and return X largest values
    * So we do need to sort, but only X largest values. But this could very large? maybe even in millions or billions?
    * In a file or standard out? answer: standard out.  
    * If output is to be sent to standard out then it cannot be in billion?
    * Initially I thought this was just a mergesort problem, but it seems it's more likely implementation through a priority queue. 
    Because if the file is extremely large, would need to segment in smaller files and then merge all these files using a priority queue so we don't run out of memory. 
    * Consideration could be memory (space complexity), time complexity and storage requirement. 
    * If implementing on a single instance (not distributed), there could be two options:
        1. Copy the remote file to the single instance in sorted segments.  This assume there is available storage locally for the data.
        2. Storage on the instance is limited, so copy only part of the file sort merge the file locally and delete the segments which have been already sorted. 

4. Dockerize the application
    * execute a docker container 

5. Output needs to be sent to standard out.

6. Output does not need to be in any particular order

7. Take into account extremely large files.

8. Reducing data transfer.
    * The only thing I think of here is while transferring file from AWS S3, if connection breaks we continue transfer from where the connection broke, not restart the connection from the start.  I see no other data transfer optimization as the last chunk of file may contain the max numbers we are looking for. 

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

* Added file mergesort but merging one file at a time.  But this is not optimal as the merged file grows and is written so storage requirement will be 
large.  So with the same storage requirement doing a n-way file mergesort will be faster. 

* If we are searching for 100 largest numbers then if each file size is 100, then when we merge with a new file segment we can discard values that are smaller than the values in the final file. This would reduce storage requirements.

* But what if we are searching for 100 max numbers in a file size of billions. In this case we don't want our file chunks to be 100. So at a minimum we want our file chunk sizes to be larger than the number of values we are looking for but not larger than what can be handled in the instance memory. 

* MapReduce? 

* Now I am only saving in memory the top X dict items after merging, so this will not grow beyond X. 

* I think first implementation is done as I am:
    * Segmenting input file into chunks of manageable size
    * Sorting each file using sorted (which is selection sort and mergesort combination)
    * Using priority queue for merging different files, keeping space complexity limited by only keeping the top X number of records. 
    * Still need to implement a robust mechanism for getting remote file in chunks and retries in case of network failure.
    * Dockerize solution
    * Add exception handling, testing, logging.
