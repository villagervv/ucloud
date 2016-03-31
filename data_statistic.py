'''
Created on 28 Dec, 2015

@author: lab-xu.zeke
'''
def load_page_view_data(path):
    #load data
    uid = []
    cid = []
    uc_id = []
    num = 0
    num1 = 0
    for i in range(8):
        txt_path = path + "00000" + str(i) + "_0"
        fid = open(txt_path)
        lines = fid.readlines()
        num = num + len(lines)
        for line in lines:
            data = line.split()
            uid.append(data[0])           
            cid.append(data[3])            
            uc_id.append(data[0]+data[3])  
            if len(data) != 7:
                print "error"
            if (int(data[4]) != 1) and (int(data[4]) != 2):
                print "error"    
            if (int(data[5]) == 0) and (int(data[6]) == 0):
                print "error"
            if (int(data[5]) == 0) and (int(data[6]) > 0):
                num1 += 1 
    #data statistic
    print "num of page view data is:",num                     #95416395
    print "num of uid is:",len(set(uid))                      #114832
    print "num of cid is:",len(set(cid))                      #83873
    print "num of uc_id data is:",len(set(uc_id))             #44379477
    print "num of error data is:",num1                        #2915196
def load_train(path):
    #load data
    fid = open(path)
    lines = fid.readlines()
    numOfEmptyUid = 0
    uid = []
    cid = []
    uc_id = []
    for line in lines:
        data = line.split('\t')
        if len(data[0])==0:
            numOfEmptyUid += 1
        else: 
            uid.append(data[0])           
            cid.append(data[1])      
            uc_id.append(data[0]+data[1]) 
    #data statistic
    print "num of train is:",len(lines)                        #474564
    print "num of dev_id is:",len(set(uid))                    #142670
    print "num of post_id is:",len(set(cid))                   #30348
    print "num of empty dev_id is:", numOfEmptyUid             #791
    print "num of dev_post_id data is:",len(set(uc_id))        #473375
def load_post_data(path):
    #load data
    fid = open(path)
    lines = fid.readlines()
    cid = []
    cid_title = []
    cid_content = []
    for line in lines:
        data = line.split('\t')
        cid.append(data[0])
        cid_title.append(data[1])
        cid_content.append(data[2].strip())
    cid = cid[1:]
    cid_title = cid_title[1:]
    cid_content = cid_content[1:]
    #data statistic
    print "num of cid is:",len(cid)                    #83836
    numOfTitle = 0
    for title in cid_title:
        if len(title)>0:
            numOfTitle += 1
    print "num of cid with title is:", numOfTitle      #2508
    numOfContent = 0
    for content in cid_content:
        if len(content)>0:
            numOfContent += 1
    print "num of cid with content is:", numOfContent  #75283


if __name__ == "__main__":
    post_data_path = "/home/lab-xu.zeke/ZakeXu/proj/data/post_data.txt"
    page_view_data_path = "/home/lab-xu.zeke/ZakeXu/proj/data/page_view_data/race_data/"
    train_path = "/home/lab-xu.zeke/ZakeXu/proj/data/train.txt"
    load_page_view_data(page_view_data_path)
    load_train(train_path)
    load_post_data(post_data_path)
