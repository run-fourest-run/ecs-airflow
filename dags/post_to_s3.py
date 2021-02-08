class Get_Stocks:
    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        self.headers = {
                        'x-rapidapi-key': "d5e95517a2msh75c98018c625d82p12ab5ejsndd559dc778fd",
                        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
                        }


    def __call__(self):
        s3 = boto3.resource('s3')
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
        query_string = {"symbol":self.holding_symbol,"region":self.country_code}
        response = requests.request("GET",url,headers=self.headers,params=query_string)
        json_obj = json.loads(response.text)
        s3Object = s3.Object(self.bucket,self.destination_file)
        s3Object.put(Body=(bytes(json.dumps(json_obj).encode('UTF-8')))
                     )
