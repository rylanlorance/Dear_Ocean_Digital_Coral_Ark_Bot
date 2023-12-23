import re
import datetime

class DigiArkFilenameFormatValidator():

     def generate_filename_format_report_from_filenames(self, filenames: list):
         number_of_files = len(filenames)
         number_of_correct_files = 0

         for filename in filenames:
             try:
                  self.validate_filename_format_for_one_file(
                       filename
                  )
             except Exception as e:
                  print('E')


     #     try:
     #          for filename in filenames:
          
     #     except Exception as e:
              

              




     def validate_filename_format_for_one_file(self, filename: str):
          print('validating filename format for one file')
          file_name_parsed = re.split(r"\s|_|\.+", filename)
          print("file_name_parsed", file_name_parsed)

          filename_id = file_name_parsed[0]
          filename_dt = file_name_parsed[1]
          filename_loc_id = file_name_parsed[2]
          filename_user_id = [file_name_parsed[3], file_name_parsed[4]]

          try:
               if len(file_name_parsed) != 9:
                    raise ValueError(f"filename format error: [{filename}]"
                                      "Incorrect number of fields.")

               self.validate_filename_format_file_id(filename_id)
               self.validate_filename_format_dt(filename_dt)
               self.validate_filename_format_location_id(filename_loc_id)
                
            
          except Exception as e:
               print("error!", e)
               return False

     def validate_filename_format_file_id(self, file_id):            
          if len(file_id) != 6:
               raise ValueError("Filename_ID_Error. Incorrect number of values.")

          if not file_id.isnumeric():
               raise ValueError("Filename_ID_Error. Filename_id can only contain digits.")

     def validate_filename_format_dt(self, dt):
          if not bool(datetime.datetime.strptime(dt, "%Y%m%d")):
               raise ValueError("Filename Date Format Error: Must be in %Y%m%d format.")
     
     def validate_filename_format_location_id(self, loc_id):
          if len(loc_id) != 3:
               raise ValueError("Filename Location Id Format Error: Must be 3 characters long.")
     
             
