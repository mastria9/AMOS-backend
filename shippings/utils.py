from suds.client import Client


import os
import re
import sys
import time
import base64
import ftplib
import PyPDF2
import shutil
from datetime import datetime
from pprint import PrettyPrinter
from django.conf import settings
import unidecode
import pytz
from django.template.loader import render_to_string
from suds.cache import NoCache
import requests
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
import xml.etree.ElementTree as ET


class GLS:
    def create(order,courier):
        #return xml to send
        return render_to_string(os.path.join('gls','parcel.xml'), {'order': order,"courier":courier})
        

    def process(shippings):
        pass


    def delete(shippings):
        pass

    def xml(self,shipping):
        data={}
        if "AB" in shipping.instructions:
            data["incoterm"]=10 # 10 = AB come consegnato (paga il mittente)
        else:
            data["incoterm"]=20 # 20 = paga il destinatario
        return render_to_string(os.path.join(settings.COURIER_TEMPLATE_DIR, 'gls_request.xml'), {'shipping': shipping,"data":data})

    def send(self,courier,xml):
        client = Client(courier.api_url, cache=NoCache())
        res=client.service.AddParcel(xml)
        return res

    def delete(self,shipObj):
        pp=PrettyPrinter()
        data = {
            "SedeGls": shipObj.courier.office_code,
            "CodiceClienteGls": shipObj.courier.client,
            "PasswordClienteGls": shipObj.courier.api_password,
            "NumSpedizione": shipObj.tracking
        }
        
        client = Client(shipObj.courier.api_url, cache=NoCache())
        res = client.service.DeleteSped(**data)
        # GLS FAULT : Risponde semrpe con il tag DescrizioneErrore
        if "avvenuta" in res.DescrizioneErrore:
            return True
        else:
            return res.DescrizioneErrore
        


    def process(self,shipObjs):
        courier=shipObjs[0].courier
        company=shipObjs[0].company.name
        headers = {
            'Origin': 'https://labelservice.gls-italy.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        }


        data = {
            '_xmlRequest': render_to_string(os.path.join(settings.COURIER_TEMPLATE_DIR,'gls_close_request.xml'),{'shippings':shipObjs,"courier":courier})
        }
        xml_file_name=courier.name+"_"+courier.office_code+"_"+shipObjs[0].tracking+".xml"
        with open(os.path.join(settings.SHIPPING_DIR,courier.name.lower(),"transmitted",xml_file_name),"w") as fd:
            fd.write(data["_xmlRequest"])
            fd.close()
        # Invio richiesta chiusura a GLS 
        res=requests.post('https://labelservice.gls-italy.com/ilswebservice.asmx/CloseWorkDayByShipmentNumber', headers=headers, data=data)
        
        with open(os.path.join(settings.SHIPPING_DIR,courier.name.lower(),"received",xml_file_name),"w") as fd:
            fd.write(res.text)
            fd.close()

        tracks=[]
        root=None
        errors=""
        try:
            root=ET.fromstring(res.text)
        except ET.ParseError:
            return "Non riesco a leggere la risposta di GLS"
        try:
            risultato=root.find('DescrizioneErrore').text
            if risultato=="OK":
                parcels=root.findall("Parcel")
                for parcel in parcels:
                    if parcel.find("esito").text=="OK":
                        tracks.append(str(parcel.find("NumeroDiSpedizioneGLSDaConfermare").text))
                    else:
                        ships=shipObjs.filter(tracking=str(parcel.find("NumeroDiSpedizioneGLSDaConfermare").text))
                        ships[0].error_message=str(parcel.find("esito").text)
                        ships[0].save()
                        errors="Alcune spedizioni non sono state confermate o erano state confermate in precedenza. Controlla i messaggi sulle singole spedizioni"
            else:
                return { "result":False, "message":risultato}
        except:
            return { "result":False, "message":"Errore imprevisto"}
            
            

        # CREO LA DISTINTA
        distinta = PdfDistintaGLS(courier.name.upper(), courier.office_code, courier.client,courier.code, company)
        
        
        rows = []
        for shipObj in shipObjs:
            if shipObj.tracking in tracks:
                data = {
                    "date": shipObj.created_at.strftime("%d/%m/%y"),
                    "numsped": courier.office_code + shipObj.tracking,
                    "dest": shipObj.name,
                    "loc": shipObj.town,
                    "ind": shipObj.address,
                    "prov": shipObj.province,
                    "cap": shipObj.cap,
                    "colli": str(shipObj.qty),
                    "peso": str(round(shipObj.weight,2)),
                    "bda": shipObj.reference,
                    "note": shipObj.instructions,
                }
                if shipObj.instructions is None:
                    data["note"]=""
                if int(float(shipObj.cash)) == 0:
                    data["sped_cs"]={"num": 0,"val": '0'}
                else:
                    data["sped_cs"] = {"num": 1,"val": str(shipObj.cash)}
                rows.append(data)
        
        filename=courier.name+"_"+courier.office_code+"_"+shipObjs[0].tracking+".pdf"
        filepath = os.path.join(settings.SHIPPING_DIR,courier.name.lower(),"list",filename)
        
        distinta.gen_pdf(filepath, rows)

        # Add distinta to the database
        distintaObj = Distinta(pdf=filename,courier=courier)
        distintaObj.save()
        for shipObj in shipObjs:
            distintaObj.shippings.add(shipObj)
            shipObj.shipping_list=filename
            shipObj.sent_at=datetime.now()
            shipObj.status="C"
            shipObj.save()
        distintaObj.save()
        return { "result" : True, "message" : errors }

class ShippingInterface():

    def __init__(self,shipping):
        self.shipping=shipping

    def create():
        if self.shipping.courier.name == "GLS":
            obj=GLS()
            obj.xml
            try:
                return obj.create(order,courier)
            except:
                return False
        elif courier.name == "DHL":
            obj=DHL()
            try:
                return obj.create(order,courier)
            except:
                return False
        elif courier.name == "BRT":
            obj=BRT()
            try:
                return obj.create(order,courier)
            except:
                return False

    def process(shipping):
        if shipping.courier.name == "GLS":
            obj=GLS()
            try:
                return obj.process(shipping)
            except:
                return False
        elif shipping.courier.name == "DHL":
            obj=DHL()
            try:
                return obj.create(shipping)
            except:
                return False
        elif shipping.courier.name == "BRT":
            obj=BRT()
            try:
                return obj.create(shipping)
            except:
                return False

    def delete(shipping):
        if shipping.courier.name == "GLS":
            obj=GLS()
            try:
                return obj.delete(shipping)
            except:
                return False
        elif shipping.courier.name == "DHL":
            obj=DHL()
            try:
                return obj.delete(shipping)
            except:
                return False
        elif shipping.courier.name == "BRT":
            obj=BRT()
            try:
                return obj.delete(shipping)
            except:
                return False







def uni(data):
    return unidecode.unidecode(data)

def reblank(data):
    return re.sub(r'[^.a-zA-Z0-9]', " ", data)

def delAccent(data):
    if "à" in data:
        data=data.replace("à","a'")
    if "è" in data:
        data=data.replace("è","e'")
    if "é" in data:
        data=data.replace("é","e'")
    if "ì" in data:
        data=data.replace("ì","i'")
    if "ò" in data:
        data=data.replace("ò","o'")
    if "ù" in data:
        data=data.replace("ù","u'")
    return data

            




class PDF:
    def read(self,filepath):
        data=None
        with open(filepath, 'rb') as pdffd:
            reader = PyPDF2.PdfFileReader(pdffd, strict=False)
            try:
                data={}
                text = reader.getPage(0).extractText()
                tracking = text.split("\n")[19].strip()
                data['tracking'] = tracking[:15]
                id=text.split("\n")[1].strip()
                data['id']=id
                ref = re.findall(r'Rif. (\d+)_(\d+)', text)[0]
                data['reference'] = ref[0] + ref[1]
                pdffd.close()
            except:
                pdffd.close()
                return None
        return data
    
    def merge(self, pdf_source=None):
        """
        saves a pdf with 6 labels per page
        :param pdf_source: full or relative path of the source pdf
        :param pdf_dest: full or relative path of the newly created pdf
        :param page_limit: limit the number of labels to be added in the final pdf. if not
               specified, all labels are added
        :return: None
        """
        try:
            # set values for default args
            
            dir_name, file_name = os.path.split(pdf_source)
            pdf_dest = os.path.join(dir_name, 'merged_'+file_name)
            
            page_limit = sys.maxsize

            reader = PyPDF2.PdfFileReader(open(pdf_source, 'rb'), strict=False)
            

            # if limit is specified,then limit the number of labels. otherwise
            # add all labels. if the specified limit is more than available
            # labels then just add all the labels
            NUM_OF_PAGES = min(reader.getNumPages(), page_limit)

            # divide the labels into segments of 6 labels per page
            segmented_pages = [list(range(NUM_OF_PAGES))[offset:offset + 6] for offset in range(0, NUM_OF_PAGES, 6)]
            
            # if the pdf has only one label then just copy the same pdf as output
            if NUM_OF_PAGES == 1:
                return

            first_page = reader.getPage(0)
            data_height = first_page.mediaBox.getHeight()
            data_width = first_page.mediaBox.getWidth()

            new_page_height = data_height * 3
            new_page_width = data_height * 2

            # create the pdf writer object
            pdf_writer = PyPDF2.PdfFileWriter()

            for dest_page in segmented_pages:
                new_pdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, new_page_width, new_page_height)
                translate_y = None

                for idx, source_page_num in enumerate(dest_page):
                    # update the translate y property for each 2 labels
                    if source_page_num % 2 == 0:
                        translate_y = data_height * (3 - idx // 2 - 1)
                    translate_x = (source_page_num % 2) * data_width

                    # add the current label to the pdf page
                    try:
                        new_pdf_page.mergeScaledTranslatedPage(
                            reader.getPage(source_page_num),
                            scale=1,
                            tx=translate_x,
                            ty=translate_y
                        )
                    except IndexError:
                        continue

                    # add this page to writer object
                pdf_writer.addPage(new_pdf_page)

            # save the merged pdf in source dir
            with open(pdf_source, 'wb') as fd:
                pdf_writer.write(fd)
            fd.close()
            return
        except:
            return None

    def multiMerge(self, pdf_sources,pdf_dest):
        """
        saves a pdf with 6 labels per page
        :param pdf_sources: list of full or relative path of the source pdf files
        :param pdf_dest: full or relative path of the newly created pdf
        :param page_limit: limit the number of labels to be added in the final pdf. if not
                specified, all labels are added
        :return: None
        """

        # set values for default args

        
        page_limit = sys.maxsize
        readers = [PyPDF2.PdfFileReader(open(pdf_source, 'rb'), strict=False) for pdf_source in pdf_sources]

        # if limit is specified,then limit the number of labels. otherwise
        # add all labels. if the specified limit is more than available
        # labels then just add all the labels
        num_of_pages = min(len(pdf_sources), page_limit)

        # divide the labels into segments of 6 labels per page
        segmented_pages = [list(range(num_of_pages))[offset:offset + 6] for offset in range(0, num_of_pages, 6)]
        

        first_page = readers[0].getPage(0)
        first_page.mediaBox.upperLeft = (0, 419)
        first_page.mediaBox.lowerRight = (290, 135)
        data_height = first_page.mediaBox.getHeight() + 50
        data_width = first_page.mediaBox.getWidth() + 70

        new_page_height = data_height * 3
        new_page_width = data_height * 2

        # create the pdf writer object
        pdf_writer = PyPDF2.PdfFileWriter()

        for dest_page in segmented_pages:
            new_pdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, new_page_width, new_page_height)
            translate_y = None

            for idx, source_page_num in enumerate(dest_page):
                # update the translate y property for each 2 labels
                if source_page_num % 2 == 0:
                    translate_y = data_height * (3 - idx // 2 - 1)
                translate_x = (source_page_num % 2) * data_width

                # add the current label to the pdf page
                try:
                    new_pdf_page.mergeScaledTranslatedPage(
                        readers[source_page_num].getPage(0),
                        scale=1,
                        tx=translate_x + 10,
                        ty=translate_y - 95
                    )
                except IndexError:
                    print('error')
                    continue

                # add this page to writer object
            pdf_writer.addPage(new_pdf_page)

        # save the merged pdf in source dir
        with open(pdf_dest, 'wb') as f:
            pdf_writer.write(f)
        
    def toBase64(self,inFilename):
        pdf_stream=None
        with open(inFilename, "rb") as fd:
            pdf_stream = base64.b64encode(fd.read())
        fd.close()
        return pdf_stream

    def writeFromBase64(self,pdfBase64,outFilename):
        with open(outFilename, 'wb') as f:
            f.write(base64.b64decode(pdfBase64))

        






class PdfDistintaGLS:
    
    def __init__(self, corriere, sede, codcliente, codcontratto, company):
        self.sede = sede
        self.corriere = corriere
        self.codcliente = codcliente + ' - ' + company
        self.contrattomit = codcontratto + ' - ' +company
        self.row_offset = 10
        left_size = 20
        start_document = 590
        self.table_column_header = start_document - 110
        self.col_date = left_size
        self.col_nsped = left_size + 40
        self.col_dest = left_size + 105
        self.col_loca = left_size + 240
        self.col_indi = left_size + 320
        self.col_prov = left_size + 460
        self.col_cap = left_size + 485
        self.col_colli = left_size + 515
        self.col_peso = left_size + 540
        self.col_bda = left_size + 570
        self.col_note = left_size + 615
        self.start_document = start_document

    

    def print_header(self, date, nsped, dest, loca, indi, prov, cap, colli, peso, bda, note):
        cv = self.cv
        cv.setFont('Helvetica', 8)
        cv.drawString(date, self.table_column_header, 'Data')
        cv.drawString(nsped,self.table_column_header, 'N° Sped.')
        cv.drawString(dest, self.table_column_header, 'Destinatario')
        cv.drawString(loca, self.table_column_header, 'Località')
        cv.drawString(indi, self.table_column_header, 'Indirizzo')
        cv.drawString(prov, self.table_column_header, 'Prov')
        cv.drawString(cap,  self.table_column_header, 'CAP')
        cv.drawString(colli,self.table_column_header, 'Colli')
        cv.drawString(peso, self.table_column_header, 'Peso')
        cv.drawString(bda,  self.table_column_header, 'BDA')
        cv.drawString(note, self.table_column_header, 'Note')
        cv.setFont('Helvetica', 10)
        cv.drawString(date,  self.table_column_header, '_' * 133)
        cv.setFont('Helvetica', 8)

    def print_totals(self, row_offset, tot):
        cv = self.cv
        cv.setFont('Helvetica', 13)
        diff_space = 18
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space,  'Totale spedizioni: ' + tot["sped"])
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 2,  'Totale colli: ' + tot["colli"])
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 3,  'Totale peso reale: ' + tot["peso"])

        if tot["sped_cs_num"] == '0':
            cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 5,  'Totale spedizioni in contrassegno: 0')
        else:
            cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 5,
                          'Totale spedizioni in contrassegno: ' + str(tot["sped_cs_num"]) + ' con valore complessivo di ' + str(tot["sped_cs_val"]) + ' Euro')

        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 6,  'Totale spedizioni in Porto Franco: ' + tot["sped"])
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 7,  'Totale spedizioni in Porto Assegnato: 0')
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 8,  'Totale spedizioni con assicurazione integrativa 10/10: 0 con valore complessivo di 0 Euro.')
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 9,  'Totale spedizioni con assicurazione integrativa ALL-IN: 0 con valore complessivo di 0 Euro.')
        cv.drawString(self.col_date, self.table_column_header - row_offset - diff_space * 10,  'Non sono presenti spedizioni con servizi Sprinter che prevendono un costo aggiuntivo.')

    def gen_pdf(self, filepath, data):
        cv = canvas.Canvas(filepath, pagesize=landscape(letter))
        cv.setLineWidth(.3)
        cv.setFont('Helvetica', 6)
        cv.drawString(self.col_date + 650, self.start_document + 3, 'Nevix Cloud - Web Services  © Copyright 2023')
        cv.setFont('Helvetica', 18)
        cv.drawString(self.col_date + 190, self.start_document - 20, 'Distinta spedizioni ' + self.corriere + ' :: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        cv.setFont('Helvetica', 15)
        cv.drawString(self.col_date, self.start_document - 40, 'Sede di appartenenza: ' +  self.sede)
        cv.drawString(self.col_date, self.start_document - 60, 'Codice cliente: ' +  self.codcliente)
        cv.drawString(self.col_date, self.start_document - 80, 'Contratto mittente: ' + self.contrattomit) 
        self.cv = cv
        self.print_header(self.col_date, self.col_nsped, self.col_dest,
                          self.col_loca, self.col_indi, self.col_prov,
                          self.col_cap, self.col_colli, self.col_peso, self.col_bda, self.col_note)

        is_first_page = True
        row_offset = self.row_offset
        tot = {
         "sped": len(data),
         "colli": 0,
         "peso": 0,
         "sped_cs_num": 0,
         "sped_cs_val": 0,
        }

        i = 0
        for r in data:
            if (i % 45 == 0 and i != 0):
                cv.showPage()
                cv.setFont('Helvetica', 8)
                self.table_column_header = 585
                self.print_header(self.col_date, self.col_nsped, self.col_dest,
                                  self.col_loca, self.col_indi, self.col_prov,
                                  self.col_cap, self.col_colli, self.col_peso, self.col_bda, self.col_note)
                row_offset = 10
            tot["colli"] += int(r["colli"])
            tot["peso"] += float(r["peso"])
            tot["sped_cs_num"] += r["sped_cs"]["num"]
            tot["sped_cs_val"] += round(float(r["sped_cs"]["val"]), 2)
            self.add_row(r["date"], r["numsped"], r["dest"][:28],
                         r["loc"][:15], r["ind"][:40], r["prov"],
                         r["cap"], r["colli"], r["peso"], 
                         r["bda"], r["note"], row_offset, self.table_column_header )
            row_offset += 10
            i += 1
        
        tot["peso"] = str(round(tot["peso"], 2))

        for k,v in tot.items():
            tot[k] = str(v)
        
        if row_offset >= 280:
            cv.showPage()
            cv.setFont('Helvetica', 8)
            self.table_column_header = 585
            row_offset = 10

        self.print_totals(row_offset, tot)

        cv.save()

    def add_row(self, date, nsped, dest, loc, ind, prov, cap, colli, peso, bda, note, offset, start_table):
        self.cv.drawString(str(self.col_date),  start_table - offset, date)
        self.cv.drawString(str(self.col_nsped), start_table - offset, nsped)
        self.cv.drawString(self.col_dest,  start_table - offset, dest)
        self.cv.drawString(self.col_loca,  start_table - offset, loc)
        self.cv.drawString(self.col_indi,  start_table - offset, ind)
        self.cv.drawString(self.col_prov,  start_table - offset, prov)
        self.cv.drawString(self.col_cap,   start_table - offset, cap)
        self.cv.drawString(self.col_colli, start_table - offset, colli)
        self.cv.drawString(self.col_peso,  start_table - offset, peso)
        self.cv.drawString(self.col_bda,   start_table - offset, bda)
        self.cv.drawString(self.col_note,  start_table - offset, note)



class BRT():
    pass

class DHL():
    pass