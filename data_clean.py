'''
Created on 29 Dec, 2015

@author: lab-xu.zeke
'''
def process_train_data(train_path):
    action_train_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/action_train.txt"
    repeat_action_train_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/repeat_action_train.txt"
    lost_uid_train_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/lost_uid_train.txt"
    action_train_fid = open(action_train_path,'w')
    repeat_action_train_fid = open(repeat_action_train_path,'w')
    lost_uid_train_fid = open(lost_uid_train_path,'w')
    train_data = {}
    fid = open(train_path)
    lines = fid.readlines()
    for line in lines:
        data = line.split('\t')
        if len(data[0])==0:
            lost_uid_train_fid.write(line)
        else:
            if (data[0]+data[1]) not in train_data: 
                train_data[data[0]+data[1]] = [line]
            else:
                train_data[data[0]+data[1]].append(line)
    for key in train_data:
        if len(train_data[key]) == 1:
            action_train_fid.write(train_data[key][0])
        else:
            for line in train_data[key]:
                repeat_action_train_fid.write(line)
def create_train_test_id(page_view_data_path):  
    train_id = {}
    test_id = {}
    for i in range(8):
        txt_path = page_view_data_path + "00000" + str(i) + "_0"
        fid = open(txt_path)
        lines = fid.readlines()
        for line in lines:
            data = line.split('\t')
            if data[1]> "20151127":
                if data[0]+data[3] not in test_id:
                    test_id[data[0]+data[3]] = data[0]+'\t'+data[3]+'\t'+data[1]+'\n'
                else:
                    data1 = test_id[data[0]+data[3]].split()
                    if data[1]<data1[2]:
                        test_id[data[0]+data[3]] = data[0]+'\t'+data[3]+'\t'+data[1]+'\n'            
            else:
                if (data[0]+data[3]) not in train_id: 
                    train_id[data[0]+data[3]] = data[0]+'\t'+data[3]+'\t'+data[1]+'\t'+'0'+'\n'
                else:
                    data1 = train_id[data[0]+data[3]].split()
                    if data[1]<data1[2]:
                        train_id[data[0]+data[3]] = data[0]+'\t'+data[3]+'\t'+data[1]+'\t'+'0'+'\n'               
    for key in train_id:
        if key in test_id:
            test_id.pop(key)      
    print "num of train_id is :",len(train_id)   #40181342
    print "num of test_id is :",len(test_id)     #4198135
    action_train_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/action_train.txt"
    fid = open(action_train_path)
    lines = fid.readlines()
    num1 = 0
    num2 = 0
    num3 = 0
    for line in lines:
        data = line.split()
        if (data[0]+data[1]) in train_id:
            num1 += 1
            data1 = train_id[data[0]+data[1]].split()
            if data1[2] == data[3][:8]:
                num3 += 1
            train_id[(data[0]+data[1])] = data1[0]+'\t'+data1[1]+'\t'+data1[2]+'\t'+data[2]+'\t'+data[3]+'\n'
        if (data[0]+data[1]) in test_id:
            num2 += 1
            test_id.pop(data[0]+data[1])
    print "action_num of train_id is:",num1  #292431
    print "action_num of test_id is:",num2   #616
    print "num of action happen on same day is:",num3 #272407
    print "num of train_id is :",len(train_id)   #40181342
    print "num of test_id is :",len(test_id)     #4197519
    train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/train_id.txt"
    test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/test_id.txt"
    train_id_fid = open(train_id_path,'w')
    test_id_fid = open(test_id_path,'w')
    for key in train_id:
        train_id_fid.write(train_id[key])
    for key in test_id:
        test_id_fid.write(test_id[key])
def filter_train_and_test_id(train_id_path,test_id_path):
    train_id_fid = open(train_id_path)
    train_id_lines = train_id_fid.readlines()
    test_id_fid = open(test_id_path)
    test_id_lines = test_id_fid.readlines()
    train_uid_data = {}
    for line in train_id_lines:
        data = line.split('\t')
        if data[0] not in train_uid_data:
            train_uid_data[data[0]] = [int(data[3])]
        else:
            train_uid_data[data[0]].append(int(data[3]))
    no_action_uid = {}
    for key in train_uid_data:
        num = len(train_uid_data[key])
        num0 = train_uid_data[key].count(0)
        if num0/float(num) == 1.0:
            no_action_uid[key] = 1
    filter_train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/filter_train_id.txt"
    filter_train_id_fid = open(filter_train_id_path,'w')
    for line in train_id_lines:
        data = line.split('\t')
        if data[0] not in no_action_uid:
            filter_train_id_fid.write(line)       
    filter_test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/filter_test_id.txt"
    filter_test_id_fid = open(filter_test_id_path,'w')
    for line in test_id_lines:
        data = line.split('\t')
        if data[0] not in no_action_uid:
            filter_test_id_fid.write(line)
