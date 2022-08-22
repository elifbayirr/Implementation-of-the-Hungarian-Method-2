import numpy as np
import time  #for start = time.time etc.
import tracemalloc  # tracemalloc is a library module that traces every memory block in python


# we need to find the row with the fewest zero elements. So, we can convert the previous matrix to the boolean matrix(0 → True, Others → False)
def min_zero_row(zero_mat, mark_zero):
	
	#find the row
	min_row = [999999999, -1]

	for row_num in range(zero_mat.shape[0]): 
		if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
			min_row = [np.sum(zero_mat[row_num] == True), row_num]

	# marked the specific row and column as False
	zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
	mark_zero.append((min_row[1], zero_index))
	zero_mat[min_row[1], :] = False
	zero_mat[:, zero_index] = False

def mark_matrix(mat):

	# transform the matrix to boolean matrix
	# 0 is true
	cur_mat = mat
	zero_bool_mat = (cur_mat == 0)
	zero_bool_mat_copy = zero_bool_mat.copy()

	# recording possible answer positions by marked_zero
	marked_zero = []
	while (True in zero_bool_mat_copy):
		min_zero_row(zero_bool_mat_copy, marked_zero)
	
	# recording the row and column positions seperately.
	marked_zero_row = []
	marked_zero_col = []
	for i in range(len(marked_zero)):
		marked_zero_row.append(marked_zero[i][0])
		marked_zero_col.append(marked_zero[i][1])

	non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))
	# mark rows that do not contain marked 0 elements and store row indexes in the non_marked_row
	
	marked_cols = []
	check_switch = True
	while check_switch:
		check_switch = False
		for i in range(len(non_marked_row)):
			row_array = zero_bool_mat[non_marked_row[i], :]
			for j in range(row_array.shape[0]):
				# search non_marked_row element, and find out if there are any unmarked 0 elements in the corresponding column
				if row_array[j] == True and j not in marked_cols:
					# store the column indexes in the marked_cols
					marked_cols.append(j)
					check_switch = True

		for row_num, col_num in marked_zero:
			# compare the column indexes stored in marked_zero and marked_cols
			if row_num not in non_marked_row and col_num in marked_cols:
				# if a matching column index exists, the corresponding row_index is saved to non_marked_rows
				non_marked_row.append(row_num)
				check_switch = True
	# the row indexes that are not in non_marked_row are stored in marked_rows
	marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))

	return(marked_zero, marked_rows, marked_cols)
	# mark_matrx function is finished and then returns marked_zero, marked_rows, marked_cols

def adjust_matrix(mat, cover_rows, cover_cols):
	cur_mat = mat
	non_zero_element = []

	# find the minimum value for an element that is not in marked_rows and not in marked_cols
	for row in range(len(cur_mat)):
		if row not in cover_rows:
			for i in range(len(cur_mat[row])):
				if i not in cover_cols:
					non_zero_element.append(cur_mat[row][i])
	min_num = min(non_zero_element)

	# subtract the elements which not in marked_rows nor marked_cols from the minimum values obtained in the previous step
	for row in range(len(cur_mat)):
		if row not in cover_rows:
			for i in range(len(cur_mat[row])):
				if i not in cover_cols:
					cur_mat[row, i] = cur_mat[row, i] - min_num
	# add the element in marked_rows, which is also in marked_cols, to the minimum value obtained by first loop.
	for row in range(len(cover_rows)):  
		for col in range(len(cover_cols)):
			cur_mat[cover_rows[row], cover_cols[col]] = cur_mat[cover_rows[row], cover_cols[col]] + min_num
	return cur_mat

def hungarian_algorithm(mat): 
	dim = mat.shape[0]
	cur_mat = mat

	# this step makes every column and every row subtract its internal minimum
	for row_num in range(mat.shape[0]): 
		cur_mat[row_num] = cur_mat[row_num] - np.min(cur_mat[row_num])
	
	for col_num in range(mat.shape[1]): 
		cur_mat[:,col_num] = cur_mat[:,col_num] - np.min(cur_mat[:,col_num])
	zero_count = 0
	while zero_count < dim:
		ans_pos, marked_rows, marked_cols = mark_matrix(cur_mat)
		zero_count = len(marked_rows) + len(marked_cols)

		if zero_count < dim:
			cur_mat = adjust_matrix(cur_mat, marked_rows, marked_cols)

	return ans_pos

def ans_calculation(mat, pos):
    # element composition stored in marked_zero, the minimum and maximum values of the linear assignment problem calculated
	total = 0
	ans_mat = np.zeros((mat.shape[0], mat.shape[1]))
	for i in range(len(pos)):
		total += mat[pos[i][0], pos[i][1]]
		ans_mat[pos[i][0], pos[i][1]] = mat[pos[i][0], pos[i][1]]
	return total, ans_mat

	
def main():
    
    # lets me get comma separated matrix or matrix from file
	cost_matrix = np.loadtxt("5x5mat.txt", delimiter=',')  
	#which matrix file you want to calculate you have to name it. Like 5x5mat,10x10mat,100x100mat...
	
	tracemalloc.start()
	
	# I put start at the beginning of the function to learn 'time'
	start = time.time()  # as we learned in class
	
	# to get the location of the element
	ans_pos = hungarian_algorithm(cost_matrix.copy()) 
	# to get the minimum/maximum value and the corresponding matrix.
	ans, ans_mat = ans_calculation(cost_matrix, ans_pos)  
	
	end=time.time() # end time

	print(f"Assignment problem result: {ans:.0f}\n")
	
	# assign our result to a value that will keep in 'rp' for print new text file
	rp = f"Assignment problem result: {ans:.0f}\n"
	
	
	print("Time {} seconds".format(end-start))  # use it to print our time
	
	# assign our time to a value that will keep in 'tp' for print new text file
	tp = "Time {} seconds\n".format(end-start)  
	
	
	print('current memory , peak memory :' , tracemalloc.get_traced_memory())  # thanks to tracemalloc library
	
	# current memory is the memory the code is currently using and peak memory is the maximum space the program used while executing.
	memory = 'current memory , peak memory :' , tracemalloc.get_traced_memory()
	
	tracemalloc.stop()  ## stopping the library
	

	with open('outputforpy.txt', 'w') as f:    # ı write outputforpy.txt file thanks to 'w' format
	
	    f.write(rp)  # save the result to file
	    f.write(tp)  # save the time to file
	    mp = str(memory)  # it has to be in the form of 'str' to print my memory
	    f.write(mp)  #  save the memory to file
	    

if __name__ == '__main__':
	main()