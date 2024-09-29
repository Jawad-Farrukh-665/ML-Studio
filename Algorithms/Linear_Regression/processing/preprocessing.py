from .data_sanitization import reading_file

def column_separation(file_path):
    dataframe = reading_file(file_path)
    columns = dataframe.columns
    pass
    return columns