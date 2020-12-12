import matplotlib.pyplot as plt
import numpy as np

# Transforms object detection table from wide format to long format
def object_detections_wide_to_long(conn, input_table, output_table, replace=True, num_objects=5):
    conn.loadactionset('fedSql')
    if replace == True:
        replace_option = "{options replace=true}"
    else:
        replace_option = "{options replace=false}"
    # column definitions
    copy_columns = ['_filename_0::varchar', 
                    '_id_::bigint']
    object_columns = ['_label_::varchar',
                      'OBJECT_NUMBER::bigint', 
                      'OBJECT_NAME::varchar',
                      'OBJECT_PROBABILITY::double',
                      'X::double',
                      'Y::double',
                      'WIDTH::double',
                      'HEIGHT::double']
    query = 'create table {} {} as select '.format(output_table, replace_option)
    for col in copy_columns+object_columns:
        query+='objdet.{},'.format(col)
    query = query[:-1]
    query+=' from ('
    #subqueries (for each object we need a subquery)
    for i in range(num_objects):
        query+='select _id_::char || \'_\' || \'{}\' as _label_,'.format(i)
        for col in copy_columns:
            query+='{},'.format(col)
        # Column transformations
        query+='\'{}\' as OBJECT_NUMBER,'.format(i)
        query+='_Object{}_ as OBJECT_NAME,'.format(i)
        query+='_P_Object{}_ as OBJECT_PROBABILITY,'.format(i)
        query+='_Object{}_x as X,'.format(i)
        query+='_Object{}_y as Y,'.format(i)
        query+='_Object{}_width as WIDTH,'.format(i)
        query+='_Object{}_height as HEIGHT'.format(i)
        query+=' from {} where _P_Object{}_ is not missing'.format(input_table, i)
        if i < num_objects-1:
            query+=' union '
    query+=' ) as objdet'
    conn.fedSql.execDirect(query=query)
    return conn.CASTable(output_table)

def display_detections_long_table(detection_table_long, columns=['OBJECT_NAME'], label_column='OBJECT_NAME', nimages=5, ncol=8, figsize=None, where=None):
    # check if columns is a list object
    if type(columns) == str:
        columns = [columns]
    if label_column not in columns:
        columns.append(label_column)
    detection_table_long.params['where'] = where
    # restrict the number of observations to be shown
    try:
        # we use numrows to check if where clause is valid
        max_obs = detection_table_long.numrows().numrows
        nimages = min(max_obs, nimages)
    except AttributeError:
        detection_table_long.params['where'] = None
        warn("Where clause doesn't take effect, because we encountered an error while processing the where clause."
             "Please check your where clause.")
    temp_tbl = detection_table_long.fetchimages(to=nimages, fetchimagesvars=columns)
    if nimages > ncol:
        nrow = nimages // ncol + 1
    else:
        nrow = 1
        ncol = nimages
    if figsize is None:
        figsize = (16, 16 // ncol * nrow)
    fig = plt.figure(figsize=figsize)
    for i in range(nimages):
        image = temp_tbl['Images']['Image'][i]
        if label_column in temp_tbl['Images'].columns:
            label = temp_tbl['Images'][label_column][i]
        else:
            label = 'N/A'
        ax = fig.add_subplot(nrow, ncol, i + 1)
        ax.set_title('{}'.format(label))
        if len(image.size) == 2:
            plt.imshow(np.array(image), cmap='Greys_r')
        else:
            plt.imshow(image)
        plt.xticks([]), plt.yticks([])
    plt.show()