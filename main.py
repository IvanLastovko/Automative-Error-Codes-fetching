import pandas as pd
from impala.dbapi import connect

error_code_query = """
WITH summary AS (
    SELECT p.serialnumber, 
           p.firstfailedmeasurepointname, 
           p.measureitem_result, 
           ROW_NUMBER() OVER(PARTITION BY p.serialnumber 
                                 ORDER BY p.measures_test_timestamp ASC) AS rank
      FROM plda.curve_testresults_full_extract p
      WHERE p.serialnumber in ('X617A12367','X617A12321','BU95435600') 
      AND testpassed = 'N' AND measurepoint_status = 'Fail'
      AND measurepoint_name = 'Average Absolute Value')
 SELECT serialnumber as SerialNumber, firstfailedmeasurepointname, measureitem_result,
 	CASE
	    WHEN summary.firstfailedmeasurepointname LIKE 'IM3_C1%' THEN 
			CASE 
				WHEN SUBSTRING(summary.firstfailedmeasurepointname, 8, 2) IN ('01', '05', '09', '13') THEN concat('RXA', ' ', summary.measureitem_result)
				WHEN SUBSTRING(summary.firstfailedmeasurepointname, 8, 2) IN ('02', '06', '10', '14') THEN concat('RXB', ' ', summary.measureitem_result)
				WHEN SUBSTRING(summary.firstfailedmeasurepointname, 8, 2) IN ('03', '07', '11', '15') THEN concat('RXC', ' ', summary.measureitem_result)
				WHEN SUBSTRING(summary.firstfailedmeasurepointname, 8, 2) IN ('04', '08', '12', '16') THEN concat('RXD', ' ', summary.measureitem_result)
	        ELSE '' END
	    ELSE concat('RX', SUBSTRING(summary.firstfailedmeasurepointname, 3, 1), ' ', summary.measureitem_result)
	END AS ErrorCode
   FROM summary
 WHERE rank = 1
;
"""

# Specify connection details
host_name = 'hadoop-c02n14.ss.sw.ericsson.se'
port = 21050
conn = connect(host=host_name, port=port)
cur = conn.cursor()

# Execute the query
cur.execute(error_code_query)
result = cur.fetchall()

# Displays result in terminal
for data in result:
    print(data)

# Download data to excel sheet and save it with file name "ErrorCodes.xlsx"
df = pd.DataFrame(list(result))
writer = pd.ExcelWriter('ErrorCodes.xlsx')
df.to_excel(writer, sheet_name='ErrorCodes')
writer.save()
