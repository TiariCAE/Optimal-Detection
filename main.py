
import pandas as pd

# cria uma lista de 1 até n+1 do número de casos exportados
cases = list(range(1,17))    
# quantidade de pontos que foram exportados em cada caso 
points_lengh = 30            

# importa o arquivo csv gerado no cfd-post
df = pd.read_csv("data\export-transient copy.csv")  

# cria lista vazia
case_number = []   
# cria lista vazia          
point_number = []    

# percorre a lista com número de casos definido
for case in cases:           
    i=0 
    # enquanto i é menor do que o número de possíveil pontos de detecção exportados
    while i < points_lengh:    
        # nomeia os Casos a cada n total de pontos       
        case_number.append('Case_{}'.format(case))    
        # nomeia os pontos de 1 a n para cada caso
        point_number.append('Point_{}'.format(i+1))   
        i += 1

# cria a lista de pontos sem repetição para usar adiante
points = list(set(point_number))    

# acrescenta a coluna com o número de cada caso
df['Case_Number'] = case_number    
# acrescenta a coluna com o número de cada ponto
df['Point_Number'] = point_number  
# acrescenta uma coluna vazia
df['Detected'] = 0 

# cria um novo df igual ao anterior
df1 = df.copy() 
# na coluna Detected escreverá 0 para fração mássica não detectável e 1 para fração mássica detectável                                    
df1.loc[df1.iloc[:, 3] <= 0.002, 'Detected'] = 0    
df1.loc[df1.iloc[:, 3] > 0.002, 'Detected'] = 1   

# mostrar a quantidade de pontos que não detectaram nenhum caso, ou seja, tem o index [0]
#df1[['Point_Number', 'Detected']].groupby('Point_Number').agg(lambda x: list(set(x))).Detected.value_counts().reset_index()  

# cria um dicionário com as informações de ponto, caso e detecção
pcd = []   
 # para a geração do df a partir do dicionário
df2 = pd.DataFrame()   

# caminha cada item da lista points (lista com o nome dos n pontos)                               
for i in points:    
    # filtra o df1, onde Point_Number é um "Point_i")                                        
    dfa = df1[df1["Point_Number"] == i] 
    # filtra o dfa onde só os casos detectados são escritos                    
    dfb = dfa[dfa["Detected"] == 1]  
    # cria uma lista com a informação dos Case_Number apenas que foram detectados.                       
    list_cases = list(dfb["Case_Number"])     
    # cria o dicionário item_pcd que contém, para cada ponto (que teve pelo menos detecção de um caso), a quantidade e identificação dos casos detectados
    item_pcd = {                            
            "Detected Cases": list_cases,           
            "Quantity": len(list_cases),          
            "Point": i                                      
        }
    # cria um df a partir do dicionário item_pcd
    df2 = df2.append(pd.DataFrame(item_pcd))      
# cria um df final ordenado pelos pontos que mais detectaram casos
df_final = df2.sort_values(["Quantity",'Point'], ascending=False)
#print(df_final.head(50))

# cria uma lista com o nome de todos os casos que estão sendo avaliados
case_names = []
for i in cases:
    case_names.append('Case_{}'.format(i))
print('\n Os casos foram verificados são: \n', case_names)

# cria uma lista com os pontos que detectaram casos e de forma ordenada
points_dff = list((df_final['Point']))
# elimina da lista os pontos repetidos
points_sem_rep = [item for i, item in enumerate(points_dff) if item != points_dff[i-1]]

# cria uma lista que será preenchida com os pontos ótimos de detecção
detection_point = [] 
# percorre a lista de pontos que são candidatos a pontos ótimos de forma ordenada
for i, item in enumerate(points_sem_rep):    
    # filtra o df_final pelos pontos que estão na lista de pontos candidatos                                        
    dfc = df_final[df_final["Point"] == item] 
    # cria uma lista com a informação dos Detected Cases do determinado ponto                      
    list_cases_dff = list(dfc["Detected Cases"]) 
    # avalia a diferença da lista com todos os casos e a lista dos casos detectados daquele ponto 
    difference = list(set(case_names) - set(list_cases_dff))
    # condicional que para o for se todos os casos já estiverem listados no primeiro ponto e escreve esse ponto na lista de pontos ótimos
    if len(difference) == 0 and i == 0:
        detection_point.append(item)
        break
    # se houver casos que ainda não estão na lista do ponto, escreve esse ponto na lista de ótimos e continua o for
    elif len(difference) < len(case_names):
        detection_point.append(item)
    # condicional que para o for quando não há mais pontos a serem avaliados já que todos os casos foram abrangidos
    if len(difference) < len(case_names) and len(difference) == 0:
        break
    # a nova lista usada para comparação será uma lista apenas com os casos faltantes e reinicia-se o for
    case_names = difference
print('\n Os pontos ótimos de detecção são:', detection_point)

df_final.to_csv('Df.csv', index= False)

# cria um df para conter as coordenadas x, y e z dos pontos ótimos
df_all_coord = pd.DataFrame() 
for i in detection_point:    
    # filtra o df1 onde Point_Number é um dos pontos ótimos (i)                                         
    df_coord = df1[df1["Point_Number"] == i].reset_index()
    # acrescenta uma linha no df de coordenadas referente ao ponto i
    df_all_coord = df_all_coord.append(df_coord.iloc[0]) 

# imprime apenas as colunas relevantes do df das coordenadas                        
print('\n As coordenadas dos pontos ótimos estão na tabela a seguir. \n', df_all_coord[['Point_Number', 'X', ' Y ', ' Z ']]) 













