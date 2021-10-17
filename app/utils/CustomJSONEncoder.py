from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):

    def default(self, o):
        import datetime
        # if type(o) == datetime.timedelta:
        #     return str(o)
        # elif type(o) == datetime.datetime:
        #     return o.isoformate()
        '''日期格式'''
        if isinstance(o,datetime.datetime):
            return str(o)
        # decimal格式
        import decimal
        if isinstance(o,decimal.Decimal):
            # print(o)
            return float(o)
        super(CustomJSONEncoder, self).default(o)



