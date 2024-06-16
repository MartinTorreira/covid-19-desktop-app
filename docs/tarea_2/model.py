import gi
import threading
import requests
from datetime import datetime,timedelta

class Model():

    def search_user_data(*entry):
        if(len(entry[1]) == 0):
            r = requests.get("http://localhost:8080/api/rest/users",
                            headers = {"x-hasura-admin-secret":"myadminsecretkey"})
        elif(len(entry[1]) == 1):
            r = requests.get("http://localhost:8080/api/rest/user?name="+
                            entry[1][0]+"&surname=",
                            headers = {"x-hasura-admin-secret":"myadminsecretkey"})
        else:
            r = requests.get("http://localhost:8080/api/rest/user?name="+
                            entry[1][0]+"&surname="+entry[1][1],
                            headers={"x-hasura-admin-secret":"myadminsecretkey"})
        data = r.json()
        return data
        
        
        
    def facility_data(self,id):
        print(id)
        r = requests.get("http://localhost:8080/api/rest/user_access_log/"+str(id),
                         headers = {"x-hasura-admin-secret":"myadminsecretkey"})
        data = r.json()
        return data
        
       
       
    def facilities_id(*entry):
        r = requests.get("http://localhost:8080/api/rest/facilities",
                headers = {"x-hasura-admin-secret":"myadminsecretkey"})
        data = r.json()

        for x in range(len(data['facilities'])):
            if (data['facilities'][x]['name'] == entry[1]):
                return data['facilities'][x]['id']

    def search_tracker_data(self, id, date_string):
        d = datetime.strptime(date_string,"%d/%m/%Y")
        d2 = d + timedelta(days=-20)
        d_iso = d.isoformat()
        d2_iso = d2.isoformat()
        r = requests.get(
        "http://localhost:8080/api/rest/facility_access_log/"+str(id)+"/daterange",
        headers={"x-hasura-admin-secret":"myadminsecretkey"},
        json={"startdate": d2_iso, "enddate": d_iso})
        data = r.json()
        
        return data
        
    
    def search_tracker_data2(self, uuid, date_string):
        d = datetime.strptime(date_string,"%d/%m/%Y")
        d2 = d + timedelta(days=-20)
        d_iso = d.isoformat()
        d2_iso = d2.isoformat()
        r = requests.get(
        "http://localhost:8080/api/rest/user_access_log/"+str(uuid)+"/daterange",
        headers={"x-hasura-admin-secret":"myadminsecretkey"},
        json={"startdate": d2_iso, "enddate": d_iso})
        data = r.json()
        
        array_id=[]

        for x in range (len(data['access_log'])):
        	if(data['access_log'][x]['type']=='IN'):
        		array_id.append(data['access_log'][x]['facility']['id'])
        		
        return array_id














