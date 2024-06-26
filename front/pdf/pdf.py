def CreerPresentation(id_rapport,headers):
    import reportlab
    from reportlab.pdfgen import canvas 
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet
    import os
    import subprocess
    import sys
    import requests




    # ###################################
    # Content

    rapport_query       = requests.get(f'http://192.168.1.119:8000/rapport/{id_rapport}',headers=headers)
    rapport_infos       = rapport_query.json()
    medecin_query       = requests.get(f'http://192.168.1.119:8000/medecin/{rapport_infos['MED_ID']}',headers=headers)
    rapport_med         = medecin_query.json()
    echantillon_query   = requests.get(f'http://192.168.1.119:8000/echantillons/{id_rapport}',headers=headers)
    rapport_echantillon = echantillon_query.json() 
    medicament1_query   = requests.get(f'http://192.168.1.119:8000/medicament/{rapport_echantillon[0]['MEDI_ID']}',headers=headers)
    rapport_medicament1 = medicament1_query.json()
    medicament2_query   = requests.get(f'http://192.168.1.119:8000/medicament/{rapport_echantillon[1]['MEDI_ID']}',headers=headers)
    rapport_medicament2 = medicament1_query.json()
    print(rapport_medicament1)
    print(rapport_medicament2)




    PDFTitle = f"Fiche de présentation rapport {id_rapport}"
    fileName = f'Fiche de présentation rapport {id_rapport}.pdf'
    documentTitle = 'GSB Applivisiteur - Fiche de présentation'
    image = "pdf/logoGSB.png"
    footer = "2024 GSB Applivsiteur"

    textPraticien = f'Praticien : Dr. {rapport_med['MED_NOM']} {rapport_med['MED_PRENOM']}'

    Title = "Médicament(s) :"

    LabelMedicaments1 = rapport_medicament1[0]['MEDI_LABEL']
    Composition1 = rapport_medicament1[0]['MEDI_COMPOSITION']
    Effet1 = rapport_medicament1[0]['MEDI_EFFETS']
    CI1 = rapport_medicament1[0]['MEDI_CONTREINDIC']
    Prix1 = rapport_medicament1[0]['MEDI_PRIX']

    LabelMedicaments2 = rapport_medicament2[0]['MEDI_LABEL']
    Composition2 = rapport_medicament2[0]['MEDI_COMPOSITION']
    Effet2 = rapport_medicament2[0]['MEDI_EFFETS']
    CI2 = rapport_medicament2[0]['MEDI_CONTREINDIC']
    Prix2 = rapport_medicament2[0]['MEDI_PRIX']

    textMedicament1 = [f'Quantité : {rapport_echantillon[0]['ECH_NOMBRE']}',f'Composition : {Composition1}',f'Effet(s) : {Effet1}',f'Contre-indication(s) : {CI1}',f'Prix : {Prix1}']
    textMedicament2 = [f'Quantité : {rapport_echantillon[1]['ECH_NOMBRE']}',f'Composition : {Composition2}',f'Effet(s) : {Effet2}',f'Contre-indication(s) : {CI2}',f'Prix : {Prix2}']



    # ###################################
    # 0) Create document 


    
    username = os.environ.get('USERNAME')
    path = f"C:/Users/{username}/Downloads/"
    pdf = canvas.Canvas(path + fileName)
    pdf.setTitle(documentTitle)
    y = 740
    pdf.drawImage(image, 30, y, width=121, height=67)

    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    text = pdf.beginText(180, 750)
    text.setFont("Helvetica", 27)
    text.textLine(PDFTitle)
    pdf.drawText(text)

    pdfmetrics.registerFont(
        TTFont('abc', 'arial.ttf')
    )
    pdf.setFont('abc', 36)

    pdf.setFont("Helvetica", 24)

    y-=40
    text = pdf.beginText(40, y)
    text.setFont("Helvetica", 18)
    text.textLine(textPraticien)

    pdf.drawText(text)

    #Médicaments

    y-=50
    text = pdf.beginText(40, y)
    text.setFont("Helvetica-Bold", 24)
    text.textLine(Title)
    pdf.drawText(text)


    #Informations médicaments 1

    text = pdf.beginText(40, 600)
    text.setFont("Helvetica", 18)
    text.textLine(LabelMedicaments1)
    text.moveCursor(14,20)
    pdf.line(40,595,40+float(len(rapport_medicament1[0]['MEDI_LABEL'])*8.5),595)
    for line in textMedicament1:
        text.textLine(line)
    pdf.drawText(text)

    #Informations médicaments 2
    text = pdf.beginText(40, 450)
    text.setFont("Helvetica", 18)
    text.textLine(LabelMedicaments2)
    text.moveCursor(14, 20)
    pdf.line(40,445,40+float(len(rapport_medicament1[0]['MEDI_LABEL'])*8.5),445)
    for line in textMedicament2:
        text.textLine(line)
    pdf.drawText(text)

    text = pdf.beginText(250, 50)
    text.setFont("Helvetica", 10)
    text.textLine(footer)
    pdf.drawText(text)

    pdf.save()
    pdf.showPage()
    output = f"\"{path}{fileName}\""
    subprocess.Popen([path+fileName], shell=True)
    return output
    #os.system(cmd)
