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
    * If output is to be sent to standard out then it cannot be in billion? right?
4. Dockerize the application
    * execute a docker container 

5. Output needs to be sent to standard out.

6. Output does not need to be in any particular order

7. Take into account extremely large files.

8. Reducing data transfer.

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

* 
