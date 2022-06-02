from flask import flash
import re 
  
def main(password): 

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
      
    
    pat = re.compile(reg) 
      
    
    mat = re.search(pat, password) 
      
    
    if mat: 
        return mat
    else: 
        print("Password invalid !!") 
