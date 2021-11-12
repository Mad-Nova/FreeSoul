def lastTwo(num):
    return num %100

def lastOne(num):
    return num %10

def produceSpaceTime(timer):
    val = timer
    sec = lastTwo(val)
    val = val/100
    min = lastTwo(val)
    val = val/100
    hrs = lastOne(val)
    val = val/10
    day = lastOne(val)
    val = val/10
    mon = lastOne(val)
    val = val/10
    yrs = val
    return {"sec":sec,"min":min,"hrs":hrs,"day":day,"mon":mon,"yrs":yrs}
    
