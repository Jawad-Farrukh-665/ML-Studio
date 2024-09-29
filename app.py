import customtkinter
from PIL import Image, ImageTk
from options import dropdown_options
from Components.Linear_Regression_Window import linear_regression_window
    
current_visible = None
all_options = []

def selectLanguage(language):
    language_menu.set(language)

def check_searched_entry():
    global all_options
    entry = search_entry.get()
    entry = entry.lower()
    complete_match = []
    partial_match = []
    for option in all_options:
        option_lower = option.lower()
        if entry == option_lower:
            complete_match.append(option_lower)
        elif entry in option_lower:
            partial_match.append(option_lower)
    return {
        'complete_matches': complete_match,
        'partial_match': partial_match
    }

def handle_search_blur_on_click_outside(event):
    internal_entry_widget = search_entry._entry
    if event.widget != search_entry and event.widget != internal_entry_widget:
        search_entry.focus_set()
        app.focus()

def on_hover(foreground, text, button):
    button.configure(text_color=text)
    button.configure(fg_color=foreground)
    

def on_leave(foreground, text, button):
    button.configure(text_color=text)
    button.configure(fg_color=foreground)

def hide_all():
    global option_buttons_list
    for option in option_buttons_list:
        for btn in option:
            btn.grid_remove()

def option_toggle(options, Row, button_row_dict):
    global current_visible
    if current_visible == options:
        hide_all()
        current_visible = None
    else:
        hide_all()
        for i, button in enumerate(options):
            button.grid(row=i+2+Row, column=0, pady=5, padx=30, sticky="e")
        current_visible = options
    adjust_button_positions(button_row_dict)

def adjust_button_positions(button_row_dict):
    start_row = 0
    for button, options in button_row_dict.items():
        button.grid(row=start_row, column=0, sticky="we", padx=30)
        if current_visible == options:
            start_row += len(options) + 1
        else:
            start_row += 1

app = customtkinter.CTk()
screen_height = app.winfo_height()
app.geometry("1000x{screen_height}")
app.title("ML Studio")
app.iconbitmap('ML 1.ico')
app.columnconfigure((0,2), weight=1)
app.columnconfigure(1, weight=8)
app.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)
app.configure(fg_color = "#E9EFEC")

#      |\   |  /\    \      /
#     | \  |  /  \    \    /
#    |  \ |  /____\    \  /
#   |   \|  /      \    \/

logo_image = Image.open("ML 1.png")
logo_image = logo_image.resize((75, 75))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = customtkinter.CTkLabel(app, image=logo_photo, text="")
logo_label.grid(row=0, column=0, padx=20, pady=20, sticky='w')

option_frame = customtkinter.CTkFrame(app, fg_color="#E9EFEC")
option_frame.columnconfigure((0,1,2), weight=1)
documentation_label = customtkinter.CTkLabel(option_frame, text="Documentation", text_color="#16423C", font=("Arial", 20))
documentation_label.grid(row=0, column=0, padx=20)
get_started_label = customtkinter.CTkLabel(option_frame, text="Get Started", text_color="#16423C", font=("Arial", 20))
get_started_label.grid(row=0, column=1, padx=20)
help_label = customtkinter.CTkLabel(option_frame, text="Help", text_color="#16423C", font=("Arial", 20))
help_label.grid(row=0, column=2, padx=20)
option_frame.grid(row=0, column=1, padx=50, sticky="we")

language_frame = customtkinter.CTkFrame(app, fg_color="#E9EFEC")
language_frame.columnconfigure(0, weight=1)

language_menu = customtkinter.CTkOptionMenu(language_frame, values=dropdown_options['languages'], command=selectLanguage, fg_color="#16423C", button_color="#16423C", button_hover_color="#16423C", dropdown_fg_color="#E9EFEC", dropdown_text_color="#16423C", dropdown_hover_color="#B8BFBC")
language_menu.grid(column=0, sticky="w")
language_frame.grid(row=0, column=2, sticky="we")


#  ________  
# |                |              |
# |                |              |
# |_______  O      |     ______   |________   _______     |   ______
#        |  |     _|    |     /   |       |  |      |     | /
#       |   |   /  |   |_ ___/    |       |  |      |     |/
# _____|    |   \_ |_  |______    |_______|  |______|___  |

search_frame = customtkinter.CTkFrame(app, fg_color="#E9EFEC")
search_frame.columnconfigure((0,1), weight=1)

search_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Search...", fg_color="#E9EFEC", text_color="#16423C", corner_radius=30, width=200)
search_entry.grid(row=0, column=0, sticky='we', padx=(0,5))
search_button = customtkinter.CTkButton(search_frame, text="Search", fg_color='#16423C', text_color="#E9EFEC", width= 100, command=check_searched_entry, hover_color="#0E2F2B")
search_button.grid(row=0, column=1, sticky="we")

search_frame.grid(row=1, column=0, sticky='ns')


