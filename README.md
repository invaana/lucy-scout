# Scout  

This is a data aggregation framework for scouting and aggregating Scientific Data.

The framework contains 3 modules:

- **scider** - a scientific data spider  
- **sanitizer** - sanitising the aggregated data to use it further for text mining and processing.
- **db** - database module that stored the data into database (Currently supports MongoDB only)

## How to use 

```
Step1:  Create a scider input json file 
# example : examples/configs/github.json

Step2: Install scout

# development version
pip install -e git://github.com/invaana/scout.git@develop#egg=scout 

# stable version (currently no stable version exists)
pip install -e git://github.com/invaana/scout.git#egg=scout



```