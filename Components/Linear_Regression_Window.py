import customtkinter
from tkinter import filedialog, BooleanVar, colorchooser
from PIL import Image 
from Algorithms.Linear_Regression.processing.preprocessing import column_separation

filename = None
columns = []
is_dropdown_visible = False

def update_dropdowns(target_dropdown , predictor_dropdown, predictors):
    global columns
    if len(predictors) != 0:
        predictors.pop(0)
    target_selected = target_dropdown.get()
    predictor_selected = predictor_dropdown.get()
    target_options = [option for option in columns if option != predictor_selected]
    predictor_options = [option for option in columns if option != target_selected]
    target_dropdown.configure(values = target_options)
    predictor_dropdown.configure(values = predictor_options)
    predictors.append(predictor_selected)

def perform_linear_regression(selected_dataset_field, selected_type, target_dropdown, predictors, original_data, gradient_descent, learning_rate, linear_regression_color, original_data_color):
    props = {
        "filePath": selected_dataset_field.get(),
        "type": selected_type.get(),
        "target": target_dropdown.get(),
        "predictors": predictors,
        "originalData": original_data.get(), 
        "gradientDescent": gradient_descent.get(),
        "learningRate": learning_rate.get(),
        "linearRegressionColor": linear_regression_color.get(),
        "originalDataColor": original_data_color.get()
    }
    if props["target"] in props["predictors"]:
        print("Error")
    print(props)

def close_window(LR_Window):
    LR_Window.destroy()

def open_color_chooser(selected_color, entry):
    color_code = colorchooser.askcolor(title="Choose A Color For Linear Regression")
    if color_code[1]:
        selected_color.set(color_code[1])
        entry.delete(0, customtkinter.END)
        entry.insert(0, selected_color.get())

def learning_rate_toggle(gradient_descesnt_value, learning_rate_entry):
    if gradient_descesnt_value.get() == 1:
        learning_rate_entry.configure(state = "normal",  placeholder_text="Enter Learning Rate...")
    else:
        learning_rate_entry.delete(0, customtkinter.END)
        learning_rate_entry.configure( placeholder_text="",)
        learning_rate_entry.configure(state = "disabled")
        
def original_color_toggle(original_data_value, original_color_entry, button):
    if original_data_value.get() == 1:
        original_color_entry.configure(state = "normal",  placeholder_text="Enter Color For Original Data...")
        button.configure(state="normal")
    else:
        original_color_entry.delete(0, customtkinter.END)
        original_color_entry.configure( placeholder_text="",)
        original_color_entry.configure(state = "disabled")
        button.configure(state="disabled")

def handle_search_blur_on_click_outside(event, entries, LR_window):
    is_click_outside = True
    for entry in entries:
        if event.widget == entry:
            is_click_outside = False
            break
    if is_click_outside:
        entry.focus_set()
        LR_window.focus()

def update_radio_buttons(radio_button, dropdown_frame, customize_predictors_button, predictor_dropdown, target_dropdown, predictors):
    global columns
    if radio_button.cget("value") == 1 or radio_button.cget("value") == 3:
        selected_value = target_dropdown.get()
        if selected_value:
            columns = [column for column in column_separation(filename) if column != selected_value]
        dropdown_frame.grid_remove()
        customize_predictors_button.grid_remove()
        predictor_dropdown.configure(values=columns)
        predictor_dropdown.grid(row = 0, column=0, columnspan=2, sticky='we')
        update_dropdowns(target_dropdown, predictor_dropdown, predictors)
    else:
        predictor_dropdown.grid_remove()
        customize_predictors_button.grid(column=0, row=0, sticky='e')
    radio_button.configure(fg_color="#16423C")

def browse_file(entry, dropdown, dropdown_frame , predictors):
    global filename, columns
    filename = filedialog.askopenfilename()
    entry.delete(0, customtkinter.END)
    entry.insert(0, filename)
    dropdown.set("Select A Target Variable")
    selected_option = dropdown.get()
    columns = column_separation(filename)  
    dropdown.configure(values=columns)
    columns = [column for column in columns if column != selected_option]
    update_predictors(dropdown_frame , predictors)
    dropdown.configure(command=lambda selected_value: update_columns(selected_value, dropdown_frame , predictors))

def update_columns(selected_value, dropdown_frame , predictors):
    global columns
    if selected_value:
        columns = [column for column in column_separation(filename) if column != selected_value]
    update_predictors(dropdown_frame , predictors)

