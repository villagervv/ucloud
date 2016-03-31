'''
Created on 30 Dec, 2015

@author: lab-xu.zeke
'''
from numpy import *
def extract_uid_feat(model_train_id_path,page_view_data_path):
    uid_feat = {}
    uid_data_all = {}
    model_train_id_fid = open(model_train_id_path)
    model_train_id_lines = model_train_id_fid.readlines()
    for line in model_train_id_lines:
        data = line.split()
        if data[0] not in uid_data_all:
            uid_data_all[data[0]] = [int(data[3])]
        else:
            uid_data_all[data[0]].append(int(data[3]))
    for uid in uid_data_all:  #9 dim
        num_of_cid = len(uid_data_all[uid])
        num_of_like = uid_data_all[uid].count(1)
        num_of_unlike = uid_data_all[uid].count(2)
        num_of_action = num_of_like + num_of_unlike
        num_of_nonaction = num_of_cid - num_of_action
        rate_of_like = num_of_like/float(num_of_cid)
        rate_of_unlike = num_of_unlike/float(num_of_cid)
        rate_of_action = num_of_action/float(num_of_cid)
        rate_of_nonaction = num_of_nonaction/float(num_of_cid)
        uid_feat[uid] = [num_of_cid,num_of_like,num_of_unlike,num_of_action,num_of_nonaction,rate_of_like,rate_of_unlike,rate_of_action,rate_of_nonaction]   
    uid_data_all = {}
    for i in range(8):
        txt_path = page_view_data_path + "00000" + str(i) + "_0"
        fid = open(txt_path)
        lines = fid.readlines()   
        for line in lines:
            data = line.split('\t')
            if data[0] in uid_feat:
                if data[1] < "20151128":
                    if data[0] not in uid_data_all:
                        uid_data_all[data[0]] = [[int(data[4])],[int(data[5])],[int(data[6])]]
                    else:
                        uid_data_all[data[0]][0].append(int(data[4]))
                        uid_data_all[data[0]][1].append(int(data[5]))
                        uid_data_all[data[0]][2].append(int(data[6]))
    for uid in uid_data_all: #5 dim
        frequent_type = int(round(array(uid_data_all[uid][0]).mean()))
        sum_of_view = sum(uid_data_all[uid][1])
        sum_of_click = sum(uid_data_all[uid][2])
        mean_of_view = sum_of_view/float(uid_feat[uid][0]+1.0)
        mean_of_click = sum_of_click/float(uid_feat[uid][0]+1.0)
        uid_feat[uid].extend([frequent_type,sum_of_view,sum_of_click,mean_of_view,mean_of_click])
    uid_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/uid_feat.txt"
    uid_feat_fid = open(uid_feat_path,'w')
    for uid in uid_feat: #14 dim
        feat = [str(i) for i in uid_feat[uid]]
        if len(feat)!= 14:
            print "error"
        uid_feat_fid.write(uid+'\t'+'\t'.join(feat)+'\n')
def extract_cid_feat(train_id_path,page_view_data_path):
    cid_feat = {}
    train_id_fid = open(train_id_path)
    train_id_lines = train_id_fid.readlines()
    cid_data_all = {}
    for line in train_id_lines:
        data = line.split()
        if data[1] not in cid_data_all:
            cid_data_all[data[1]] = [int(data[3])]
        else:
            cid_data_all[data[1]].append(int(data[3]))
    for cid in cid_data_all: #9 dim
        num_of_uid = len(cid_data_all[cid])
        num_of_like = cid_data_all[cid].count(1)
        num_of_unlike = cid_data_all[cid].count(2)
        num_of_action = num_of_like + num_of_unlike
        num_of_nonaction = num_of_uid - num_of_action
        rate_of_like = num_of_like/float(num_of_uid)
        rate_of_unlike = num_of_unlike/float(num_of_uid)
        rate_of_action = num_of_action/float(num_of_uid)
        rate_of_nonaction = num_of_nonaction/float(num_of_uid)
        cid_feat[cid] = [num_of_uid,num_of_like,num_of_unlike,num_of_action,num_of_nonaction,rate_of_like,rate_of_unlike,rate_of_action,rate_of_nonaction]
    cid_data_all = {}
    for i in range(8):
        txt_path = page_view_data_path + "00000" + str(i) + "_0"
        fid = open(txt_path)
        lines = fid.readlines()   
        for line in lines:
            data = line.split('\t')
            if data[3] in cid_feat:
                if data[1] < "20151128":
                    if data[3] not in cid_data_all:
                        cid_data_all[data[3]] = [[int(data[4])],[int(data[5])],[int(data[6])]]
                    else:
                        cid_data_all[data[3]][0].append(int(data[4]))
                        cid_data_all[data[3]][1].append(int(data[5]))
                        cid_data_all[data[3]][2].append(int(data[6]))
    for cid in cid_data_all: #5 dim
        cid_type = cid_data_all[cid][0][0]
        sum_of_view = sum(cid_data_all[cid][1])
        sum_of_click = sum(cid_data_all[cid][2])
        mean_of_view = float(sum_of_view)/cid_feat[cid][0]
        mean_of_click = float(sum_of_click)/cid_feat[cid][0]
        cid_feat[cid].extend([cid_type,sum_of_view,sum_of_click,mean_of_view,mean_of_click])
    cid_feat_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/cid_feat.txt"
    cid_feat_fid = open(cid_feat_path,'w')
    for cid in cid_feat: #14 dim
        feat = [str(i) for i in cid_feat[cid]]
        if len(feat)!= 14:
            print "error"
        cid_feat_fid.write(cid+'\t'+'\t'.join(feat)+'\n')   
if __name__ == "__main__":
    page_view_data_path = "/home/lab-xu.zeke/ZakeXu/proj/data/page_view_data/race_data/"
    model_train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/model_train_id.txt"
    train_id_path = "/home/lab-xu.zeke/ZakeXu/proj/data/self/train_id.txt"
    print "extract uid feat..."
    extract_uid_feat(model_train_id_path,page_view_data_path) 
    #print "extract cid feat..."
    #extract_cid_feat(model_train_id_path,page_view_data_path)
