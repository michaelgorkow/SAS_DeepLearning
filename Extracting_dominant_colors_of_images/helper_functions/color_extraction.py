from dlpy.images import ImageTable
import pandas as pd
from scipy.spatial import distance_matrix

# Read Color Data
color_data = pd.read_csv('helper_functions/color_data.csv')
color_data_numpy = color_data[['r','g','b']].to_numpy()

# Helper Function to find closest color
def get_color_data(row):
    r = row.R
    g = row.G
    b = row.B
    ix = distance_matrix(color_data[['r','g','b']].to_numpy(), [[r,g,b]]).argmin(axis=0)[0]
    color_group = color_data.GROUP.iloc[ix]
    color_name = color_data.NAME.iloc[ix]
    color_r = color_data.r.iloc[ix]
    color_g = color_data.g.iloc[ix]
    color_b = color_data.b.iloc[ix]
    return color_group, color_name, color_r, color_g, color_b

# Extract dominant colors by clustering pixel values
def extract_dominant_colors(conn, image_table, image_column='_image_', output_table='color_extraction', image_width=50, image_height=50):
    s = conn
    num_pixels = image_width*image_height
    # Load functions
    conn.loadactionset('transpose')
    conn.loadactionset(actionset="clustering")

    # Create a flat table where each columns represents a R, G or B value for each pixel
    # Output table width is: 1 + pixel-width*pixel-height*number-channels
    # Example: 224*224 RGB image results in a table of width 1+224*224*3=150529
    # NOTE: groupchannels has the order B-G-R
    flat_image_table = conn.image.flattenImageTable(casout={'name':'flattenedImagesTable', 'replace':True},
                                                    table=image_table,
                                                    image=image_column,
                                                    w = image_width,
                                                    h = image_height, 
                                                    transpose=False, 
                                                    groupchannels=True)['OutputCasTables']['casTable'][0]
    # B - Table
    b_cols = set(['c{}'.format(i) for i in range(1,1+num_pixels)])
    conn.transpose.transpose(table=flat_image_table,
                             transpose=b_cols, 
                             name='pixel',
                             id={"_label_"},
                             prefix='B_',
                             casOut={"name":"tout_b", "replace":True})
    conn.datastep.runcode(code='''data casuser.tout_b (drop=pixel);
                                    set casuser.tout_b;
                                    pixel2 = input(SUBSTR(pixel,2), 10.);
                                    rename pixel2=pixel;
                                    run;''')
    b_table = conn.CASTable('tout_b')
    # G - Table
    g_cols = set(['c{}'.format(i) for i in range(1+num_pixels,1+num_pixels*2)])
    conn.transpose.transpose(table=flat_image_table,
                             transpose=g_cols,
                             name='pixel',
                             id={"_label_"},
                             prefix='G_',
                             casOut={"name":"tout_g", "replace":True})
    conn.datastep.runcode(code='''data casuser.tout_g (drop=pixel);
                                    set casuser.tout_g;
                                    pixel2 = input(SUBSTR(pixel,2), 10.);
                                    pixel2 = pixel2 - {};
                                    rename pixel2=pixel;
                                    run;'''.format(num_pixels))
    g_table = conn.CASTable('tout_g')
    # R - Table
    r_cols = set(['c{}'.format(i) for i in range(1+num_pixels*2,1+num_pixels*3)])
    conn.transpose.transpose(table=flat_image_table,
                             transpose=r_cols,
                             name='pixel',
                             id={"_label_"},
                             prefix='R_',
                             casOut={"name":"tout_r", "replace":True})
    conn.datastep.runcode(code='''data casuser.tout_r (drop=pixel);
                                    set casuser.tout_r;
                                    pixel2 = input(SUBSTR(pixel,2), 10.);
                                    pixel2 = pixel2 - {};
                                    rename pixel2=pixel;
                                    run;'''.format(num_pixels*2))
    r_table = conn.CASTable('tout_r')
    # Merge tables
    bg_table = b_table.merge(g_table, on='pixel')
    bgr_table = bg_table.merge(r_table, on='pixel')
    # # Create color clusters for each image
    first_table = True
    for l in image_table['_LABEL_']:
        b = 'B_{}'.format(l)
        g = 'G_{}'.format(l)
        r = 'R_{}'.format(l)
        clusters = conn.kclus(table=bgr_table,
                              inputs={b, g, r},
                              standardize='RANGE',
                              #nClusters=3,
                              estimateNClusters=dict(method='ABC', minClusters=2),
                              seed=534,
                              maxIters=40,
                              init="RAND")
        cluster_centers = clusters['ClusterCenters'].drop('_ITERATION_', axis=1)
        cluster_summary = clusters['ClusterSum'][['Cluster','Frequency']]
        cluster_summary['COLOR_CLUSTER_PERCENT'] = cluster_summary['Frequency'] / num_pixels * 100
        cluster_summary = cluster_summary.merge(cluster_centers, how='inner', left_on='Cluster', right_on='_CLUSTER_ID_')
        cluster_summary = cluster_summary.drop('_CLUSTER_ID_', axis=1)
        cluster_summary.rename(inplace=True,
                               columns={cluster_summary.columns[3]:cluster_summary.columns[3][:1],
                                        cluster_summary.columns[4]:cluster_summary.columns[4][:1],
                                        cluster_summary.columns[5]:cluster_summary.columns[5][:1],
                                        'Frequency':'COLOR_CLUSTER_SIZE', 
                                        'Cluster':'COLOR_CLUSTER_ID'})
        cluster_summary['_LABEL_'] = l
        # Map colors to web safe colors
        cluster_summary[['COLOR_GROUP','COLOR_NAME','COLOR_R','COLOR_G','COLOR_B']] = cluster_summary.apply(lambda row: get_color_data(row), axis='columns', result_type='expand')
        # groupby color_name to avoid duplicates
        cluster_summary = cluster_summary.groupby('COLOR_NAME').agg(dict(COLOR_CLUSTER_SIZE='sum', 
                                                                         COLOR_CLUSTER_ID='sum', 
                                                                         COLOR_CLUSTER_PERCENT='mean',
                                                                         R='mean', 
                                                                         G='mean', 
                                                                         B='mean', 
                                                                         _LABEL_='first', 
                                                                         COLOR_GROUP='first', 
                                                                         COLOR_R='first', 
                                                                         COLOR_G='first', 
                                                                         COLOR_B='first')).reset_index()
        cluster_summary.sort_values('COLOR_CLUSTER_SIZE', inplace=True)
        cluster_summary['COLOR_CLUSTER_ID'] = range(0, len(cluster_summary))
        # Upload and concatenate results in CAS
        if first_table == True:
            conn.upload_frame(cluster_summary, casout=dict(name=output_table, replace=True))
            first_table = False
        else:
            conn.upload_frame(cluster_summary, casout=dict(name='tmp', replace=True))
            conn.datastep.runcode(code='''data casuser.{} (append=yes);
                                            set tmp;
                                            run;'''.format(output_table))
    return conn.CASTable(output_table)

# Create Image table from query
def find_object_by_color(conn, detection_table_long, object_color_table, output_table, object_name, object_color, color_cluster_min_size=0, object_column='OBJECT_NAME', color_column='COLOR_NAME', color_cluster_size_column='COLOR_CLUSTER_PERCENT', id_column='_LABEL_', replace=True):
    conn.loadactionset('fedSql')
    #object_ids = object_color_table[object_color_table[color_column] == object_color][id_column].values
    object_ids = object_color_table[(object_color_table[color_column] == object_color) & (object_color_table[color_cluster_size_column] > color_cluster_min_size)][id_column].values
    object_ids = "', '".join(object_ids)
    object_ids = "('{}')".format(object_ids)
    
    conn.loadactionset('fedSql')
    if replace == True:
        replace_option = "{options replace=true}"
    else:
        replace_option = "{options replace=false}"
    query  = ' create table {} {} as '.format(output_table, replace_option)
    
    query += " select * from {} ".format(detection_table_long.name)
    query += " where {} = \'{}\' and {} in {} ".format(object_column, object_name, id_column, object_ids)
    res = conn.fedSql.execDirect(query=query)
    img_tbl = ImageTable.from_table(conn.CASTable(output_table))
    return img_tbl