import time, calendar
from datetime import datetime,timedelta

now = lambda: time.time()
nowref = lambda: "%d" % (time.time()*1000)
qgroup_localtime = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
beijingtime = lambda: datetime.strftime(datetime.utcnow() + timedelta(hours=8),"%Y-%m-%d %H:%M:%S")
getutcnow = lambda: datetime.strftime(datetime.utcnow(),"%Y-%m-%d %H:%M:%S")
getutcnow_f = lambda: datetime.strftime(datetime.utcnow(),"%Y-%m-%d %H:%M:%S.%f")

def utc2local(strtime):
    # UTC 为时间字符串转本地时间
    try:
        utc_dtm = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S") 
        local_tm = datetime.fromtimestamp(0)
        utc_tm = datetime.utcfromtimestamp(0)
        offset = local_tm - utc_tm
        ret = datetime.strftime(utc_dtm + offset,"%Y-%m-%d %H:%M:%S")
    except ValueError or TypeError:
        ret = ""
    return ret

def local2utc(strtime):
    # 本地时间字符串转UTC时间字符串
    try:
        local_dtm = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f" if '.' in strtime else \
                    "%Y-%m-%d %H:%M:%S")
        local_tm = datetime.fromtimestamp(0)
        utc_tm = datetime.utcfromtimestamp(0)
        offset = local_tm - utc_tm
        ret = datetime.strftime(local_dtm - offset,"%Y-%m-%d %H:%M:%S")
    except ValueError or TypeError:
        ret = ""
    return ret

def utc2beijing(strtime):
    try:
        utc_dtm = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f" if '.' in strtime else \
                    "%Y-%m-%d %H:%M:%S")
        ret = datetime.strftime(utc_dtm + timedelta(hours=8),"%Y-%m-%d %H:%M:%S")
    except ValueError or TypeError:
        ret = ""
    return ret
    
def beijing2utc(strtime):
    try:
        bj_dtm = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f" if '.' in strtime else \
                    "%Y-%m-%d %H:%M:%S")
        ret = datetime.strftime(bj_dtm - timedelta(hours=8),"%Y-%m-%d %H:%M:%S")
    except ValueError or TypeError:
        ret = ""
    return ret

#flag = 0 then -timedelta, else + timedelta
def deltadate(strtime, delta, flag = 0):
    try:
        utc_dtm = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f" if '.' in strtime else \
                    "%Y-%m-%d %H:%M:%S")
        ret = datetime.strftime((utc_dtm + timedelta(hours=delta)) if flag else (utc_dtm -timedelta(hours=delta)),"%Y-%m-%d %H:%M:%S")
    except ValueError or TypeError:
        ret = ""
    return ret
    
def getDate(strtime):
    try:
        utc_dtm = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f" if '.' in strtime else \
                    "%Y-%m-%d %H:%M:%S")
        ret = datetime.strftime(utc_dtm,"%Y-%m-%d")
    except ValueError or TypeError:
        ret = ""
    return ret

class dict2obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [dict2obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, dict2obj(b) if isinstance(b, dict) else b)
               
def obj2dict(obj):
    '''把对象(支持单个对象、list、set)转换成字典'''
    #注意，不支持嵌套
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            #把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
    return dict