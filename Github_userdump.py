import requests
import json

pg_num= 1
lmt_num = 100
#URL = "https://api.github.com/orgs/<org>/users"
while True:
    URL = "https://api.github.com/orgs/<org>/members?per_page="+str(lmt_num)+"&page="+str(pg_num)
    headers = {"Accept": "application/vnd.github+json",
            "Authorization": "Bearer <token>",
            "X-GitHub-Api-Version": "2022-11-28"
            }
    response = requests.get(URL, headers = headers)
    json_data = response.text

    if json_data == "[]":
        #print("No more data")
        break
    else:
        data_prs = json.loads(json_data)
        with open("github_names.txt", "a") as file:
            for data in data_prs:
                file.write(data["login"]+"\n")
                #print(data["login"])
        #print(data_prs)
        #print(data_prs['login'])
    pg_num +=1
