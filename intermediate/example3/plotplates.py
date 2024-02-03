import os
import requests
import pyvo as vo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def list_els(dxx,itr):
    ''' Check elements of dxx '''
    i=0
    for row in dxx.itertuples():
        st = '%d %d %f %f %f %f' % (row[0] , row[2],row[3],row[4],row[5],row[6])
        print(st)
        i += 1
        if(i > itr) : break
            
            
def map_coord(ar):
    ''' Convert ra/dec (deg) => ra/dec (rad) '''
    ard = ar
    ra = np.radians(ar.ra)
    ra[ra > np.pi] = ra - 2 * np.pi
    ard.ra=ra
    ard.de = np.radians(ar.de)
    ard.fov1= np.radians(ar.fov1)
    ard.fov2= np.radians(ar.fov2)
    return ard


def plot_mwrfov(dr,loc,nx,dfxp,imgname,colx,xtlab,s):
    ''' 
        create the Mollweide plot with the values from the table 
    '''
    fig = plt.figure(figsize=(16, 8))
    
    if(len(colx) <1 ):
        colx = '#FF0011'
    ax = fig.add_subplot(111, projection="mollweide")
    title=('APPLAUSE %s\nArchive %s\n Number of plates: %d' % (dr,loc,nx))
    
    ax.grid()
    ax.set_xticklabels(xtlab)
    ax.set_title(title);

    archiv_data = dfxp
    
    archiv_data.rename(columns={'ra_icrs':'ra','dec_icrs':'de'}, inplace=True)
    ax.set_linewidth=0.2
    ard = map_coord(archiv_data)  

    # contains the boundaries for FOV of each plate
    lines = []

    for i in range(len(ard)):
        if(ard.fov1[i] > ard.fov2[i]):
            blx= ard.fov1[i]/2
            bly= ard.fov2[i]/2
        else:
            bly= ard.fov1[i]/2
            blx= ard.fov2[i]/2

        # calculates location on the sky 
        rec = np.array([(ard.ra[i] - blx,ard.de[i]-bly),
                   (ard.ra[i] + blx,ard.de[i]-bly),
                   (ard.ra[i] + blx,ard.de[i]+bly),
                   (ard.ra[i] - blx,ard.de[i]+bly)
                   ])

        lines.extend(list(np.roll(np.tile(rec, 2).flatten(), -2).reshape((4, 2, 2))))
        # lines exceeding -pi have to wrap around, they are plotted with +2 pi added
        if (ard.ra[i] - blx  < -np.pi):
            rax=ard.ra[i]+2*np.pi
            rec = np.array([(rax - blx,ard.de[i]-bly),
                   (rax + blx,ard.de[i]-bly),
                   (rax + blx,ard.de[i]+bly),
                   (rax - blx,ard.de[i]+bly)
                   ])
            lines.extend(list(np.roll(np.tile(rec, 2).flatten(), -2).reshape((4, 2, 2))))


    ax.scatter(ard.ra, ard.de, s=3, c='r', alpha=0.6)
    ax.add_collection(LineCollection(lines, linewidths=0.2))
    if s == 1:
        plt.savefig(imgname)
    plt.clf()
        
def create_plot(arch_id, arch_nam, num_plates):
   
    verb = 0
    # don't try solar data
    if (arch_id == 6): return

    # check if img dir availabale 
    imgpath = 'imgdr4'
    if(not os.path.exists(imgpath)):
        os.mkdir(imgpath)

    # static data for plotting
    xtlab=['14h', '16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h']
    DR='DR4'
    COLR = '#33F4F0'

    archive_num = '%03d' % arch_id 
    imgname = '%s/dr4_archive_%s.png' % (imgpath,archive_num)
    if(verb>0): print(imgname)

    if (arch_id == 2):

        # SQL query to database, table solution, because the field of view (= size of the area mapped on a plate) is required
        query1 = "SELECT plate_id,archive_id, ra_icrs, dec_icrs FROM applause_dr4.exposure WHERE archive_id = "
        query2 = "AND NOT(ra_icrs IS NULL OR dec_icrs IS NULL) ORDER BY plate_id"
        query = ("%s %s %s" % (query1,archive_num,query2))
        tap_result = tap_service.run_sync(query, language=lang)

        dfx = tap_result.to_table().to_pandas()
        ## extend the data (add fov1 = 2.1, fov2 =2.1  )
        dfx['fov1'] = 2.1 
        dfx['fov2'] = 2.1 

    else:    
    # SQL query to database, table solution, because the field of view (= size of the area mapped on a plate) is required
        query1 = "SELECT plate_id,archive_id, fov1, fov2, ra_icrs, dec_icrs FROM applause_dr4.solution WHERE archive_id = "
        query2 = "AND NOT(ra_icrs IS NULL OR dec_icrs IS NULL) ORDER BY plate_id"
        query = ("%s %s %s" % (query1,archive_num,query2))
    
        tap_result = tap_service.run_sync(query, language=lang)                
        
        if (arch_id == 401):
            # TLS special: take means for  ra / dec, and fov1=fov2 (quadratic shape of plate)  
            dfy = tap_result.to_table().to_pandas() 
            dfy['fov1'] = dfy['fov2']
            if(verb>0): list_els(dfy,4)
            # now calculate the means, some black magic of pandas
            dfx = dfy.groupby('plate_id',as_index=False, group_keys=False)[['plate_id','archive_id','fov1','fov2','ra_icrs','dec_icrs']].mean()
            if(verb>0): list_els(dfx,4)
        else:
            dfx = tap_result.to_table().to_pandas()
   
         
    if(verb>0): print(query) 

    # call plotting 
    plot_mwrfov(DR,arch_nam,num_plates,dfx,imgname,COLR,xtlab,1)
    
# Prepare archive access
x_url = 'https://www.plate-archive.org/tap'
tap_session = requests.Session()
tap_service = vo.dal.TAPService(x_url, session=tap_session)
lang='PostgreSQL'

# Query archive table for all available archives
qry = "Select archive_id, archive_name, num_plates from applause_dr4.archive order by archive_id"
tap_result = tap_service.run_sync(qry, language=lang)
dfa = tap_result.to_table().to_pandas()
dfa.to_csv('archive_id.csv', index=False)

# Loop through the archives
for index, row in dfa.iterrows():
    if(row['archive_id']==401):
        create_plot(row['archive_id'], row['archive_name'], row['num_plates'])
      