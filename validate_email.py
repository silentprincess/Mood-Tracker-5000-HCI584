def is_valid_email_address(emailAddress):
    #check for single '@' symbol
    symbol_count = emailAddress.count("@")
    if (symbol_count > 1):
        return 1, "Too many @ symbols, invalid address."
    if (symbol_count < 1): 
        return 2, "No @ symbol, invalid address."
    
    #check for single '.'
    symbol_count = emailAddress.count(".")
    if (symbol_count > 1):
        return 3, "Too many . symbols, invalid address."
    if (symbol_count < 1):
        return 4, "No . symbol, invalid address."
        
    #split email address into parts A, B, and C
    
    #portion A
    emailAddress = emailAddress.split("@")
    emailAddress_a = emailAddress [0]
    
    #portions B & C
    emailAddress = emailAddress[1].split(".")
    
    emailAddress_b = emailAddress [0]
    emailAddress_c = emailAddress [1]
  
    #check the length of portion A
    a_length = len(emailAddress_a)
    if (a_length < 3 or a_length > 16):
        return 5, "Email before @ must be between 3 and 16 characters, try again."
    
    #check if A is alphanumeric
    a_num = emailAddress_a.isalnum()
    if(a_num == 0):
        return 6, "Email before @ is not alphanumeric, try again."
    
    #check the legnth of portion B
    b_length = len(emailAddress_b)
    if (b_length < 2 or b_length > 8):
        return 7, "Email after @ must be between 2 and 8 characters, try again."
    
    #check if B is alphanumeric
    b_num = emailAddress_b.isalnum()
    if (b_num == 0):
        return 8, "Email after @ is not alphanumeric, try again."
    
    #check if C is com, edu, org, gov
    if emailAddress_c not in ["com", "edu", "org", "gov"]:
        return 9, "Email does not have valid domain. Try again."
    
    return None, "Seems Legit."