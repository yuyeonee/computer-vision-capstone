# Database Module for single client

import pyrebase
import json

class Client:
    def __init__(self):
        """
        class: Initialize Database Client
        """
        with open("auth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        print("✅ Database Correctly Connected")


    def write_attention(self, data):
        """
        function: write single summarized data about attention on database
        """
        # data_parameter_example = {
        #     "name":"Charlie",
        #     "s_id":202000002, # s_id로 데이터를 처리할 것임
        #     "score":1
        # }
        # data = data_parameter_example
        self.db.child("attention").child(data["s_id"]).set(data)

    def __is_exist__(self, s_id, database = "understand"):
        """
        function: s_id에 해당하는 데이터가 데이터베이스에 존재하는지 확인하는 코드
        """
        data = self.db.child(database).child(s_id).get().val()
        if data == None:
            return False
        else:
            return True

    def write_understand(self, data):
        """
        function: 아래의 data_parameter_example처럼 들어오는 data에 대해서 understand라는 이름 아래에 하나씩 업데이트
        만약에 s_id에 해당하는 정보가 있을 경우엔, 해당 데이터를 업데이트 한다. 
        아닐 경우, 새로 데이터를 넣는다.
        """
        # data_parameter_example = {
        #     "name":"Charlie",
        #     "s_id":202000002, # s_id로 데이터를 처리할 것임
        #     "score":0
        # }
        # data = data_parameter_example
        self.db.child("understand").child(data["s_id"]).set(data)
        

if __name__ == "__main__":
    my_client = Client()
    my_client.write_attention()