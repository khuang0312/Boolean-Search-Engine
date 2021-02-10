# this contains the main routine for the program



from os import walk

from document import Document


if __name__ == "__main__":
   main_folder = "DEV/" # folder of webpages 
   

   documents = []

   # goes through files...
   for domain, dir, pages in walk(main_folder):
       for p in pages:
           path = domain + "/" + p
           doc = Document(path)
           documents.append(doc)
                              

   
