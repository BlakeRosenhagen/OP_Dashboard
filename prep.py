


def get_data():
    import pandas as pd
    import numpy as np
    from datetime import timedelta


    df = pd.read_csv("data/input.csv", header=0)
    df


    df["New"] = df['New'].astype('str')
    df["Stage"] = df['Stage'].astype('str')


    true_phrases = ["new","New","ew","Ne","ne"]
    false_phrases = ["exist","Exist","ex","Ex","ist","ng","st"]
    stage_phrases = ["confirming","con","nfirm","application","app","investigating","invest","gating"]
    for index, row in df.iterrows():
        for t_p in true_phrases:
            if type(row["New"]) == bool: break
            if t_p in row["New"]:
                df.at[index,"New"] = True

        for f_p in false_phrases:
            if type(row["New"]) == bool: break
            if f_p in row["New"]:
                df.at[index,"New"] = False
                
        if type(row["New"]) != bool:
            pass
            #df.at[index,"New"] = np.nan
            
        for s_p in stage_phrases:
            if s_p in row["Stage"]:
                df.at[index,"Stage"] = "Discovery (S.P.I.N.)"


    ### removing artifacts from PV and PP

    df["PotentialValue"] = df['PotentialValue'].astype('str')
    df["ProbPercent"] = df['ProbPercent'].astype('str')


    df["UpdateDate"] = df['UpdateDate'].astype('str')
    df["ExpectedOrderDate"] = df['ExpectedOrderDate'].astype('str')


    numlist = ["0","1","2","3","4","5","6","7","8","9"]
    PVindex = []
    PPindex = []
    UDindex = []
    EODindex = []
    nonnumindex = []
    for index, row in df.iterrows():
        stringa = row['PotentialValue']
        row['PotentialValue'] = stringa.strip("$").replace(',',"")
        stringb = row['ProbPercent']
        row['ProbPercent'] = stringb.strip("%")
        stringc = row["UpdateDate"]
        stringd = row["ExpectedOrderDate"]
        counta, countb, countc, countd = [0]*4
        for num in numlist:
            if num in stringa: counta += 1
            if num in stringb: countb += 1
            if num in stringc: countc += 1
            if num in stringd: countd += 1
        if counta == 0: 
            df.at[index,"PotentialValue"] = np.NaN
            PVindex.append(index)
        if countb == 0:
            df.at[index,"ProbPercent"] = np.NaN
            PPindex.append(index)
        if countc == 0:
            df.at[index,"UpdateDate"] = np.NaN
            UDindex.append(index)
        if countd == 0:
            df.at[index,"ExpectedOrderDate"] = np.NaN
            EODindex.append(index)


    df["UpdateDate"] = pd.to_datetime(df["UpdateDate"],errors="coerce")
    df["ExpectedOrderDate"] = pd.to_datetime(df["ExpectedOrderDate"],errors="coerce")


    now = pd.to_datetime("now")
    df["EOD_delta"] = df["ExpectedOrderDate"] - now
    df["EOD_delta"] = df["EOD_delta"].dt.days
    df["UD_delta"] = df["UpdateDate"] - now
    df["UD_delta"] = df["UD_delta"].dt.days


    stage_weight_dict = {"Discovery (S.P.I.N.)":.40,
                        "Solution Development":.50,
                        "Quoting":.60,
                        "Working":.75,
                        "On Hold":.9,
                        "Won":1.0,
                        "Lost (why?)":0
                        }

    ProbPercent_stage = []
    for i in df["Stage"]:
        if i not in stage_weight_dict.keys(): 
            ProbPercent_stage.append(np.NaN)
            continue
        ProbPercent_stage.append(stage_weight_dict[i])
    df["ProbPercentStage"] = ProbPercent_stage


    df_num = df.dropna(subset=["PotentialValue","ProbPercent","ProbPercentStage"])

    df_num["PotentialValue"] = df_num['PotentialValue'].astype('int')
    df_num["ProbPercent"] = df_num['ProbPercent'].astype('float')
    df_num["ProbPercentStage"] = df_num["ProbPercentStage"].astype("float")

    df_num["ProbPercent"] = df_num["ProbPercent"] / 100

    df["ProbPercentDiff"] = df_num["ProbPercent"] - df_num["ProbPercentStage"]

    df_num["ExpectedValue"] = df_num["PotentialValue"] * df_num["ProbPercent"]
    df_num["ExpectedValue"] = df_num["ExpectedValue"].astype("int")

    df_num["ExpectedValueStage"] = df_num["PotentialValue"] * df_num["ProbPercentStage"]


    column_names = ['Div', 'Branch', 'OAM', 'LeadType', 'LeadSpecifics',
        'Customer', 'Type', 'New', 'City, St', 'ProjectOpportunity',
        'KeyVendor', 'TechnologiesServices Proposed', 'PotentialValue',
        'ProbPercent','ExpectedValue', "ExpectedValueStage",
            'CustomerCompelingEvent', 'Stage', "ProbPercentStage", "ProbPercentDiff", 'YourNextBIGStep',
            'Notes','UpdateDate', "UD_delta", 'ExpectedOrderDate', "EOD_delta" ]
    df_num = df_num.reindex(columns=column_names)


    ### splitting data frames
    """
    df

        df_num
            df_date
    """

    # Opportunity Funnel

    ### People often use "sales pipeline" and "sales funnel" interchangeably. However, a funnel suggests the number of prospects you're working with steadily drops off as the sales process goes on.

    ### creating junk DataFrame

    PV_list = list(str(i) for i in df_num["PotentialValue"].unique())
    PP_list = list(str(int(i*100)) for i in df_num["ProbPercent"].unique())
    df_junka = df[~df.PotentialValue.isin(PV_list)]
    df_junkb = df_junka.append(df[~df.ProbPercent.isin(PP_list)])


    stages = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won","Lost (why?)"]
    #stages_other = ["Lost (why?)"]
    df_junkc = df_junkb.append(df_num[~df_num.Stage.isin(stages)])
    df_num =df_num[df_num.Stage.isin(stages)]


    ### numbers management

    #code examples not used
    #df_num[(df_num["Branch"]=="Austin") & (df_num["Stage"]=="Won")]
    #df_num[df_num["Stage"]=="Lost (why?)"]

    df_noncumun_whole = pd.DataFrame(columns=["PV_sum","EV_sum","PP_mean","Count"])
    df_noncumun_whole[["PV_sum","EV_sum"]] = df_num.groupby("Stage")["PotentialValue","ExpectedValue"].sum()
    df_noncumun_whole["PP_mean"] = df_num.groupby("Stage")[["ProbPercent"]].mean()
    df_noncumun_whole["Count"] = df_num.groupby("Stage")[["Div"]].count()
    df_noncumun_whole





    noncumun_dfs = {}

    for branch in df_num["Branch"].unique():
        df_sum = df_num[df_num["Branch"]==branch].groupby("Stage")["PotentialValue","ExpectedValue"].sum()
        df_mean = df_num[df_num["Branch"]==branch].groupby("Stage")[["ProbPercent"]].mean()
        df_count = df_num[df_num["Branch"]==branch].groupby("Stage")[["Div"]].count()
        #df_sum[["PotentialValue","ExpectedValue"]]

        columns = ["PV_sum","EV_sum","PP_mean","Count"]
        df_branch = pd.DataFrame(columns=columns)
        df_branch[["PV_sum","EV_sum"]] = df_sum[["PotentialValue","ExpectedValue"]]
        df_branch[["PP_mean"]] = df_mean[["ProbPercent"]]
        df_branch[["Count"]] = df_count[["Div"]]
        df_branch = df_branch.round(2)
        
        noncumun_dfs[branch] = df_branch


    stage_list = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"]
    for branch in noncumun_dfs.keys():
        for stage in stage_list:
            if not stage in noncumun_dfs[branch].index:
                noncumun_dfs[branch].loc[stage] = [0,0,0,0]


    stage_dict1 = {"Discovery (S.P.I.N.)":1,
                        "Solution Development":2,
                        "Quoting":3,
                        "Working":4,
                        "On Hold":5,
                        "Won":6,
                        "Lost (why?)":7}
    stage_dict2 = {y:x for x,y in stage_dict1.items()}


    cumun_dfs = {}

    for branch in df_num["Branch"].unique():
        columns = ["PV_cumun","EV_cumun","Count_cumun"]
        df_branch_cumun = pd.DataFrame(columns=columns)
        for stage in df_num["Stage"].unique():
            df_branch_cumun.loc[stage] = [0,0,0]
        cumun_dfs[branch] = df_branch_cumun

    for branch in df_num["Branch"].unique():
    #for branch in df_num[df_num["Branch"]=="Austin"]["Branch"].unique():
        for index,row in noncumun_dfs[branch].iterrows():
                PV_cumun = row["PV_sum"]
                EV_cumun = row["EV_sum"]
                Count_cumun = row["Count"]
                if index != "Lost (why)":
                    for i in range(1,stage_dict1[index] + 1):
                        PV_cumun_temp = PV_cumun
                        EV_cumun_temp = EV_cumun
                        Count_cumun_temp = Count_cumun
                        PV_cumun_temp += cumun_dfs[branch].loc[stage_dict2[i],"PV_cumun"]
                        EV_cumun_temp += cumun_dfs[branch].loc[stage_dict2[i],"EV_cumun"]
                        Count_cumun_temp += cumun_dfs[branch].loc[stage_dict2[i],"Count_cumun"]
                        cumun_dfs[branch].loc[stage_dict2[i]] = [PV_cumun_temp, EV_cumun_temp, Count_cumun_temp]
                else:
                    cumun_dfs[branch].loc[stage_dict2[7]] = [Pv_cumun, EV_cumun, Count_cumun]


    ### Cummunalative: cummun_sum of PV, cummun_sum of EV, cummun_len of rows
    ### Snapshot: sum of PV, sum of EV, avg of PP, len of rows

    return [df, df_num, df_noncumun_whole, noncumun_dfs]

