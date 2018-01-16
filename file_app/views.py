from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from .models import File
#from .views import FileView
from django.http import HttpResponse
from .serializers import FileSerializer
from string import digits
#pdf
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
#image
from PIL import Image
import pytesseract
import argparse
import cv2
import re


class FileView(APIView):

  parser_classes = (MultiPartParser, FormParser)

  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'file.html'
  def post(self, request, *args, **kwargs):

    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      file_path = "D:/file/fileupload"+file_serializer.data["file"]
      FilePointer = open(file_path, "r")
      t = file_path.split(".")
      if(t[1]=="pdf"):

          bt1 = ['define', 'describe', 'draw', 'find', 'identify', 'label', 'list', 'locate', 'match', 'memorise',
                 'name', 'recall', 'recite', 'recognize', 'relate', 'reproduce', 'select', 'state', 'tell', 'write']
          bt2 = ['compare', 'convert', 'demonstarte', 'describe', 'discuss', 'distinguish', 'explain',
                 'find out more information about', 'generalize', 'interpret', 'outline', 'paraphrase', 'predict',
                 'put into your own words', 'relate', 'restate', 'summarize', 'translate', 'visualize']
          bt3 = ['apply', 'calculate', 'change', 'choose', 'complete', 'construct', 'examine', 'illustrate',
                 'interpret', 'make', 'manipulate', 'modify', 'produce', 'put into practice', 'put together', 'solve',
                 'show', 'translate', 'use']
          bt4 = ['advertise', 'analyse', 'categoriase', 'compare', 'contrast', 'deduce', 'differenciate', 'distinguish',
                 'examine', 'explain', 'identify', 'investigate', 'seperate', 'subdivide', 'take apart']
          bt5 = ['argue', 'assess', 'choose', 'compose', 'construct', 'create', 'criticise', 'critique', 'debate',
                 'decide', 'defend', 'design', 'determine', 'device', 'discuss', 'estimate', 'evaluate', 'formulate',
                 'imagine', 'invent', 'judge', 'justify', 'plan', 'predict', 'prioritise', 'propose', 'rate',
                 'recommend', 'select', 'value']
          bt6 = ['add to', 'argue', 'assess', 'choose', 'combine', 'compose', 'construct', 'create', 'debate', 'decide',
                 'design', 'determine', 'devise', 'discuss', 'forcast', 'formulate', 'hypothesise', 'imagine', 'invent',
                 'judge', 'justify', 'originate', 'plan', 'predict', 'priortise', 'propose', 'rate', 'recommend',
                 'select', 'verify']
          bt = {'bt1': bt1, 'bt2': bt2, 'bt3': bt3, 'bt4': bt4, 'bt5': bt5, 'bt6': bt6}
          my_file = os.path.join(file_path)
          log_file = os.path.join("D:/file/fileupload/media/log.txt")

          password = ""
          extracted_text = ""

          # Open and read the pdf file in binary mode
          fp = open(my_file, "rb")

          # Create parser object to parse the pdf content
          parser = PDFParser(fp)

          # Store the parsed content in PDFDocument object
          document = PDFDocument(parser, password)

          # Check if document is extractable, if not abort
          if not document.is_extractable:
              raise PDFTextExtractionNotAllowed

          # Create PDFResourceManager object that stores shared resources such as fonts or images
          rsrcmgr = PDFResourceManager()

          # set parameters for analysis
          laparams = LAParams()

          # Create a PDFDevice object which translates interpreted information into desired format
          # Device needs to be connected to resource manager to store shared resources
          # device = PDFDevice(rsrcmgr)
          # Extract the decive to page aggregator to get LT object elements
          device = PDFPageAggregator(rsrcmgr, laparams=laparams)

          # Create interpreter object to process page content from PDFDocument
          # Interpreter needs to be connected to resource manager for shared resources and device
          interpreter = PDFPageInterpreter(rsrcmgr, device)

          # Ok now that we have everything to process a pdf document, lets process it page by page
          for page in PDFPage.create_pages(document):
              # As the interpreter processes the page stored in PDFDocument object
              interpreter.process_page(page)
              # The device renders the layout from interpreter
              layout = device.get_result()
              # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
              for lt_obj in layout:
                  if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                      extracted_text += lt_obj.get_text()

          # close the pdf file
          fp.close()
          """
          data = extracted_text.encode("utf-8").lower()
          read1 = data.split("q")

          btperq = []
          for i in range(1, len(read1)):
              btlevellist = []
              read1[i] = read1[i].translate(None, digits)
              read1[i] = re.sub('[.,!?]', '', read1[i])
              t = read1[i].split(" ")
              for word in range(len(t)):
                  for values in bt.values():
                      for keywords in values:
                          if (t[word] == keywords):
                              btlevellist.append(bt.keys()[bt.values().index(values)])
              btperq.append(btlevellist)
          senddata = {'question': read1, 'btlevel': btperq, 'list': zip(read1, btperq)}
          return Response(senddata, template_name='file.html')
           """
          return  HttpResponse( nextracted_text.encode("utf-8"))


          #return Response("it is pdf")
      #response = HttpResponse(FilePointer)
      #response['Content-Disposition'] = 'attachment; filename=NameOfFile'
      #return response
      elif(t[1]=="jpg"):

          image = cv2.imread(file_path)
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

          # check to see if we should apply thresholding to preprocess the
          # image
          #if args["preprocess"] == "thresh":
          gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

          # make a check to see if median blurring should be done to remove
          # noise
          # elif args["preprocess"] == "blur":
          #gray = cv2.medianBlur(gray, 3)

          # write the grayscale image to disk as a temporary file so we can
          # apply OCR to it
          filename = "{}.png".format(os.getpid())
          cv2.imwrite(filename, gray)

          # load the image as a PIL/Pillow image, apply OCR, and then delete
          # the temporary file
          text = pytesseract.image_to_string(Image.open(filename))
          os.remove(filename)
          return HttpResponse(text)
      #return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          bt1=['define','describe','draw','find','identify','label','list','locate','match','memorise','name','recall','recite','recognize','relate','reproduce','select','state','tell','write']
          bt2=['compare','convert','demonstarte','describe','discuss','distinguish','explain','find out more information about','generalize','interpret','outline','paraphrase','predict','put into your own words','relate','restate','summarize','translate','visualize']
          bt3=['apply','calculate','change','choose','complete','construct','examine','illustrate','interpret','make','manipulate','modify','produce','put into practice','put together','solve','show','translate','use']
          bt4 = ['advertise','analyse','categoriase','compare','contrast','deduce','differenciate','distinguish','examine','explain','identify','investigate','seperate','subdivide','take apart']
          bt5 = ['argue','assess','choose','compose','construct','create','criticise','critique','debate','decide','defend','design','determine','device','discuss','estimate','evaluate','formulate','imagine','invent','judge','justify','plan','predict','prioritise','propose','rate','recommend','select','value']
          bt6 = ['add to','argue','assess','choose','combine','compose','construct','create','debate','decide','design','determine','devise','discuss','forcast','formulate','hypothesise','imagine','invent','judge','justify','originate','plan','predict','priortise','propose','rate','recommend','select','verify']
          bt = {'bt1': bt1, 'bt2': bt2,'bt3':bt3,'bt4':bt4,'bt5':bt5,'bt6':bt6}
          data=FilePointer.read()
          data = data.lower()
          read1 = data.split("q")
          btperq = []
          for i in range(1,len(read1)):
              btlevellist=[]
              read1[i]=read1[i].translate(None,digits)
              read1[i] = re.sub('[.,!?]', '', read1[i])
              t = read1[i].split(" ")
              for word in range(len(t)):
                  for values in bt.values():
                      for keywords in values:
                          if(t[word]==keywords):
                              btlevellist.append(bt.keys()[bt.values().index(values)])
              btperq.append(btlevellist)
          senddata = {'question':read1,'btlevel':btperq,'list':zip(read1, btperq)}
          return Response(senddata, template_name='file.html')







    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class File1(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'file.html'

    def get(self, request):

        return Response()

