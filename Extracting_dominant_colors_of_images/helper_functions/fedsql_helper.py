# Performs an inner-join
# FedSQL is used because it supports blob data
def fedsql_inner_join(conn, left_table, right_table, output_table, left_columns=['*'],right_columns=['_image_'], left_on=[], right_on=[], replace=True):
    conn.loadactionset('fedSql')
    if replace == True:
        replace_option = "{options replace=true}"
    else:
        replace_option = "{options replace=false}"
    #query = "create table {} {} as select left_table.*, right_table.* ".format(output_table, replace_option)
    query  = ' create table {} {} as select '.format(output_table, replace_option)
    for col in left_columns:
        query += ' left_table.{}, '.format(col)
    for col in right_columns:
        query += ' right_table.{},'.format(col)
    query = query[:-1]
    query += " from {} as left_table, {} as right_table ".format(left_table, right_table)
    query += " where "
    for i, joincols in enumerate(zip(left_on, right_on)):
        query += "left_table.{} = right_table.{}".format(joincols[0], joincols[1])
        if i < len(left_on)-1:
            query += ' and '
    conn.fedSql.execDirect(query=query)
    return conn.CASTable(output_table)