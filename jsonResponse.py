import json



string1 = {
	"results": {
		"locations": [{
			"@AWAY": False,
			"@AWAYCONFIG": True,
			"@LOCATION_INFO": "Tracy, CA",
			"@LOCATION_NAME": "Home",
			"@LOCATION_STATUS": "I'm Home",
			"@VACATION": False,
			"@VACATIONCONFIG": False,
			"@WEATHER": "99°",
			"@WEATHER_F": 99,
			"@WEATHER_I": "sunny.png",
			"equiptments": [{
				"@ACTIVE": True,
				"@ALERTCOUNT": 0,
				"@AWAY": False,
				"@AWAYCONFIG": False,
				"@AWAY_MSG": "",
				"@BCONFIG": [{
					"align": "center",
					"name": "@HEATERSON",
					"type": "TEXT_LABEL_VIEW",
					"value": ""
				}],
				"@CONNECTED": True,
				"@DRACTIVE": {
					"constraints": {
						"dialog": [{
							"message": "This should not impact the water temperature in your home. Do you want to opt out for this event ?",
							"title": "Tank temperature has been changed in response to a Utility Load Control event",
							"value": 1
						}]
					},
					"value": ""
				},
				"@ENABLED": {
					"constraints": {
						"enumText": ["Disabled", "Enabled"],
						"enumTextIcon": ["ic_device_off.png", "ic_enabled.png"],
						"lowerLimit": 0,
						"upperLimit": 1
					},
					"status": "Enabled",
					"value": 1
				},
				"@HEATERSON": "",
				"@NAME": {
					"constraints": {
						"stringLength": 64
					},
					"value": "Tankless Water Heater"
				},
				"@RESUME": False,
				"@RUNNING": "",
				"@SCHEDULE": False,
				"@SCHEDULERESUME": "",
				"@SCHEDULESTATUS": "",
				"@SETPOINT": {
					"constraints": {
						"error": [],
						"isConversion": True,
						"lowerLimit": 85,
						"unit": 1,
						"upperLimit": 140,
						"warning": [{
							"message": "CAUTION HOT WATER. Contact may cause serious burns to skin",
							"value": 121
						}]
					},
					"value": 138
				},
				"@STATUS": "Enabled",
				"@TCONFIG": [{
					"align": "center",
					"name": "@RUNNING",
					"type": "TEXT_LABEL_VIEW",
					"value": ""
				}],
				"@TYPE": "tanklessWaterHeater",
				"actions": ["networkSettings", "waterheaterUsageReportView"],
				"device_name": "6309535886154236",
				"device_type": "WH",
				"mac_address": "40-9F-38-42-40-57",
				"serial_number": "40-9F-38-42-40-57-4160"
			}],
			"location_id": "b515bfb8-7f2b-4aa1-aae2-6d9671df4d69"
		}]
	},

	"options": {
		"_id": "60a36f10da6f34d3d697d813",
		"account_id": "4856732562345223",
		"allow_email_notifications": False,
		"allow_product_alert_emails": True,
		"allow_product_alert_text_msg": True,
        "allow_push_notifications": False,
        "allow_special_offers_emails": True,
        "allow_special_offers_text_msg": True,
        "allow_text_notifications": False,
        "cb_service_account": False,
        "connected": False,
        "email": "sjpbailey@comcast.net",
        "first_name": "Steven",
        "is_phone_verified": True,
        "last_name": "Bailey",
        "phone_number": "12099141055",
        "receive_marketing_messages": False,
        "report_state": True,
        "role": 0,
        "share_status": 0,
        "success": True,
        "temperature_display_unit": "Fahrenheit",
        "user_id": "ccc1d2f00bbcf0ccd8c8fffdc3a001"
	},
	
	"user_id": "ccc1d2f00bbcf0ccd8c8fffdc3a001",
	"user_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjY2MxZDJmMDBiYmNmMGNjZDhjOGZmZmRjM2EwMDEiLCJzaWQiOiIxYTJjNWRmZS03YTM4LTQ4ZGItYjFjNi1lNWY0M2EyNzYyNWEiLCJ1dCI6MiwidHQiOjEsImV4cCI6LTEsImlhdCI6MTYzMTUzODgzM30.5rqGeqWWYCDA1iZWc4ahBFrsH_rC-EOTzT4zC63a8jQ"
    
}

print("\n")
#print(string1)
print("\n")


print("\n")
#print((string1, "locations"))
print("\n")

print(string1["results"]["locations"][0]["@WEATHER_F"]) # Tracy, CA
print("\n")
print(string1["results"]["locations"][0]["equiptments"])
print("\n")
string1["results"]["locations"][0]["equiptments"][0]['@SETPOINT']['value']=137
print(string1["results"]["locations"][0]["equiptments"][0]['@SETPOINT']['value'] ) # 138 YEAH!!!!!!!!!!!!!!!!!!!!!!
print("\n")
print(string1["results"]["locations"][0]["equiptments"][0]["@ENABLED"]['value']) # {'constraints': {'enumText': ['Disabled', 'Enabled'], 'enumTextIcon': ['ic_device_off.png', 'ic_enabled.png'], 'lowerLimit': 0, 'upperLimit': 1}, 'status': 'Enabled', 'value': 1}
print("\n")
print(string1["options"]["phone_number"])


#print(string1["results"]["locations"][0]["equiptments"][0]["@ENABLED"]['constraints']['enumText']) # ['Disabled', 'Enabled']
#print(string1["results"]["locations"][0]["equiptments"][0]["@ENABLED"]['constraints']['enumTextIcon']) # ['ic_device_off.png', 'ic_enabled.png']
#print(string1["results"]["locations"][0]["equiptments"][0]["@ENABLED"]['constraints']['upperLimit'])
print("\n")

print("\n")
#print("\n".join("{}\t{}".format(k, v) for k, v in string1.items()))
print("\n")

print("\n")
#for results in string1.values():
#    print("Key : {} , Value : {}".format(results,string1[results]))
#    print("\n")