def update_predictors(dropdown_frame , predictors):
    for widget in dropdown_frame.winfo_children():
        widget.destroy()
    global options_vars
    options_vars = {option: BooleanVar(value=False) for option in columns}
    for i, (option, var) in enumerate(options_vars.items()):
        checkbox = customtkinter.CTkCheckBox(dropdown_frame, text=option, variable=var, command=lambda: update_selection(options_vars, predictors), text_color="#16423C")
        checkbox.grid(column=0, row=i, sticky='w')

def toggle_dropdown(dropdown_frame):
    global is_dropdown_visible
    if is_dropdown_visible:
        dropdown_frame.grid_forget()
        is_dropdown_visible = False
    else:
        dropdown_frame.grid(row=0, column=1, pady=10, padx=20, sticky="s")
        dropdown_frame.tkraise()
        is_dropdown_visible = True
    
def update_selection(options_vars, predictors):
    selected_values = [option for option, var in options_vars.items() if var.get()]
    predictors.clear()
    predictors.extend(selected_values)
    
def linear_regression_window():
    global columns
    LR_window = customtkinter.CTkToplevel()
    LR_window.title("Linear Regression")
    LR_window.geometry("700x700")
    LR_window.resizable(False, False)
    LR_window.columnconfigure((0,1), weight=1)
    LR_window.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
    LR_window.configure(fg_color="#E9EFEC")
    LR_window.attributes("-topmost", True)
    
    selected_type = customtkinter.StringVar(value="None")
    linear_regression_color = customtkinter.StringVar(value="#0000FF")
    original_data_color = customtkinter.StringVar(value="#FF0000")
    predictors = []
    
    uploading_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    uploading_frame.columnconfigure((0,1), weight=1)
    
    selected_dataset_field = customtkinter.CTkEntry(uploading_frame, width=320, fg_color="#E9EFEC", text_color='#16423C', placeholder_text_color="#4D6F6B", placeholder_text="Selected Dataset...")
    selected_dataset_field.grid(column=0, row=0, sticky='we', padx=(20,0))
    upload_icon = customtkinter.CTkImage(Image.open("Upload.png"), size=(15,15))
    upload_dataset_button = customtkinter.CTkButton(uploading_frame, fg_color="#16423C", text="Upload ", font=("Arial", 15), image=upload_icon, compound="left", command=lambda: browse_file(selected_dataset_field, target_dropdown, dropdown_frame, predictors), hover_color="#0E2F2B")
    upload_dataset_button.grid(column=1, row=0, sticky='w', padx=(5,0))
    
    uploading_frame.grid(row=0, column=0, columnspan=2)
    
    types_label = customtkinter.CTkLabel(LR_window, text="Types", fg_color="#E9EFEC", text_color="#16423C", font=("Arial", 20))
    types_label.grid(row=1, sticky="w", padx=8, column=0)
    
    types_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    types_frame.columnconfigure((0,1,2), weight=1)
    type1_radiobutton = customtkinter.CTkRadioButton(types_frame, fg_color="#E9EFEC", text_color="#16423C", hover=False, text="Simple Linear Regression", border_color="#16423C", variable=selected_type, value=1, command=lambda: update_radio_buttons(type1_radiobutton, dropdown_frame, customize_predictors_button, predictor_dropdown, target_dropdown, predictors), border_width_unchecked=2, border_width_checked=5)
    type1_radiobutton.grid(column=0, row=0)
    type2_radiobutton = customtkinter.CTkRadioButton(types_frame, fg_color="#E9EFEC", text_color="#16423C", hover=False, text="Multiple Linear Regression", border_color="#16423C", variable=selected_type, value=2, command=lambda: update_radio_buttons(type2_radiobutton, dropdown_frame, customize_predictors_button, predictor_dropdown, target_dropdown, predictors), border_width_unchecked=2, border_width_checked=5)
    type3_radiobutton = customtkinter.CTkRadioButton(types_frame, fg_color="#E9EFEC", text_color="#16423C", hover=False, text="Multivariate Linear Regression", border_color="#16423C", variable=selected_type, value=3, command=lambda: update_radio_buttons(type3_radiobutton, dropdown_frame, customize_predictors_button, predictor_dropdown, target_dropdown, predictors), border_width_unchecked=2, border_width_checked=5)
    type2_radiobutton.grid(column=1, row=0)
    type3_radiobutton.grid(column=2, row=0)
    types_frame.grid(column=0, sticky="we", row=2, columnspan=2)
    
    target_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    target_frame.columnconfigure((0,1), weight=1)
    
    target_dropdown = customtkinter.CTkOptionMenu(target_frame, width=210, fg_color="#16423C", button_color="#16423C", button_hover_color="#16423C", dropdown_fg_color="#E9EFEC", dropdown_text_color="#16423C", dropdown_hover_color="#B8BFBC", values=[])
    target_dropdown.set("Select A Target Variable")
    target_dropdown.grid(column=0, row=0, padx=30, pady=10)
    
    target_frame.grid(column=0, row=3, sticky="we")
    
    predictor_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    predictor_frame.columnconfigure((0,1), weight=1)
    
    predictor_dropdown = customtkinter.CTkOptionMenu(predictor_frame, width=210, fg_color="#16423C", button_color="#16423C", button_hover_color="#16423C", dropdown_fg_color="#E9EFEC", dropdown_text_color="#16423C", dropdown_hover_color="#B8BFBC", values=[], command=lambda selected_value: update_dropdowns(target_dropdown, predictor_dropdown, predictors))
    predictor_dropdown.set("Select A Predictor Variable")
    
    customize_predictors_button = customtkinter.CTkButton(predictor_frame, fg_color="#16423C", text="Customize Predictors", text_color="#E9EFEC", hover_color="#0E2F2B", command=lambda: update_selection(options_vars , predictors))
    customize_predictors_button.grid(column=0, row=0, sticky='e')
    dropdown_frame = customtkinter.CTkScrollableFrame(predictor_frame, fg_color="#E9EFEC", height=100)
    dropdown_frame.columnconfigure((0,1), weight=1)
    update_predictors(dropdown_frame , predictors)
    customize_predictors_button.configure(command=lambda: toggle_dropdown(dropdown_frame))
    predictor_frame.grid(column=1, row=3, padx=30)
    
    advance_linear_regression_options_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    advance_linear_regression_options_frame.columnconfigure((0,1,2), weight=1)
    
    original_data_checkbox = customtkinter.CTkCheckBox(advance_linear_regression_options_frame, fg_color="#16423C", checkmark_color="#E9EFEC", hover=False, text="Show Original Data", text_color="#16423C", border_color="#16423C", command=lambda: original_color_toggle(original_data_checkbox, original_color_entry, original_color_picker), onvalue=1, offvalue=0)
    original_data_checkbox.grid(column=0, row=0)
    
    gradient_descent_checkbox = customtkinter.CTkCheckBox(advance_linear_regression_options_frame, fg_color="#16423C", checkmark_color="#E9EFEC", hover=False, text="Gradient Descent", text_color="#16423C", border_color="#16423C", command=lambda: learning_rate_toggle(gradient_descent_checkbox, learning_rate), onvalue=1, offvalue=0)
    gradient_descent_checkbox.grid(column=1, row=0)
    
    learning_rate_frame = customtkinter.CTkFrame(advance_linear_regression_options_frame, fg_color="#E9EFEC")
    learning_rate_frame.columnconfigure((0,1), weight = 1)
    
    learning_rate_lable = customtkinter.CTkLabel(learning_rate_frame, text="Learning Rate: ", fg_color="#E9EFEC", text_color="#16423C")
    learning_rate_lable.grid(column=0, sticky='e', row=0)
    learning_rate = customtkinter.CTkEntry(learning_rate_frame, text_color="#16423C", placeholder_text_color="#1A4F43", fg_color="#E9EFEC", state="disabled")
    learning_rate.grid(column=1, row=0, sticky='w')
    
    learning_rate_frame.grid(column=2, row = 0)
    
    advance_linear_regression_options_frame.grid(column=0, row=4, columnspan=2, sticky="we")
    
    chart_and_color_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    chart_and_color_frame.columnconfigure((0,1,2), weight=1)
    chart_and_color_frame.rowconfigure((0,1), weight=1)
    
    chart_and_color_label = customtkinter.CTkLabel(chart_and_color_frame, text="Charts & Colors", fg_color="#E9EFEC", text_color="#16423C", font=("Arial", 20))
    chart_and_color_label.grid(row=0, column=0, sticky="w", padx=8)
    
    chart_and_color_frame.grid(column=0, columnspan=2, row=5, sticky="we")
    
    chart_and_color_options = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    chart_and_color_options.columnconfigure((0,1,2), weight=1)
    
    linear_regression_color_frame = customtkinter.CTkFrame(chart_and_color_options, fg_color="#E9EFEC")
    linear_regression_color_frame.columnconfigure((0,1), weight=1)
    linear_regression_color_frame.rowconfigure((0,1), weight=1)
    
    linear_regression_color_label = customtkinter.CTkLabel(linear_regression_color_frame, fg_color="#E9EFEC", text_color="#16423C", text="Linear Regression: ")
    linear_regression_color_label.grid(column=0, row=0, sticky='w', padx=50)
    linear_regression_color_entry = customtkinter.CTkEntry(linear_regression_color_frame, fg_color="#E9EFEC", text_color="#16423C", placeholder_text="Enter Color For Linear Regression", placeholder_text_color="#1A4F43", width=200)
    linear_regression_color_entry.grid(column=0, row=1, sticky='e')
    linear_regression_color_picker = customtkinter.CTkButton(linear_regression_color_frame, fg_color="#16423C", text_color="#E9EFEC", text="Choose", hover=False, width=75, command=lambda: open_color_chooser(linear_regression_color, linear_regression_color_entry))
    linear_regression_color_picker.grid(column=1, row=1, sticky='w')
    
    linear_regression_color_frame.grid(column=0,row=0,sticky='we')
    
    original_color_frame = customtkinter.CTkFrame(chart_and_color_options, fg_color="#E9EFEC")
    original_color_frame.columnconfigure((0,1), weight=1)
    original_color_frame.rowconfigure((0,1), weight=1)
    
    original_color_label = customtkinter.CTkLabel(original_color_frame, fg_color="#E9EFEC", text_color="#16423C", text="Original Data: ")
    original_color_label.grid(column=0, row=0, sticky='w', padx=50)
    original_color_entry = customtkinter.CTkEntry(original_color_frame, fg_color="#E9EFEC", text_color="#16423C", placeholder_text="Enter Color For Linear Regression", placeholder_text_color="#1A4F43", width=200, state="disabled")
    original_color_entry.grid(column=0, row=1, sticky='e')
    original_color_picker = customtkinter.CTkButton(original_color_frame, fg_color="#16423C", text_color="#E9EFEC", text="Choose", hover=False, width=75, command=lambda: open_color_chooser(original_data_color, original_color_entry), state="disabled")
    original_color_picker.grid(column=1, row=1, sticky='w')
    
    original_color_frame.grid(column=1,row=0,sticky='e')
    
    chart_and_color_options.grid(column=0, columnspan=2, row=6, sticky='we')
    
    error_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    error_frame.columnconfigure((0,1), weight=1)
    
    error_label = customtkinter.CTkLabel(error_frame, fg_color="#E9EFEC", text_color="#FF0000", text="", font=("Ariel", 18))
    error_label.grid(column=0, columnspan=2, row=0)
    
    error_frame.grid(column=0, columnspan=2, row=7, sticky='we')
    
    next_step_frame = customtkinter.CTkFrame(LR_window, fg_color="#E9EFEC")
    next_step_frame.columnconfigure((0,1), weight=1)
    
    cancel_button = customtkinter.CTkButton(next_step_frame, fg_color="#E9EFEC", text_color="#16423C", text="Cancel", font=("Ariel", 16), hover=False, command=lambda: close_window(LR_Window=LR_window), border_width=2, border_color="#16423C")
    cancel_button.grid(column=0, row=0, sticky='w', padx=30)
    
    continue_button = customtkinter.CTkButton(next_step_frame, fg_color="#16423C", text_color="#E9EFEC", text="Continue", font=("Ariel", 16), hover=False, command=lambda: perform_linear_regression(selected_dataset_field, selected_type, target_dropdown, predictors, original_data_checkbox, gradient_descent_checkbox, learning_rate, linear_regression_color_entry, original_color_entry))
    continue_button.grid(column=1, row=0, sticky='e', padx=30)
    
    next_step_frame.grid(column=0, columnspan=2, row=8, sticky='we')
    
    entries = [linear_regression_color_entry._entry, learning_rate._entry, original_color_entry._entry]
    
    LR_window.bind("<Button-1>", lambda event: handle_search_blur_on_click_outside(event, entries, LR_window))
    
