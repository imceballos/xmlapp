import logging
from datetime import datetime

class Logger:
    def __init__(self, name, level=logging.DEBUG, filename='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler = logging.FileHandler(filename)
        self.handler.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
    
    def __getattr__(self, name):
        if name in ('debug', 'info', 'warning', 'error', 'critical'):
            return getattr(self.logger, name)
        raise AttributeError(f"'Logger' object has no attribute '{name}'")

    def logging_date_range(self, logging, d1, d2):

        logging_doc = open(logging, 'r')
        data=[]
        if d1=='' and d2=='':
            for i in logging_doc:
                data.append(i.split('\n')[0])
        else:
            try:
                date_ini, date_end=datetime.strptime(d1, "%Y-%m-%dT%H:%M"), datetime.strptime(d2, "%Y-%m-%dT%H:%M")
                for i in logging_doc:
                    date_request= datetime.strptime(i.split(' - ')[0], "%Y-%m-%d %H:%M:%S,%f")
                    if date_ini <= date_request <=date_end:
                        data.append(i.split('\n')[0])
            except Exception as e:
                self.logger.error(e)
        logging_doc.close()
        return data
    
    def logging_type(self, data_ini, tipo):
        data=[]
        for i in data_ini:
            if i.split(' - ')[2]==tipo:
                data.append(i.split('\n')[0])
        return data

    def logging_description(self, data_ini, description):       
        data=[]
        for i in data_ini:
            content = i.split(' - ')[3]
            if description.lower() in content.lower():
                data.append(i.split('\n')[0])
        return data

    def logging_select(self, document, lista):
        for i in lista[0]:
            data_one =self.logging_date_range(document, i[0], i[1])
        for j in lista[1]:
            data_two =self.logging_type(data_one, j)
        for k in lista[2]:
            data_three = self.logging_description(data_two, k)
        
        return data_three

#lista_=[[('2023-05-03 01:35:00,000', '2023-05-03 01:41:20,000')], ['INFO'], ['Not Authenticated','Login succesfully']]
#lista_=[[('','')], ['INFO'], ['Not Authenticated','Login succesfully', 'User Jesus:']]
#lista_=[[('','')], ['INFO'], ['User Jesus']]
#lista_=[[('2023-04-29 04:30:00,000', '2023-04-29 04:44:15,162')], ['INFO'], ['Not Authenticated','Login succesfully']]
#lista_=[[('2023-04-29 03:30:00,000', '2023-04-29 04:00:03,162'), ('2023-04-29 04:30:00,000', '2023-04-29 04:44:15,162')], ['INFO'], ['Not Authenticated','Login succesfully']]
lista_=[[('2023-04-29 03:30:00,000', '2023-04-29 04:00:03,162'), ('2023-05-03 01:33:51,355', '2023-05-03 01:41:40,162')], ['INFO'], ['Not Authenticated','User Jesus']]


#list_fin=logging_select(document, lista_)

#print(list_fin)

#print('')
#print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
#print('')
#3for d in list_fin:
#    print(d)
