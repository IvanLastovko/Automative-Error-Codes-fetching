import pandas as pd
from impala.dbapi import connect
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)

@app.route('/analyze', methods = ['POST'])
@cross_origin()
def analyze_SN():  # put application's code here
    list_of_SN = []
    for sn in request.json['serial_numbers']:
        print('SN: ' + str(sn))
        list_of_SN.append(str(sn))

    # with open('Book1.csv', newline='') as csv_file_read:
    #     csv_reader = csv.reader(csv_file_read)
    #
    #     for row in csv_reader:
    #         print(row[0])
    #         list_of_SN.append(row[0])
    #
    #     print(str(tuple(list_of_SN)))

    error_code_query = """
WITH summary AS (
    SELECT p.serialnumber,
           p.firstfailedmeasurepointname,
           p.measureitem_result,
           ROW_NUMBER() OVER(PARTITION BY p.serialnumber
                                 ORDER BY p.measures_test_timestamp DESC) AS rank
      FROM plda.curve_testresults_full_extract p
      WHERE p.serialnumber in """ + str(tuple(list_of_SN)) + """
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
    final_result = []

    for SN in list_of_SN:
        found = False
        for data in result:
            # print(data)
            if str(data[0]) == str(SN):
                print('FOUND: ' + SN)
                found = True
                final_result.append([SN, data[3]])
                break
        if not found:
            print('DID NOT FOUND: ' + SN)
            final_result.append([SN, '-'])


#     # Download data to excel sheet and save it with file name "ErrorCodes.xlsx"
#     df = pd.DataFrame(final_result)
#     writer = pd.ExcelWriter('ErrorCodes.xlsx')
#     df.to_excel(writer, sheet_name='ErrorCodes')
#     writer.save()
    return jsonify({'result': final_result})


if __name__ == '__main__':
    app.run()

