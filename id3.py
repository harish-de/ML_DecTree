import csv
import pandas as pd
import math

def read_csv_file():
    df_complete = pd.read_csv('car.csv', delimiter=',', header=None)
    df_complete = df_complete.add_prefix('att')
    df_complete.rename(columns={'att' + str(df_complete.shape[1] - 1): 'target_label'}, inplace=True)
    return df_complete


df_input_file = read_csv_file()
log_base = 0

def calc_log_base(df_unique_labels):
    return len(df_unique_labels['target_label'].unique())

log_p = calc_log_base(df_unique_labels=df_input_file)

def calc_entropy_per_attr(df_target_labels, log_base):
    label_distribution = df_target_labels['target_label'].value_counts()
    r_a, c_a = df_target_labels.shape

    entropy = 0.0
    for l in label_distribution:
        if(l == r_a):
            entropy = 0
        else:
            entropy += - (l/r_a) * math.log((l/r_a),log_base)

    return entropy

tree_entropy = calc_entropy_per_attr(df_input_file,log_p)

with open('harish.xml', "w") as text_file:
    print("<tree entropy=\"" + str(tree_entropy) + "\">", end="\n", file=text_file)

def omit_delete_columns(entropys, gains, df_omit_delete):
    best_column_index = gains.index(max(gains))
    column_name = df_omit_delete.columns[best_column_index]
    values_in_best_node = df_omit_delete[column_name].unique()

    for vals in values_in_best_node:

        entropies = entropys[best_column_index]

        for e in entropies:
            ent_attr_values = e.split(':')
            if(ent_attr_values[0] == vals):
                break

        if(float(ent_attr_values[1]) == 0.0):

            df_temp = df_omit_delete.loc[df_omit_delete[column_name] == ent_attr_values[0]]

            with open('harish.xml', "a") as text_file:
                print("<node entropy=\"" + str(0.0) +
                      "\" value=\"" + vals +
                      "\" feature=\"" + column_name +
                      "\">" + str(df_temp['target_label'].unique()) +
                      "</node>", end="\n", file=text_file, flush=True)

        else:

            with open('harish.xml', "a") as text_file:
                print("<node entropy=\"" + str(float(ent_attr_values[1])) +
                      "\" value=\"" + vals +
                      "\" feature=\"" + column_name  +
                      "\">", end="\n", file=text_file, flush=True)


            omit_df = df_omit_delete.loc[df_omit_delete[column_name] == vals]
            del omit_df[column_name]

            node_entropy = calc_entropy_per_attr(omit_df, log_p)
            build_decision_tree(omit_df, node_entropy)

            with open('harish.xml', "a") as text_file:
                print("</node>", end="\n", file=text_file)

def build_decision_tree(df_tree, parent_entropy):

    entropies_list = []
    information_gain = []

    r_o, c_o = df_tree.shape

    for x in df_tree.columns[0:-1]:
        entropies = []
        x_values = df_tree[x].value_counts()

        entropy_attribute = 0.0
        for x_val in x_values.keys():
            labels = df_tree.loc[df_tree[x] == x_val]
            r_v, c_v = labels.shape

            entropy_attribute += (r_v/r_o) * calc_entropy_per_attr(labels,log_p)
            entropies.append(x_val + ':' + str(calc_entropy_per_attr(labels,log_p)))

        entropies_list.append(entropies)
        information_gain_attribute = parent_entropy - entropy_attribute
        information_gain.append(information_gain_attribute)

    omit_delete_columns(entropies_list, information_gain, df_tree)

build_decision_tree(df_input_file, tree_entropy)

with open('harish.xml', "a") as text_file:
    print("</tree>", file=text_file)







