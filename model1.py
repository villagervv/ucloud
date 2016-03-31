'''
Created on 1 Jan, 2016

@author: lab-xu.zeke
'''
from numpy import *
import random
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
import numpy as np
from sklearn.linear_model import logistic
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble.forest import RandomForestClassifier
def rand_prob(rate,day,sample_type):
    if sample_type == "time":
        if random.randint(1,rate+(14-day)*8)<=12 and day>14:
            return 1
        else:
            return 0
    if sample_type == "no_time":
        if random.randint(1,40)<=1 and day>14:
            return 1
        else:
            return 0
def sample_ifaction_train_data(model_train_id_path):
    ifaction_train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/ifaction_train_id1.txt"
    ifaction_train_id_fid = open(ifaction_train_id_path,'w')
    fid = open(model_train_id_path)
    lines = fid.readlines()
    pos_num = 0
    neg_num = 0
    for line in lines:
        data = line.split()
        if int(data[3])>0:
            ifaction_train_id_fid.write(data[0]+'\t'+data[1]+'\t'+data[2]+'\t'+'1'+'\t'+data[4]+'\n')
            pos_num += 1
        else:
            if rand_prob(150,int(data[2][6:]),"no_time") == 1:
                ifaction_train_id_fid.write(line)
                neg_num += 1
    print "num of pos train is:", pos_num
    print "num of neg train is:", neg_num
def extract_uid_cid_feat(id_path,page_view_data_path): 
    id_fid = open(id_path)
    id_lines = id_fid.readlines()
    uid_cid ={}
    for line in id_lines:
        data = line.split()
        uid_cid[data[0]+data[1]] = data[2]
    uid_cid_data = {}
    for i in range(8):
        txt_path = page_view_data_path + "00000" + str(i) + "_0"
        fid = open(txt_path)
        lines = fid.readlines()   
        for line in lines:
            data = line.split('\t')
            if (data[0]+data[3]) in uid_cid:
                if (data[0]+data[3]) not in uid_cid_data:
                    uid_cid_data[data[0]+data[3]] = [[int(data[5])],[int(data[6])]]
                else:
                    uid_cid_data[data[0]+data[3]][0].append(int(data[5]))        
                    uid_cid_data[data[0]+data[3]][1].append(int(data[6]))   
    uid_cid_feat = {}
    for uc_id in uid_cid:
        feat = [uid_cid[uc_id][6:]]
        uid_cid_feat[uc_id] = feat
        if uc_id in uid_cid_data:
            num_of_interaction = len(uid_cid_data[uc_id][0])
            sum_of_view = sum(uid_cid_data[uc_id][0])
            sum_of_click = sum(uid_cid_data[uc_id][1])
            mean_of_view = sum_of_view/float(num_of_interaction)
            mean_of_click = sum_of_click/float(num_of_interaction)
            uid_cid_feat[uc_id].extend([num_of_interaction,sum_of_view,sum_of_click,mean_of_view,mean_of_click])
        else:
            uid_cid_feat[uc_id].extend([0]*5)
    return uid_cid_feat 
def extract_all_feat(id_path,uid_feat_path,txt_feat_path,cluster_feat_path,uid_cid_feat):
    uid_feat_fid = open(uid_feat_path)
    uid_feat_lines = uid_feat_fid.readlines()
    uid_feat = {}
    for line in uid_feat_lines:
        data = line.split()
        uid_feat[data[0]] = data[1:] 
    txt_feat_fid = open(txt_feat_path)
    txt_feat_lines = txt_feat_fid.readlines()
    txt_feat = {}
    for line in txt_feat_lines:
        data = line.split()
        txt_feat[data[0]] = data[1:]
    cluster_feat_fid = open(cluster_feat_path)
    cluster_feat_lines = cluster_feat_fid.readlines()
    cluster_feat = {}
    for line in cluster_feat_lines:
        data = line.split()
        cluster_feat[data[0]] = data[1:]
    id_fid = open(id_path)
    id_lines = id_fid.readlines()
    all_feat = {}
    for line in id_lines:
        data = line.split()
        if (data[0]+data[1]) not in all_feat:
            all_feat[data[0]+data[1]] = [data[0]+data[1]]
            all_feat[data[0]+data[1]].extend(uid_cid_feat[data[0]+data[1]])
            if data[0] in uid_feat:
                all_feat[data[0]+data[1]].extend(uid_feat[data[0]])
            else:
                all_feat[data[0]+data[1]].extend(['0']*14)
            if data[1] in txt_feat:
                all_feat[data[0]+data[1]].extend(txt_feat[data[1]])
            else:
                all_feat[data[0]+data[1]].extend(['0']*203)
            if data[1] in cluster_feat:
                all_feat[data[0]+data[1]].extend(cluster_feat[data[1]])
            else:
                all_feat[data[0]+data[1]].extend(['0']*300)
    return all_feat  
