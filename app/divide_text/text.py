
# this works for give a limit of words per line
# if you want to give a limit of characters per line
# you can use divide_text_width

def divide_text_width(text: str, width: int, text_size: int) -> list:
    output = []
    
   
      
    words =  text.replace("\n"," ") .split(" ")

    text_line = ""
    if  len(text)*text_size<=width:
        return words
    for i,word in  enumerate(words):
        if len(text_line)*text_size > width-len(word)*text_size:
            output.append(text_line)
            text_line = ""
        
        text_line += word+" "
        if word.find(".")!=-1:
            text_line +="\n"
            output.append(text_line)
            text_line = ""

        if i==len(words)-1:
            output.append(text_line)
    return output

# limit of lines per page

def divide_text_height(text: str, height: int, text_size: int) -> list:
    output = []
    lines = text.split("\n")
    parraf_limit=int((height-text_size)/text_size)
   
    if  len(lines)<=parraf_limit:
        return [text]
 
    while len(lines)>0:
        output.append("\n".join(lines[:parraf_limit]))
        lines=lines[parraf_limit:]
  
            


      

    return output



# this return you a list with the pages
# so you can make an animation or something with it
def divide_text(text: str, width: int, height: int, text_size:int) -> list:
    
    lin = "\n".join(divide_text_width(text, width, text_size/2))

    pages = divide_text_height(lin, height, text_size*1.5)
 
    return pages

