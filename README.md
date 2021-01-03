# triad-challenge
TRI-AD coding challenge

* Run the app inside the docker container 
  * Run default configuration `docker run --rm -it triadchallenge:latest` 
  * Run with options `docker run --rm -it triadchallenge:latest --url https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt --x 5` 

* Run the pytests inside docker container
  * `docker run --rm -it --entrypoint "pytest" triadchallenge:latest /app`