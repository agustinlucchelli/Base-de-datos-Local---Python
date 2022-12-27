from xhtml2pdf import pisa
import pandas as pd

def crear_pdf(directorio_pdf, directorio_csv):
    
    result = open(directorio_pdf, "w+b")

    csv = pd.read_csv(directorio_csv)
    html  = csv.to_html()
    
    css_1 = """
<html>
<head>
<style>
    body {font-family: Arial, Helvetica, sans-serif;}

table {     font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;    margin: 45px;     width: 175px; text-align: left;    border-collapse: collapse; }

th {     font-size: 13px;     font-weight: normal;     padding: 8px;
    border-top: 4px solid #aabcfe;    border-bottom: 1px solid #fff; color: #0399; }

td {    padding: 8px;     background: #e8edff;     border-bottom: 1px solid #fff;
    color: #669;    border-top: 1px solid transparent; }

tr:hover td { background: #d0dafd; color: #339; }
</style>
</head>

<body>
"""

    css_2 = """
</body>
</html>
    """
    html = css_1 + html +css_2
    
    pisa.CreatePDF(
                html,
                dest=result
                )

    result.close()