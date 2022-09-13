e


html_script = """<div id="wrapper"> <header> <div class="iconDiv" tooltip="Load file" tabindex="0"> <div class="iconSVG"> <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1"> <path stroke-linecap="round" stroke-linejoin="round" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" /> </svg> </div> </div> <div class="iconDiv" tooltip="Download" tabindex="0"> <div class="iconSVG"> <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1"> <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /> </svg> </div> </div> <div class="spacer"></div> <div class="divider"></div> <div class="iconDiv" tooltip="Notifications" tabindex="0"> <div class="iconSVG"> <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1"> <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /> </svg> </div> </div> <div class="iconDiv" tooltip="Log out" tabindex="0"> <div class="iconSVG"> <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1"> <path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" /> </svg> </div> </div> </header> </div>"""

# NO data like this <!--<div> </div>-->  is acceptable
# f1 -> join lines


print('Report bugs:')

print('Facebook: https://www.facebook.com/kzkamalzaitar/ (More active here)')

print()
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
            
        
# html_to_js(html_script,'kk',mode=' ') 

# script without space

# html_to_js(html_script,'kk') 


