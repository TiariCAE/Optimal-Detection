
import pandas as pd
import numpy as np

# make a list of 1 until n+1 where n is the number of cases, so you must see range(1,17) if you have 16 cases (you must to edit here)
cases = list(range(1,17))    
# quantity of points in CFD domain (you must to edit here) 
points_lengh = 30            

# import the csv archive generated from CFD-Post and modificated to have the right format
df = pd.read_csv("data\export-transient copy.csv")  

# make a empty list to recive all cases numbered
case_number = []   
# make a empty list to recive all points numbered          
point_number = []    

# make case_number and point_number lists 
for case in cases:           
    i=0 
    while i < points_lengh:        
        case_number.append('Case_{}'.format(case))    
        point_number.append('Point_{}'.format(i+1))   
        i += 1

# make a list with all points without repetition
points = list(set(point_number))    

# add the case number and point number column
df['Case_Number'] = case_number    
df['Point_Number'] = point_number  
# add an empty column
df['Detected'] = 0 

# make a new data frame equal to 'df'
df1 = df.copy() 
# in Detected column write 0 for nondetected mass fraction and 1 for detected.                                 
df1.loc[df1.iloc[:, 3] <= 0.002, 'Detected'] = 0    
df1.loc[df1.iloc[:, 3] > 0.002, 'Detected'] = 1     

# make a dictionary
pcd = []   
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
  
# make a list with the name of all cases
case_names = []
for i in cases:
    case_names.append('Case_{}'.format(i))
print('\n All cases: \n', case_names)
 
# make an empty list to append the optimal points
detection_point = [] 
# loop while there is some undetected case
while len(case_names) > 0:
    difference = [list(set(case_names) - set(point)) for point in list_points]
    len_difference = [len(item) for item in difference]
    len_difference_array = np.array(len_difference)
    point_to_choose = np.where(len_difference_array == len_difference_array.min())
    point_to_choose_list = list(point_to_choose[0])
    # loop if there are points that detected the same quantity of cases
    if len(point_to_choose_list) > 1:
        print('aqui,',point_to_choose_list)
        idx_max_cases = [len(list_points[item]) for item in point_to_choose_list]
        optimal_point = point_name[point_to_choose_list[np.argmax(np.array(idx_max_cases))]] 
        case_names = difference[np.argmax(np.array(idx_max_cases))]
        detection_point.append(optimal_point)
    else:
        case_names = difference[np.argmin(len_difference)]
        detection_point.append(point_name[point_to_choose_list[0]])
    print(case_names)
print('\n The optimal detection points are:', detection_point)

""" # cria um df para conter as coordenadas x, y e z dos pontos ótimos
df_all_coord = pd.DataFrame() 
for i in detection_point:    
    # filtra o df1 onde Point_Number é um dos pontos ótimos (i)                                         
    df_coord = df1[df1["Point_Number"] == i].reset_index()
    # acrescenta uma linha no df de coordenadas referente ao ponto i
    df_all_coord = df_all_coord.append(df_coord.iloc[0]) 

# imprime apenas as colunas relevantes do df das coordenadas                        
print('\n As coordenadas dos pontos ótimos estão na tabela a seguir. \n', df_all_coord[['Point_Number', 'X', ' Y ', ' Z ']]) """



#encontrar o vetor q detecta maior quantidade de pontos dentro dos mais otimizados









