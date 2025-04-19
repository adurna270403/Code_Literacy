import requests     
import time
import pandas as pd
import shutil
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth



load_dotenv()

username = os.getenv("WQ_USERNAME")
password = os.getenv("WQ_PASSWORD")

class WQBrain():
    def __init__(self, cookie,
                 instrumentType="EQUITY", 
                 region="USA",
                 universe="TOP3000",
                 delay=1,
                 decay=5,
                 neutralization="SUBINDUSTRY",
                 truncation=0.1,
                 pasteurization="ON",
                 unitHandling="VERIFY",
                 nanHandling="OFF",
                 language="FASTEXPR",
                 visualization=False,):
        self.header = {
                        'accept': 'application/json;version=2.0',
                        'accept-language': 'en,vi;q=0.9',
                        'origin': 'https://platform.worldquantbrain.com',
                        'priority': 'u=1, i',
                        'referer': 'https://platform.worldquantbrain.com/',
                        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        'content-type': 'application/json',
                        'content-length': '0',
                        'x-client-data': 'CKa1yQEIl7bJAQimtskBCKmdygEI6vPKAQiSocsBCMeiywEImv7MAQiFoM0BCKPAzgEYj87NAQ=='
                        }
        self.header["cookie"] = cookie


        self.settings = {
            "instrumentType": instrumentType,
            "region": region,
            "universe": universe,
            "delay": delay,
            "decay": decay,
            "neutralization": neutralization,
            "truncation": truncation,
            "pasteurization": pasteurization,
            "unitHandling": unitHandling,
            "nanHandling": nanHandling,
            "language": language,
            "visualization": visualization,
        }
        self.s = requests.session()
        self.auth = HTTPBasicAuth(username, password)  #đây là dòng thêm vào so với các video khác
        self.login = self.s.post(url = "https://api.worldquantbrain.com/authentication", headers= self.header, auth = self.auth)
        #nhớ k nhầm thì dòng này cũng là dòng mới
        cookie = f"t={self.login.cookies.get('t')}"
        

    def Simulate(self, alpha, timesleep = 0.5):
        try:
            simu_data = {
                "type": "REGULAR",
                "settings": self.settings,
                "regular": alpha
            }

            simu_response = self.s.post('https://api.worldquantbrain.com/simulations', json = simu_data)
            if 'location' not in simu_response.headers:
                print("Error at Location")
                return None 
                          
            simu_url = simu_response.headers['location']
            while True:
                simu_result = self.s.get(simu_url)
                if simu_result.headers.get('Retry-After', 0) == 0:
                    break
                time.sleep(timesleep)

            alpha = simu_result.json()["alpha"]
            final_result = self.s.get(f"https://api.worldquantbrain.com/alphas/{alpha}")

            if  not final_result.ok:
                return None
            
        except Exception as e:
            return None
             

    def get_before_after_score(self, id):
            payload = {}  #có hoặc không cũng k sao, api của bên này k chặt lắm
            url = f"https://api.worldquantbrain.com/competitions/IQC2025S1/alphas/{id}/before-and-after-performance"
            while True:
                try:
                    response = requests.get(url = url, headers=self.header, data = payload)
                    response.raise_for_status()
                    a= response.json()['score']['after']-response.json()['score']['before']
                    print("Done")
                    return a 
                except (requests.exceptions.RequestException, ValueError):
                    print("Retrying right now...")
                    time.sleep(0.5)
            

    def check_sub(self):
        



def count_pass(x):
    a=str(x["is"]).count("PASS")
    return a 