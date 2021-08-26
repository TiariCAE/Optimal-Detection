
import pandas as pd
import numpy as np

input_number_cases = int(input("Type the number of cases analyzed: "))

# make a list of 1 until n+1 where n is the number of cases 
cases = list(range(1, input_number_cases + 1))
# quantity of points in CFD domain
points_lengh = int(input("Type the number of points: "))            


# import the csv archive generated from CFD-Post and modificated to have the right format
df = pd.read_csv("data\export.csv")  

# make a empty list to recive all cases numbered
case_number = []   
# make a empty list to recive all points numbered          
point_number = []    

# make case_number and point_number lists 
for case in cases:           
    i=0 
    while i < points_lengh:        
        case_number.append('Case_{}'.format(case))    
        point_number.append('{}'.format(i+1))   
        i += 1

# make a list with all points without repetition and ordered
points = list(set(point_number))
points = [int(point) for point in points]
points.sort()
points = [str(point) for point in points]

# add the case number and point number column
df['Case_Number'] = case_number
df['Point_Number'] = point_number  
# add an empty column
df['Detected'] = 0 


detection_limit = float(input("Type the mass fraction value that is detectable( > or = this value is detected) (Decimal separator is dot): "))
# make a new data frame equal to 'df'
df1 = df.copy() 
# in Detected column write 0 for nondetected mass fraction and 1 for detected.                                 
df1.loc[df1.iloc[:, 3] < detection_limit , 'Detected'] = 0    
df1.loc[df1.iloc[:, 3] >= detection_limit, 'Detected'] = 1     

# to data frame generation from the dictionary
df2 = pd.DataFrame()   
list_points = []
point_name = []
# loop in the Points List                             
for i in points:    
    # filter the df1, where Point_Number is a "Point_i"                                     
    dfa = df1[df1["Point_Number"] == i] 
    # filter the dfa where only the detected cases are writed                   
    dfb = dfa[dfa["Detected"] == 1]  
    # make a list with Case_Number (only detected)                       
    list_cases = list(dfb["Case_Number"])     
    # make the dictionary item_pcd that content, to each point (that detects at least one case),
    # the quantity and identification of the detected cases
    item_pcd = {                            
            "Detected Cases": list_cases,           
            "Quantity": len(list_cases),          
            "Point": i                                      
        }
    list_points.append(list_cases)
    point_name.append(i)
    df2 = df2.append(item_pcd, ignore_index=True)
df2.to_excel('All_Cases.xlsx', index = False)

# make a list with the name of all cases
case_names = []
for i in cases:
    case_names.append('Case_{}'.format(i))
print('\n All analyzed cases: \n', case_names)
total_cases = case_names 
 
# make an empty list to append the optimal points
detection_point = [] 
count = 0
# loop while there is some undetected case
while (count <= 1000) and (len(case_names) > 0):
    difference = [list(set(case_names) - set(point)) for point in list_points]
    len_difference = [len(item) for item in difference]
    # we may have more than one difference with the same length
    len_difference_array = np.array(len_difference)
    point_to_choose = np.where(len_difference_array == len_difference_array.min())
    point_to_choose_list = list(point_to_choose[0])
    # loop if there are points that detected the same quantity of cases
    if len(point_to_choose_list) > 1:
        idx_max_cases = [len(list_points[item]) for item in point_to_choose_list]
        # verifying the length of idx_max_cases vectors
        idx = np.argmax(np.array(idx_max_cases))
        optimal_point = point_name[point_to_choose_list[idx]] 
        # idx of the difference list 
        case_names = difference[point_to_choose_list[idx]]
        detection_point.append(optimal_point)
        list_point_idx = int(optimal_point) - 1
        list_points[list_point_idx] = []
    else:
        case_names = difference[np.argmin(len_difference)]
        point = point_name[point_to_choose_list[0]]
        detection_point.append(point)
        list_point_idx = int(point) - 1
        list_points[list_point_idx] = list()
    
    list_point_len_items = [len(item) for item in list_points]
    
    # check if all vectors are empty
    if sum(list_point_len_items) == 0:
        break 
    count += 1
 
if len(case_names) == len(total_cases):
    print("\n ATTENTION: No cases were detected by any point.")
else:

    print("\n List of cases not detected by any point: ", case_names)
    print('\n The optimal detection points are: ', detection_point)

    # make a data frame with the point's coordinates
    df_all_coord = pd.DataFrame() 
    for i in detection_point:    
        # filter the df1 where Point_Number is an optimal point (i)                                         
        df_coord = df1[df1["Point_Number"] == i].reset_index()
        # add a line in df with the coordinates of point i
        df_all_coord = df_all_coord.append(df_coord.iloc[0]) 

    # print only the relevant columns of the df with coordinates                        
    print('\n The coordinates of the optimal points are below. \n', df_all_coord[['Point_Number', 'X', ' Y ', ' Z ']])

print("\n To find the cases detected by each point, oppen the archive All_Cases.xlsx .")







