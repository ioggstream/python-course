from time import time
from datetime import datetime

class ThrottlingQuota(): 
    def __init__(self, ttl, quota): 
        self._dict = {} 
        self.ttl = ttl 
        self.quota = quota 
    def add(self, user): 
        if user in self._dict: 
            q = self._dict[user] 
            if q['expires'] < time(): 
                q['count'] = 1 
                q['expires'] = (1 + time() // self.ttl) * self.ttl 
            else: 
                 
                q['count'] += 1 
                if q['count'] > self.quota: 
                    return dict(**q, quota=self.quota, exceeded=True, comment=datetime.fromtimestamp(q['expires']).isoformat()) 
        else: 
            q = self._dict[user] = {'count': 1, 'expires':  (1 + time() // self.ttl) * self.ttl 
            }  
        return dict(**q, quota=self.quota) 

tq = ThrottlingQuota(20, 100)
for i in range(100):
  tq.add(1)


