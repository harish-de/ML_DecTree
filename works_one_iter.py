import pandas as pd
import math

df = pd.read_csv("car.csv",delimiter=',',header=None)
df = df.add_prefix('att')
rows, cols = df.shape
old_value = 'att' + str(cols-1)
df.rename(columns={ old_value: 'target' }, inplace=True)
#print(df.head())

df_label = df['target']
labels = df_label.value_counts()
log_base = len(labels)

parent_entropy = 0.0
for label_count in labels:
    parent_entropy += (label_count/rows) * math.log((label_count/rows),log_base)

parent_entropy = -parent_entropy
#print(parent_entropy)
attr_entropies = []
attr_entropy_list = []
for col in df.columns[0:-1]:
    df_temp = df[col]
    attr_values = df_temp.value_counts()


    attr_entropy = 0.0


    for attr_val in attr_values.keys():
        df_new = df.loc[df[col] == attr_val]
        row_attr_val, col_attr_val = df_new.shape

        label_attr_count = df_new['target'].value_counts()
        label_names = list(label_attr_count.keys())
        node_entropy = 0.0
        iter = 0

        for count in label_attr_count:
            label = label_names[iter]
            temp = (count/row_attr_val) * math.log((count/row_attr_val),log_base)
            if(temp != abs(0.0)):
                temp = -temp

            str_value = str(col) + ':' + str(attr_val) + ':' + str(temp) + ':' + str(label)
            attr_entropy_list.append(str_value)
            node_entropy += temp
            iter += 1
        #node_entropy = -node_entropy
        attr_entropy +=  (row_attr_val/rows)*node_entropy

    attr_entropies.append(str(col) + ":" + str(attr_entropy))
    #print(attr_entropy_list)

#print(attr_entropies)

info_gain = []
for each_attr_gain in attr_entropies:
    col_name, entropy = each_attr_gain.split(sep=':')
    col_gain = parent_entropy - float(entropy)
    info_gain.append(str(col_name) + ':' + str(col_gain))

max = 0.0
for gain in info_gain:
    col_name, gain_value = gain.split(sep=':')
    if(float(gain_value) >= max):
        max = float(gain_value)
        max_col = col_name

low = 0.0
for attr_entropy_vals in attr_entropy_list:
    att_name, att_val, att_entropy, label_node = attr_entropy_vals.split(sep = ':')
    if(att_name == max_col):
        if(float(att_entropy) == low):
            #<node entropy="0.0" value="low" feature="att5">unacc</node>
            print(attr_entropy_vals)

#print(max_col)
#print(attr_entropy_list)

#print(info_gain)
    #print(str(col) + ' = ' + str(attr_entropy))
    #print(attr_entropy_list)
    #print(attr_values)


#print(labels)
#print(df_label.head())