def save_feat(ifaction_train_id_path,all_train_feat,all_test_feat):
    ifaction_train_id_fid = open(ifaction_train_id_path)
    ifaction_train_id_lines = ifaction_train_id_fid.readlines()
    train_label = {}
    for line in ifaction_train_id_lines:
        data = line.split()
        train_label[data[0]+data[1]] = data[3]
    ifaction_train_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/ifaction_train_feat1.txt"
    ifaction_train_feat_fid = open(ifaction_train_feat_path,'w')
    for uc_id in all_train_feat:
        feat = [str(i) for i in all_train_feat[uc_id]]
        if len(feat) != 524:
            print "error"
        feat.append(train_label[uc_id])
        ifaction_train_feat_fid.write('\t'.join(feat)+'\n')  
    ifaction_test_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/ifaction_test_feat1.txt"
    ifaction_test_feat_fid = open(ifaction_test_feat_path,'w')
    for uc_id in all_test_feat:
        feat = [str(i) for i in all_test_feat[uc_id]]
        if len(feat) != 524:
            print "error"
        ifaction_test_feat_fid.write('\t'.join(feat)+'\n') 
def create_input_output(train_feat_path,test_feat_path,feat_type):
    train_feat_fid = open(train_feat_path)
    train_feat_lines = train_feat_fid.readlines()
    trainX = []
    trainY = []
    for line in train_feat_lines:
        data = line.split('\t')
        trainY.append(int(data[-1]))
        if feat_type == "statistic_feat":
            trainX.append(data[1:21])
        if feat_type == "statistic_topic_feat":
            trainX.append(data[1:21]+data[21:24]+data[24:224])
        if feat_type == "statistic_cluster_feat":
            trainX.append(data[1:21]+data[21:24]+data[224:524])
        if feat_type == "all":
            trainX.append(data[1:-1])
    test_feat_fid = open(test_feat_path)
    test_feat_lines = test_feat_fid.readlines()
    testX = []
    for line in test_feat_lines:
        data = line.split('\t')
        if feat_type == "statistic_feat":
            testX.append(data[1:21])
        if feat_type == "statistic_topic_feat":
            testX.append(data[1:21]+data[21:24]+data[24:224])
        if feat_type == "statistic_cluster_feat":
            testX.append(data[1:21]+data[21:24]+data[224:524])
        if feat_type == "all":
            testX.append(data[1:])
    print "feature dim is:",array(trainX).shape
    return trainX,trainY,testX 
def model_pred(trainX,trainY,testX,model_type):
    if model_type == "rf":
        clf = RandomForestClassifier(n_estimators = 500,n_jobs = 20)
        clf.fit(trainX,trainY)
        pred = clf.predict(testX)
    if model_type == "gbdt":
        clf = GradientBoostingClassifier(n_estimators=6,learning_rate=0.9,random_state=0)
        clf.fit(trainX,trainY)
        pred = clf.predict(testX)
    if model_type == "fusion":
        prob = np.zeros(len(testX))
        params = [100,200,300,400,500]
        for param in params:
            clf = RandomForestClassifier(n_estimators = param,n_jobs = 20,bootstrap=True)
            clf.fit(trainX,trainY)
            prob += clf.predict(testX)
        '''
        params = [1,2,3,4,5,6,7,8,9,10]
        for param in params:
            clf = GradientBoostingClassifier(n_estimators=param,learning_rate=0.9,random_state=0)
            clf.fit(trainX,trainY)
            prob += clf.predict(testX)
        '''
        pred = list(prob >= 3)
    print "the pos rate is:",float(sum(pred))/len(pred)
    return pred
