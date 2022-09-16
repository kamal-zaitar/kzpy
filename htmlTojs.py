
# no data like this <!--<div> </div>-->  is acceptable
# f1 -> join lines


print('Report bugs:')

print('Facebook: https://www.facebook.com/kzkamalzaitar/ (More active here)')
print()
print('no data like this <!--<div> </div>-->  is acceptable')
print()


def html_to_js(html_script, js_variable_name, **kwargs):
    
    # add in this list any html element  that has no </element>
    # example: <div></div> has it 
    # <img> doesn't has </img>
    
    list_exceptions_element = ['<img', '<meta', '<!--','<input', '<path']

    mode = kwargs.get('mode','')

    first_element = True

    len_script = len(html_script)

    html_element_colletor = ''

    start_collecting = False

    between_html_element_collector = ''

    collecting_between_elements = False

    space_multi = 0

    space_step = 2

    closed_div_counter = 0

    opened_div_counter = 0

    old_close_num = 0

    old_open_num = 0

    line_code_collector = ''

    old_html_element_data = ''

    final_script = []

    for num_alpha in range(len_script):
        
        alpha = html_script[num_alpha]
        
        if start_collecting:
            
            html_element_colletor += alpha
            
        if alpha == '<':
            
            # start collecting '<' inside element
            
            start_collecting = True
            
            html_element_colletor += alpha
            
            if len(between_html_element_collector) != 0 and between_html_element_collector != ' ':
                
                # print(variable_name,'   +='+' '*(space_multi)+"'"+ between_html_element_collector+"'")
                # print()
                
                line_code_collector += between_html_element_collector
            
            collecting_between_elements = False

            between_html_element_collector = ''
            
        elif alpha == '>':
            
            # done collecting '>' inside element
            
            start_collecting = False
                        
            # print()
            
            # print(start_collecting, collecting_between_elements)
            
            an_html_exception_element = 0
            
            for html_element in list_exceptions_element:
                
                len_html_element = len(html_element)
                
                if html_element_colletor[:len_html_element] == html_element:
                
                    line_of_script = js_variable_name + '    +='+' '*(space_multi + space_step)+"'"+ html_element_colletor+"'"
                    
                    final_script.append(line_of_script)
                    
                    if mode == ' ':
                        
                        final_script.append(' ')
                    
                    # print(variable_name,'   +='+' '*space_multi+"'"+ html_element_colletor+"'")
                    
                    line_code_collector += between_html_element_collector
                
                    an_html_exception_element = 1
                    
            if not an_html_exception_element:
                
                # not except element like "<img> has no </img>"
            
                if html_element_colletor[:1] == "<" and html_element_colletor[-1:] == ">":
                
                    if html_element_colletor[:2] == '</':
                        
                        closed_div_counter += 1 
                        
                    elif html_element_colletor[:2] != '<!':
                        
                        opened_div_counter += 1 
                        
                if old_open_num != opened_div_counter and not first_element:
                
                    space_multi += space_step
                
                if first_element:
                    
                    # print('let', variable_name,'='+"'"+html_element_colletor+"'")
                    
                    line_of_script = 'let ' + js_variable_name +' ='+"'"+html_element_colletor+"'"
                    
                    final_script.append(line_of_script)
                    
                    if mode == ' ':
                        
                        final_script.append(' ')
                        
                elif  len(line_code_collector) == 0 and old_html_element_data == html_element_colletor.replace('/',''):
                    
                    # <div> == <div> old was <div></div>
                    
                    form_to_print = old_html_element_data + ''+ html_element_colletor
                    
                    # delete latest html element and replace it with a full one <div></div>
                    
                    if mode == ' ':
                        
                        del final_script[-1] # del space
                        del final_script[-1] # del html element
                        
                    else:
                    
                        del final_script[-1] # del html element
                    
                    #insert full html element
                    
                    line_of_script = js_variable_name + '    +='+' '*(space_multi)+"'"+ form_to_print+"'"
                    
                    final_script.append(line_of_script)
                    
                    if mode == ' ':
                        
                        final_script.append(' ')
                        
                    html_element_colletor = ''
                    
                elif len(line_code_collector) > 0 :
                    
                    if old_html_element_data[:2] != '</':
                        
                        form_to_print = old_html_element_data + ' '+ line_code_collector +' '+ html_element_colletor
                        
                        # print(variable_name,'   +='+' '*(space_multi)+"'"+ form_to_print+"'")
                        
                        # delete latest html element and replace it with a full one <div></div>
                        
                        if mode == ' ':
                            
                            del final_script[-1] # del space
                            del final_script[-1] # del html element
                            
                        else:
                        
                            del final_script[-1] # del html element
                        
                        #insert full html element
                        
                        line_of_script = js_variable_name + '    +='+' '*(space_multi)+"'"+ form_to_print+"'"
                        
                        final_script.append(line_of_script)
                        
                        if mode == ' ':
                            
                            final_script.append(' ')
                            
                    if old_html_element_data[:2] == '</':
              
                        list_local_elements = [old_html_element_data, line_code_collector, html_element_colletor]
                        
                        for elemnt in list_local_elements:
                                
                            if mode == ' ' and elemnt != list_local_elements[-1]:
                                
                                line_of_script = js_variable_name + '    +='+' '*(space_multi + 2)+"'"+ elemnt+"'"
                            
                                final_script.append(line_of_script)
                                
                                final_script.append(' ')
                                
                            elif mode == ' '  and elemnt == list_local_elements[-1]:
                                
                                line_of_script = js_variable_name + '    +='+' '*(space_multi - 2)+"'"+ elemnt+"'"
                            
                                final_script.append(line_of_script)
                                
                            elif mode != ' '  and elemnt == list_local_elements[-1]:
                                
                                line_of_script = js_variable_name + '    +='+' '*(space_multi)+"'"+ elemnt+"'"
                            
                                final_script.append(line_of_script)
                                
                            else:
                                
                                line_of_script = js_variable_name + '    +='+' '*(space_multi + 2)+"'"+ elemnt+"'"
                            
                                final_script.append(line_of_script)
                    
                    line_code_collector = ''
                    
                else:
                
                    line_of_script = js_variable_name + '    +='+' '*space_multi+"'"+ html_element_colletor+"'"
                    
                    final_script.append(line_of_script)
                    
                    if mode == ' ':
                        
                        final_script.append(' ')
                    
                    # print(variable_name,'   +='+' '*space_multi+"'"+ html_element_colletor+"'")
                    
                    line_code_collector += between_html_element_collector
                    
                    # print()
            
            first_element = False
            
            old_html_element_data = html_element_colletor
            
            html_element_colletor = ''
            
            collecting_between_elements = True
            
            if old_close_num != closed_div_counter:
                
                space_multi -= space_step
                
            old_close_num = closed_div_counter
            
            old_open_num = opened_div_counter
            
        elif collecting_between_elements:
            
            between_html_element_collector += alpha
            
    for line_of_html in final_script:
        
        print(line_of_html)
            
        
