# Error Description Table for Filters 
## _Fetches and creates error codes from serial numbers_

This project is to fetch error codes from PLDA database from given serial numbers.

- Sample Serial Number: _'X617A12367'_, corresponding error code: _'RXA -101.7'_

### Features

- An SQL query which fetches set of results from serial number using PLDA database.
- Conditions for the query (explained):
    1. Test is a failure (testpassed = 'N')
    2. Measurepoint status as failed (measurepoint_status = 'Fail')
    3. Measurepoint status as Average Absolute Value (measurepoint_name = 'Average Absolute Value')
    4. The error codes are created based on Measure Point Names as follows:
        a. If the measurepoint name begins with 'IM' or '12' then the error code will be the 3rd character, for example, 'IMB_B25.3' will have Error Code beginning with 'RXB' and 'IMA_B25.3' will have error code beginning with 'RXA'.
        b. If the measurepoint name begins with 'IM3_C1' then the error code will be as such:
        - RXA: When the code after 'IM3_C1' [For example: 'IM3_C1.01.01'] is from the list ['01', '05', '09', '13']
        - RXB: When the code after 'IM3_C1' is from the list ['02', '06', '10', '14']
        - RXC: When the code after 'IM3_C1' is from the list ['03', '07', '11', '15']
        - RXD: When the code after 'IM3_C1' is from the list ['04', '06', '12', '16']
- The code is then appended with the Measure Item value and saved as RXA -101.7 (For example when value is -101.7)
- After results are fetched and formatted, it is displayed in the terminal and stored in an excel file for further use.
    
## Tech

This project uses the following:

- [Python] - Python 3.9.6
- [SQL] - For fetching data using SQL query
- [Conda](https://docs.conda.io/en/latest/) - For dependency management.
- [Impyla](https://github.com/cloudera/impyla) - Python client for HiveServer2 implementations (e.g., Impala, Hive) for distributed query engines. If you have conda then installation is from https://anaconda.org/anaconda/impyla
- [Pandas](https://pandas.pydata.org/getting_started.html) -  For data analysis and manipulation.

## Issues addressed as per the requirements:

- Request multiple serial numbers at the same time.
- Speeds up the response by removing Chrome/MI analytics as the middle man and allow the code to extract the data directly from the backend.
- Security and compliance is ensured as the code connects with PLDA database as per it's connection parameters.
    
## Database Details

- Database name: Cloudera Impala
- Host: hadoop-c02n14.ss.sw.ericsson.se
- Port: 21050
- Database/Schema: PLDA

## Author
Madhushree Singh