sidebar_frame = customtkinter.CTkScrollableFrame(app, fg_color="#CCD3D0", width=285)
prediction_options = [
    customtkinter.CTkButton(sidebar_frame, text="Linear Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14), command=linear_regression_window),
    customtkinter.CTkButton(sidebar_frame, text="Logistic Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Support Vector Machines", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Decision Trees", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Random Forest", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="K-Nearest Neighbors", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Naive Bayes", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Gradient Boosting Machine", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="XGBoost", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Light Gradient Boosting Machine", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Cat Boost", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Elastic Net", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Ridge Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Lasso Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Polynomial Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Adaptive Boosting", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Extra Trees", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="K-Means Prediction Variation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14))
]
clustring_options = [
    customtkinter.CTkButton(sidebar_frame, text="K-Means Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Agglomerative Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Divisive Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="DBSCAN", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="OPTICS", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Gaussian Mixture Models", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="BIRCH", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Affinity Propagation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Spectral Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Fuzzy C-Mean", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="AIB", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="K-Medoids", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="CLARANS", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="HDBSCAN", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Fuzzy K-Mean", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="SNN Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Chameleon Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="DBCLASD", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Grid-Based Clustering", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14))
]
supervised_options = [
    customtkinter.CTkButton(sidebar_frame, text="Linear Discriminant Analysis", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Quadratic Discriminant Analysis", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Stacking", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Voting Classifier", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Bootstrap Aggregation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Support Vector Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="DTRV", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="RFRV", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="GBM Regression Variation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="XGBoost Regression Variation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="LightGBM Regression Variation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="CatBoost Regression Variation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="KNN Regresion Variation", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Bayesian Linear Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Gaussian Process Regresion", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Huber Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Quantile Regression", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14))
]
un_supervised_options = [
    customtkinter.CTkButton(sidebar_frame, text="CURE", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="DENCLUE", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Principal Component Analysis", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Independant Component Analysis", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="t-SNE", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="UMAP", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Factor Analysis", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Linear Discriminant Analysis", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Apriori Algorithm", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Eclat Algorithm", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Frequent Pattern Growth", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Isolation Forest", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
    customtkinter.CTkButton(sidebar_frame, text="Elliptic Envelope", fg_color="#CCD3D0", text_color='#16423C', font=("Arial", 14)),
]
prediction_button = customtkinter.CTkButton(sidebar_frame, text="Predictive Algorithms", font=("Arial",18), fg_color="#CCD3D0", text_color="#16423C", command=lambda: option_toggle(prediction_options, 0, button_row_dict))
prediction_button.grid(row=0, column=0, sticky="we", padx=30)
prediction_button.bind("<Leave>", lambda event: on_hover("#CCD3D0", "#16423C", prediction_button))
prediction_button.bind("<Enter>", lambda event: on_leave("#16423C", "#CCD3D0", prediction_button))
clustering_button = customtkinter.CTkButton(sidebar_frame, text="Clustering Algorithms", font=("Arial",18), fg_color="#CCD3D0", text_color="#16423C", command=lambda: option_toggle(clustring_options, 1, button_row_dict))
clustering_button.grid(row=1, column=0, sticky="we", padx=30)
clustering_button.bind("<Leave>", lambda event: on_hover("#CCD3D0", "#16423C", clustering_button))
clustering_button.bind("<Enter>", lambda event: on_leave("#16423C", "#CCD3D0", clustering_button))
supervised_button = customtkinter.CTkButton(sidebar_frame, text="Supervised Algorithms", font=("Arial",18), fg_color="#CCD3D0", text_color="#16423C", command=lambda: option_toggle(supervised_options, 2, button_row_dict))
supervised_button.grid(row=2, column=0, sticky="we", padx=30)
supervised_button.bind("<Leave>", lambda event: on_hover("#CCD3D0", "#16423C", supervised_button))
supervised_button.bind("<Enter>", lambda event: on_leave("#16423C", "#CCD3D0", supervised_button))
unsupervised_button = customtkinter.CTkButton(sidebar_frame, text="Un-Supervised Algorithms", font=("Arial",18), fg_color="#CCD3D0", text_color="#16423C", command=lambda: option_toggle(un_supervised_options, 3, button_row_dict))
unsupervised_button.grid(row=3, column=0, sticky="we", padx=30)
unsupervised_button.bind("<Leave>", lambda event: on_hover("#CCD3D0", "#16423C", unsupervised_button))
unsupervised_button.bind("<Enter>", lambda event: on_leave("#16423C", "#CCD3D0", unsupervised_button))

sidebar_frame.grid(row=2, column=0, sticky="ns", rowspan=20, pady=(10,10), padx=10)

option_buttons_list=[prediction_options, clustring_options, supervised_options, un_supervised_options]

prediction_options_texts = [button.cget("text") for button in prediction_options]
clustring_options_texts = [button.cget("text") for button in clustring_options]
supervised_options_texts = [button.cget("text") for button in supervised_options]
un_supervised_options_texts = [button.cget("text") for button in un_supervised_options]

all_options.extend(prediction_options_texts)
all_options.extend(clustring_options_texts)
all_options.extend(supervised_options_texts)
all_options.extend(un_supervised_options_texts)

button_row_dict = {
    prediction_button: prediction_options,
    clustering_button: clustring_options,
    supervised_button: supervised_options,
    unsupervised_button: un_supervised_options,
}

adjust_button_positions(button_row_dict)

main_frame = customtkinter.CTkFrame(app, fg_color="#CCD3D0")
main_frame.columnconfigure(0, weight=1)

main_frame.grid(column=1, row=2, sticky="wens", columnspan=2, padx= (0,20))

# app.bind("<Configure>", padding_adjustment)
app.bind("<Button-1>", handle_search_blur_on_click_outside)
app.mainloop()

