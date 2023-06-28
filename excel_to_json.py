import pandas
import json

excel_file_name = "20230628_CONT_ASSESS_CEIL"
new_file_name = "cont_asses_ceil_v2"
order = ["ContAssessCeil", "Date"]

excel_data = pandas.read_excel(f"{excel_file_name}.xlsx", header=10)
excel_data = excel_data[order]
excel_data.rename(columns={"ContAssessCeil": "cont_asses_ceil", "Date": "date"}, inplace=True)

excel_data["cont_asses_ceil"] = excel_data["cont_asses_ceil"].round().astype(int)

json_data = excel_data.to_json(orient="records")

json_dict = json.loads(json_data)

with open(f'{new_file_name}.json', 'w') as json_file:
    json.dump(json_dict, json_file)
