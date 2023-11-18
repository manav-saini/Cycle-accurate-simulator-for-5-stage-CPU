arr_sim={
    '000':[],
    '001':[],
    '010':[],
    '011':[],
    '100':[],
}

reg_sim={
    '000':0,
    '001':0,
    '010':0,
    '011':0,
    '100':0,
}

f=open('D:\Download\Cycle-accurate-simulator-for-5-stage-CPU-main\Cycle-accurate-simulator-for-5-stage-CPU-main\SIMD\/binn.txt', 'r')
arrays=[]
for istr in f:
    iarr=[istr[i:i+3] for i in range(0, len(istr), 3)]
    iarr.pop()
    print(iarr)
    if iarr[0]=='000':
        n=int(iarr[2], 2)
        buff=[]
        for i in range(n):
            buff.append(int(iarr[3+i], 2))
        arr_sim[iarr[1]]=buff
    if iarr[0] == '010':
        for i in range(len(arr_sim[iarr[2]])):
            arr_sim[iarr[1]].append(arr_sim[iarr[2]][i]+arr_sim[iarr[3]][i])
    if iarr[0] == '011':
        for i in range(len(arr_sim[iarr[2]])):
            arr_sim[iarr[1]].append(arr_sim[iarr[2]][i]-arr_sim[iarr[3]][i])
    if iarr[0]== '100':
        x=int(iarr[3], 2)
        for i in range(len(arr_sim[iarr[2]])):
            arr_sim[iarr[1]].append(arr_sim[iarr[2]][i]+x)
    if iarr[0]=='001':
        # print(int(iarr[1], 2))
        index=int(iarr[1], 2)//4
        reg_sim[iarr[3]]=arr_sim[iarr[2]][index]