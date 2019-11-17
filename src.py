import pandas as pd
import math

def find_next_node(df,cols_in_df,log_base,last_col):
    # print(df.shape)
    # rows_in_df, cols_in_df = df.shape
    # last_col = cols_in_df-1
    # labels = df[last_col]
    # unique_labels = labels.value_counts()
    # log_base = len(unique_labels)
    p_i = log_base
    target = last_col

    entropy_result = 0.0
    global attr_val_result
    global attr_result
    global label_result

    cols = list(df)
    #print(cols)
    #for col in range(cols_in_df-1):                         # get the shape of attribute eg.Sky
    for col in df:

        if col != last_col:
            df_attr = df[col]
            attr_distinct_vals = df_attr.value_counts()

            for each_attr_val in attr_distinct_vals.keys():                    # gets each value of Sky eg.Sunny
                df_each_attr_val = df.loc[df[col] == each_attr_val]
                attr_rows_count,attr_cols_count = df_each_attr_val.shape
                df_label_per_val = df_each_attr_val[target]
                label_split_per_val = df_label_per_val.value_counts()

                entropy = 0.0
                for each_label in label_split_per_val:          # checks split for Sunny eg. 5+ 3-
                    entropy += (each_label / attr_rows_count) * math.log((each_label / attr_rows_count), log_base)

                if(entropy != abs(0.0)):
                    entropy = -entropy

                if (entropy <= entropy_result):
                    entropy_result = entropy
                    attr_result = col
                    attr_val_result = each_attr_val
                    label_result = label_split_per_val.keys()
                    label_result = str(label_result)[8:]
                    label_result = label_result.split("'")
                    label_result = label_result[0]

            print('<node entropy=' + str(entropy_result) + ' '
                'value =' + str(attr_val_result) + ' '
                'feature= att' + str(attr_result) + '>' + str(label_result)
                + '</node>')

        next_node_attr_vals = df[attr_result].value_counts()
        next_node_attr_vals = next_node_attr_vals.keys()

        list_vals = []
        for key in next_node_attr_vals:
            if(key != attr_val_result):
                list_vals.append(key)

        for each_node_value in list_vals:
            df_new = df.loc[df[attr_result] == each_node_value]
            del df_new[attr_result]
            row_temp, col_temp = df_new.shape
            find_next_node(df_new,col_temp,log_base=p_i,last_col=target)

def main():
    df = pd.read_csv('car.csv',delimiter=',',header=None)
    rows_in_df, cols_in_df = df.shape
    last_col = cols_in_df - 1
    labels = df[last_col]
    unique_labels = labels.value_counts()
    log_base = len(unique_labels)

    find_next_node(df,cols_in_df,log_base,last_col)

if __name__ == '__main__':
    main()