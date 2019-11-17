import pandas as pd
import math
import csv

def calc_node_entropy(df):
    rows, cols = df.shape
    df_label = df['target']
    labels = df_label.value_counts()
    log_base = get_log_base()
    parent_entropy = 0.0
    for label_count in labels:
        parent_entropy += ((label_count / rows) * math.log((label_count / rows), log_base))
    parent_entropy = -parent_entropy
    return parent_entropy

def decision_tree(df, parent_entropy):
    attr_entropies = []
    attr_entropy_list = []
    info_gain = []
    log_base = get_log_base()
    for col in df.columns[0:-1]:
        df_temp = df[col]
        a,b =calc_attr_entr_gain(df_temp,col, parent_entropy,log_base)
        attr_entropy_list.append(a)
        info_gain.append(b)

    max = 0.0
    for index in range(0,len(info_gain)):
        col_name, gain_val = info_gain[index].split(sep=':')
        if (float(gain_val) >= max):
            max = float(gain_val)
            max_col = col_name


    attr_unique_vals = get_unique_values(df, max_col)

    order = []
    sorted_entropy = []
    for x in range(0, len(attr_unique_vals)):
        order = attr_entropy_list[int(max_col[3])][x].split(sep=':')
        sorted_entropy.append(order)

    sorted_entropy = sorted(sorted_entropy, key=lambda x:x[0], reverse=False)
    print(sorted_entropy)

    for vals in range(0,len(attr_unique_vals)):

        result = sorted_entropy[vals]
        if(float(result[0]) == abs(0.0)):
            with open('car.xml', "a") as text_file:
                print("<node entropy=\"" + str(float(result[0])) +
                      "\" feature=\"" + str(max_col) +
                      "\" value=\"" + str(result[2]) +
                      "\">" + str(result[1]) +
                      "</node>", end="\n", file=text_file, flush=True)

        else:
            with open('car.xml', "a") as text_file:
                print("<node entropy=\"" + str(float(result[0])) +
                      "\" feature=\"" + str(max_col) +
                      "\" value=\"" + str(result[2]) +
                      "\">", end="\n", file=text_file, flush=True)

            reduced_df = df.loc[df[max_col] == str(result[2])]
            deleted_df = delete_column(reduced_df, max_col)
            entropy_new = calc_node_entropy(deleted_df)
            decision_tree(deleted_df,entropy_new)
            with open('car.xml', "a") as text_file:
                print("</node>", end="\n", file=text_file)


def get_unique_values(df, max_col):
    #attr_unique_vals = df[max_col].value_counts()
    attr_unique_vals = df[max_col].unique()
    return attr_unique_vals


def delete_column(df_next, max_col):
    del df_next[max_col]
    return df_next


def calc_attr_entr_gain(df_temp,col, parent_entropy,log_base):
    attr_values = df_temp.value_counts()
    each_entropy = []
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
            temp = (count / row_attr_val) * math.log((count / row_attr_val), log_base)
            if (temp != abs(0.0)):
                temp = -temp


            #str_value = str(col) + ':' + str(attr_val) + ':' + str(temp) + ':' + str(label)
            node_entropy += temp
            iter += 1

        each_entropy.append(str(node_entropy)+ ':' + str(label) + ':' + str(attr_val))
        attr_entropy += (row_attr_val / rows) * node_entropy
    gain = col + ':' + str(parent_entropy - attr_entropy)
    return each_entropy,gain


def get_log_base():
    global df, rows, cols, old_value
    df = pd.read_csv("car.csv", delimiter=',', header=None)
    df = df.add_prefix('att')
    rows, cols = df.shape
    old_value = 'att' + str(cols - 1)
    df.rename(columns={old_value: 'target'}, inplace=True)
    unique_labels = df['target'].unique()
    return len(unique_labels)


df = pd.read_csv('car.csv',delimiter=',', header=None)
df = df.add_prefix('att')
rows, cols = df.shape
old_value = 'att' + str(cols-1)
df.rename(columns={ old_value: 'target' }, inplace=True)
node_ent_val = calc_node_entropy(df)

with open('car.xml', "w") as text_file:
    print("<tree entropy=\"" + str(node_ent_val) + "\">", end="\n", file=text_file)
decision_tree(df,node_ent_val)
with open('car.xml', "a") as text_file:
    print("</tree>", file=text_file)

