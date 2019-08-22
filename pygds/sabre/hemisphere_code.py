


def get_hemisphere_code(region_name):
    
    hemisphere_code = "0"

    if region_name == "United States":
        hemisphere_code = "0"
    
    if region_name == "Central America":
        hemisphere_code = "1"
    
    if region_name == "Caribbean":
        hemisphere_code = "2"
    
    if region_name == "Latin America":
        hemisphere_code = "3"

    if region_name == "Europe":
        hemisphere_code = "4"
    
    if region_name == "Africa":
        hemisphere_code = "5"
    
    if region_name == "Middle East":
        hemisphere_code = "6"
    
    if region_name == "Asia":
        hemisphere_code = "7"
    
    if region_name == "Asia Pacific":
        hemisphere_code = "8"
    
    if region_name == "Canada":
        hemisphere_code = "9"
        
    return hemisphere_code