def create_model_data(filter_train_id_path,filter_test_id_path):
    train_id_fid = open(filter_train_id_path)
    train_id_lines = train_id_fid.readlines()
    test_id_fid = open(filter_test_id_path)
    test_id_lines = test_id_fid.readlines()
    train_uid = {}
    test_uid = {}
    common_uid = {}
    for line in train_id_lines:
        data = line.split('\t')
        if data[0] not in train_uid:
            train_uid[data[0]] = 1
    for line in test_id_lines:
        data = line.split('\t')
        if data[0] not in test_uid:
            test_uid[data[0]] = 1
    for uid in test_uid:
        if  uid in train_uid:
            common_uid[uid] = 1         
    model_train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id.txt"    
    model_train_id_fid = open(model_train_id_path,'w')
    for line in train_id_lines:
        data = line.split('\t')
        if data[0] in common_uid:
            model_train_id_fid.write(line)     
    model_test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id.txt"
    model_test_id_fid = open(model_test_id_path,'w')
    for line in test_id_lines:
        data = line.split('\t')
        if data[0] in common_uid:
            model_test_id_fid.write(line)
def split_model_data(model_train_id_path,model_test_id_path):
    model_train_id_fid = open(model_train_id_path)
    model_train_id_lines = model_train_id_fid.readlines()
    model_test_id_fid = open(model_test_id_path)
    model_test_id_lines = model_test_id_fid.readlines()
    
    model_train_uid_data = {}
    for line in model_train_id_lines:
        data = line.split('\t')
        if data[0] not in model_train_uid_data:
            model_train_uid_data[data[0]] = [int(data[3])]
        else:
            model_train_uid_data[data[0]].append(int(data[3]))
    no_action_uid = {}
    for key in model_train_uid_data:
        num = len(model_train_uid_data[key])
        num0 = model_train_uid_data[key].count(0)
        if num0/float(num) > 0.98:
            no_action_uid[key] = 1
    model_train_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id1.txt"
    model_train_id1_fid = open(model_train_id1_path,'w')
    model_train_id2_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id2.txt"
    model_train_id2_fid = open(model_train_id2_path,'w')
    for line in model_train_id_lines:
        data = line.split('\t')
        if data[0] not in no_action_uid:
            model_train_id1_fid.write(line)     
        else:
            model_train_id2_fid.write(line)
    model_test_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id1.txt"
    model_test_id1_fid = open(model_test_id1_path,'w')
    model_test_id2_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id2.txt"
    model_test_id2_fid = open(model_test_id2_path,'w')
    for line in model_test_id_lines:
        data = line.split('\t')
        if data[0] not in no_action_uid:
            model_test_id1_fid.write(line)
        else:
            model_test_id2_fid.write(line)
