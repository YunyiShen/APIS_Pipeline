import os
import shutil

def multiple_split(path,tol=500,by=50): 

# put files into tree-like sub folder system, in order to overcome google drive timeout problem
  if by>tol: # should not have more sub folders than tolerate
    by=tol
  all_files = os.listdir(path) # find all files
  n_files = len(all_files)

  if n_files>tol:
    
    spliter = int(n_files/(by-1))
    split_remain = int(n_files-spliter*(by-1))
	
    for i in range(by-1):
      os.makedirs(path+"/"+str(i)) # mk this sub directory, 
      for j in range(spliter):
        os.rename(path+"/"+all_files[i*spliter+j],
                  path+"/"+str(i)+"/"+all_files[i*spliter+j]) # move ith part
      multiple_split(path+"/"+str(i),tol=tol,by=by) # recursive call
    
    i=(by-1)
    os.makedirs(path+"/"+str(i))
    for j in range(split_remain):
      os.rename(path+"/"+all_files[i*spliter+j],
                path+"/"+str(i)+"/"+all_files[i*spliter+j])
    multiple_split(path+"/"+str(i),tol=tol,by=by) # recursive call

    return(0)
  else :
    return(0)