# html_to_js(html_script,'kk',mode='') 

def js_to_html(js_script, js_variable_name):
    
    html_script_collector = ''
    
    lines_list = []
    
    for char_num in range(len(js_script)):
        
        char = js_script[char_num]
        
        html_script_collector += char
        
        bg= 'let ' + js_variable_name + ' ='
        
        end_arg = js_variable_name + '    +='
        
        len_end_arg = len(end_arg)
        
        if html_script_collector == bg:
            
            html_script_collector = html_script_collector.replace(bg, '')
            
        elif html_script_collector[-len_end_arg:] == end_arg:
            
            phrase_len = len(html_script_collector) - len_end_arg
            
            phrase_with_apostrophes  = html_script_collector[:phrase_len]
            
            output_collector = ''
            
            stop = False
            
            for alpha in phrase_with_apostrophes:
                
                if alpha == "'" and not stop:
                    
                    output_collector += '' 
                    stop = True
                    
                else:
                    
                    output_collector += alpha
            
            clean_html_line = output_collector[:-2]
            
            lines_list.append(clean_html_line)
            
            html_script_collector = ''  
            
        elif char_num == len(js_script) - 1:
            
            clean_html_line = html_script_collector[1:-1]
            
            lines_list.append(clean_html_line)
            
            html_script_collector = ''  
    
    for x in lines_list:
        
        print(x)            
        
# js_to_html(js_script, 'kk')      
        

# print(list_html_element)
