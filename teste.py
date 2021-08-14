import numpy as np

len_difference_array = np.array([1, 10, 1])
list_points = [['caso1', 'caso3', 'caso4'],['caso1'],['caso1', 'caso3', 'caso4']]
point_to_choose = np.where(len_difference_array == len_difference_array.min())
point_to_choose_list = list(point_to_choose[0])
print(list(point_to_choose[0]))
if len(point_to_choose_list) > 1:
        idx_max_cases = [len(list_points[item]) for item in point_to_choose_list]
        optimal_point = point_to_choose_list[np.argmax(np.array(idx_max_cases))]
        
print(idx_max_cases, optimal_point)