def create_result(pred,test_id_path,test_feat_path):
    test_feat_fid = open(test_feat_path)
    test_feat_lines = test_feat_fid.readlines()
    label = {}
    index = 0
    for line in test_feat_lines:
        data = line.split()
        label[data[0]] = pred[index]
        index += 1
    test_id_fid = open(test_id_path)
    test_id_lines = test_id_fid.readlines()
    action_test_id_path = "/home/lab-xu.zeke/ZakeXu/proj/result/action_test_id1.txt"
    action_test_id_fid = open(action_test_id_path,'w')
    for line in test_id_lines:
        data = line.split()
        if label[data[0]+data[1]] == 1:
            action_test_id_fid.write(line)    
def compute_uid_action(train_id_path):
    fid = open(train_id_path)
    lines = fid.readlines()
    uid_data = {}
    uid_action = {}
    for line in lines:
        data = line.split('\t')
        if data[0] not in uid_data:
            uid_data[data[0]] = [int(data[3])]
        else:
            uid_data[data[0]].append(int(data[3]))
    for key in uid_data:
        num1 = float(uid_data[key].count(1))
        num2 = float(uid_data[key].count(2))
        if num1>num2:
            uid_action[key] = 1
        else:
            uid_action[key] = 2
    return uid_action
def predict(test_id_path,uid_action):
    save_path = "/home/lab-xu.zeke/ZakeXu/proj/result/result_rules1.txt"
    save_fid = open(save_path,'w')
    test_fid = open(test_id_path)
    test_lines = test_fid.readlines()
    for line in test_lines:
        data = line.split()
        if data[0] in uid_action:
            save_fid.write(data[0]+'\t'+data[1]+'\t'+str(uid_action[data[0]])+'\n')    
if __name__ == "__main__":
    page_view_data_path = "/home/lab-xu.zeke/ZakeXu/proj/data/page_view_data/race_data/"
    model_train_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id1.txt"
    ifaction_train_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/ifaction_train_id1.txt"
    model_test_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_test_id1.txt"
    uid_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/uid_feat.txt"
    txt_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/txt_feat.txt"
    cluster_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/cluster_feat.txt"
    ifaction_train_feat1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/ifaction_train_feat1.txt"
    ifaction_test_feat1_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/ifaction_test_feat1.txt"
    action_test_id1_path = "/home/lab-xu.zeke/ZakeXu/proj/result/action_test_id1.txt"
    '''
    print "sample..."
    sample_ifaction_train_data(model_train_id1_path)
    '''
    print "extract uid_cid feat of train..."
    uid_cid_feat  = extract_uid_cid_feat(ifaction_train_id1_path,page_view_data_path)
    print "extract all_feat of train..."
    all_train_feat = extract_all_feat(ifaction_train_id1_path,uid_feat_path,txt_feat_path,cluster_feat_path,uid_cid_feat)
    print "extract uid_cid feat of test..."
    uid_cid_feat  = extract_uid_cid_feat(model_test_id1_path,page_view_data_path)
    print "extract all_feat of test..."
    all_test_feat = extract_all_feat(model_test_id1_path,uid_feat_path,txt_feat_path,cluster_feat_path,uid_cid_feat)
    print "save feat..."
    save_feat(ifaction_train_id1_path,all_train_feat,all_test_feat)
    
    print "create input and output of model..."
    trainX,trainY,testX = create_input_output(ifaction_train_feat1_path,ifaction_test_feat1_path,"statistic_topic_feat")
    print "model pred..."
    pred = model_pred(trainX,trainY,testX,'rf')
    print "create_result..."
    create_result(pred,model_test_id1_path,ifaction_test_feat1_path)
    print "submit..."
    uid_action = compute_uid_action(model_train_id1_path)
    predict(action_test_id1_path,uid_action)
    print "finish..."