def compute_distribute(train_id_path,test_id_path):
    train_id_fid = open(train_id_path)
    train_id_lines = train_id_fid.readlines()
    train_uid_data = {}
    for line in train_id_lines:
        data = line.split('\t')
        if data[0] not in train_uid_data:
            train_uid_data[data[0]] = [int(data[3])]
        else:
            train_uid_data[data[0]].append(int(data[3]))
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0
    num7 = 0
    num8 = 0
    num9 = 0
    num10 = 0
    uid1 = {}
    uid2 = {}
    uid3 = {}
    uid4 = {}
    uid5 = {}
    for key in train_uid_data:
        num = len(train_uid_data[key])
        num0 = train_uid_data[key].count(0)
        score = num0/float(num)
        if score<0.97:
            num1 += 1
            num6 += num
            uid1[key] = 1
            continue
        if score >=0.97 and score<0.98:
            num2 += 1
            num7 += num
            uid2[key] = 1
            continue
        if score >=0.98 and score<0.99:
            num3 += 1
            num8 += num
            uid3[key] = 1
            continue
        if score >=0.99 and score<1.0:
            num4 += 1
            num9 += num
            uid4[key] = 1
        if score >=1.0:
            num5 += 1
            num10 += num
            uid5[key] = 1
            continue
    print num1,num2,num3,num4,num5,num6,num7,num8,num9,num10 
    test_id_fid = open(test_id_path)
    test_id_lines = test_id_fid.readlines()
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0
    for line in test_id_lines:
        data = line.split()
        if data[0] in uid1:
            num1 += 1
            continue
        if data[0] in uid2:
            num2 += 1
            continue
        if data[0] in uid3:
            num3 += 1
            continue
        if data[0] in uid4:
            num4 += 1
            continue
        if data[0] in uid5:
            num5 += 1
            continue
        num6 += 1
    print num1,num2,num3,num4,num5,num6  
def compute_common_uid(train_id_path,test_id_path):
    train_id_fid = open(train_id_path)
    train_id_lines = train_id_fid.readlines()
    test_id_fid = open(test_id_path)
    test_id_lines = test_id_fid.readlines()
    train_uid = {}
    test_uid = {}
    for line in train_id_lines:
        data = line.split('\t')
        if data[0] not in train_uid:
            train_uid[data[0]] = 1
    for line in test_id_lines:
        data = line.split('\t')
        if data[0] not in test_uid:
            test_uid[data[0]] = 1
    common_num = 0
    for uid in test_uid:
        if  uid in train_uid:
            common_num += 1 
    print "the uid_num of train_id is:",len(train_uid)
    print "the uid_num of test_id is:",len(test_uid)
    print "the common uid_num from train and model1 is :",common_num
def compute_common_cid(train_id_path,test_id_path):
    train_id_fid = open(train_id_path)
    train_id_lines = train_id_fid.readlines()
    test_id_fid = open(test_id_path)
    test_id_lines = test_id_fid.readlines()
    train_cid = {}
    test_cid = {}
    for line in train_id_lines:
        data = line.split('\t')
        if data[1] not in train_cid:
            train_cid[data[1]] = 1
    for line in test_id_lines:
        data = line.split('\t')
        if data[1] not in test_cid:
            test_cid[data[1]] = 1
    common_num = 0
    for cid in test_cid:
        if  cid in train_cid:
            common_num += 1 
    print "the cid_num of train_id is:",len(train_cid)
    print "the cid_num of test_id is:",len(test_cid)
    print "the common cid_num from train and model1 is :",common_num
if __name__ == "__main__":
    train_path = "/home/lab-xu.zeke/ZakeXu/proj/data/train.txt"
    page_view_data_path = "/home/lab-xu.zeke/ZakeXu/proj/data/page_view_data/race_data/"
    train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/train_id.txt"
    test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/test_id.txt"
    filter_train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/filter_train_id.txt"
    filter_test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/filter_test_id.txt"
    model_train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id.txt"
    model_test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id.txt" 
    model_train_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id1.txt"
    model_test_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id1.txt"
    model_train_id2_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id2.txt"
    model_test_id2_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id2.txt"
    
    #process_train_data(train_path)
    create_train_test_id(page_view_data_path)
    compute_common_uid(train_id_path,test_id_path)                #113679 68027 66874
    compute_common_cid(train_id_path,test_id_path)                #78596 24670 19394
    
    filter_train_and_test_id(train_id_path,test_id_path)
    compute_distribute(train_id_path,test_id_path)   
    compute_common_uid(filter_train_id_path,filter_test_id_path)  #96389 58141 56988
    compute_common_cid(filter_train_id_path,filter_test_id_path)  #77176 21461 16710
    
    create_model_data(filter_train_id_path,filter_test_id_path)
    compute_common_uid(model_train_id_path,model_test_id_path)    #56988 56988 56988
    compute_common_cid(model_train_id_path,model_test_id_path)    #68314 20700 16010 
    
    split_model_data(model_train_id_path,model_test_id_path)      
    compute_common_uid(model_train_id1_path,model_test_id1_path)  #6504 6504 6504
    compute_common_uid(model_train_id2_path,model_test_id2_path)  #50484 50484 50484
