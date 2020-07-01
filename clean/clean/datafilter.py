def df_filter(dff = None, series=None, minimum=None, maximum=None):
    if minimum == 0 and not maximum:
        dff = dff[dff[series] >= 0]
        return dff
    if not minimum and maximum == 0:
        dff = dff[dff[series] <= 0]
        return dff
    if minimum == 0 and maximum:
        dff = dff[(dff[series] >= 0) & (dff[series] <= maximum)]
        return dff
    elif minimum and maximum == 0:
        dff = dff[(dff[series] >= minimax) & (dff[series] <= 0)]
        return dff
    elif minimum == 0 and maximum == 0:
        dff = dff[(dff[series] >= 0) & (dff[series] <= 0)]
        return dff
    elif minimum and maximum:
        dff = dff[(dff[series] >= minimum) & (dff[series] <= maximum)]
        return dff
    elif minimum:
        dff = dff[dff[series] >= minimum]
        return dff
    elif maximum:
        dff = dff[dff[series] <= maximum]
        return dff
    return dff


def value_none(value):
    if value == "None":
        value = None
    return value


def filter_data_master(PV_min,PV_max,PP_min,PP_max,EOD_min,EOD_max,dff):
    for v in [PV_min,PV_max,PP_min,PP_max,EOD_min,EOD_max]:
        value_none(v)
    
    PV_min = value_none(PV_min)
    PV_max = value_none(PV_max)
    PP_min = value_none(PP_min)
    PP_max = value_none(PP_max)
    EOD_min = value_none(EOD_min)
    EOD_max = value_none(EOD_max)
    

    dff1 = df_filter(dff,'PotentialValue',PV_min,PV_min)
    dff2 = df_filter(dff1,'ProbPercent',PP_min,PP_max)
    dff3 = df_filter(dff2,'EOD_delta',EOD_min,EOD_max)
    return dff3