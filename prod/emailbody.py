from prod.separatevalue import SeparateValue

class BuildBodyEmail(object):

    def __init__(self,filename:str):

        self.filename = filename
        self.style = ""
        self.title = self.reindex_date()

    def create_html_table_body(self,df):
        nclss = ""
        row_data = ''
        title = 'Top 10 clients' if df.columns[0] == 'Client' else  df.columns[0]
        k = []
        for l in range(df.shape[0]):
            row_data +='\n<tr> \n'
           
            for c in range(df.shape[1]):
                
                nclss = 'clss' if c == df.shape[1] - 1 else ''
                if ((l % 2) == 0) : #not an even row and the start of a new row
                    row_data += f'<td class = "tg-dg7a {nclss}">'+str(df.iloc[l,c])+'</td>\n'
                else: 
                    row_data += f'<td class = "tg-0lax {nclss}">'+str(df.iloc[l,c])+'</td>\n'
 
            row_data +='\n</tr> \n'

        if title == 'Point Vente':
            for c in range(df.shape[1]):
                p = 0
                for l in range(df.shape[0]):
                    v =str(df.iloc[l,c]).replace(" ","")
                    if v.isdigit():
                        p += float(v) 
                k.append(p)
            row_data += '''
                        <tr style="font-weight: bold;">
                            <td class = "tg-0lax ">TOTAL</td>
                            <td class = "tg-0lax ">'''+ SeparateValue(int(k[1])).generate_value()+'''</td>
                            <td class = "tg-0lax ">'''+  SeparateValue(int(k[2])).generate_value()+'''</td>
                            <td class = "tg-0lax ">'''+ SeparateValue(int(k[3])).generate_value()+'''</td>
                            <td class = "tg-0lax ">'''+ str(int(round((k[3]/k[2])*100)))+'''%</td>
                            <td class = "tg-0lax ">'''+ SeparateValue(int(k[5])).generate_value()+'''</td>
                            <td class = "tg-0lax clss">'''+ str(int(round((k[5]/k[2])*100)))+'''%</td>
                        </tr>\n
                        '''

        table = '''\
                <container style="overflow-x:auto;">
                    <h3 style="color:#005abb">'''+  title +''':</h3>
                            <table class="tg">
                                <thead>
                                    <tr class = "header">
                                    <th class = "tg-0pky">'''+df.columns[0]+'''</th>
                                    <th class = "tg-0lax">'''+df.columns[1]+'''</th>
                                    <th class = "tg-0lax">'''+df.columns[2]+'''</th>
                                    <th class = "tg-0lax">'''+df.columns[3]+'''</th>
                                    <th class = "tg-0lax">'''+df.columns[4]+'''</th>
                                    <th class = "tg-0lax">'''+df.columns[5]+'''</th>
                                    <th class = "tg-0lax ">'''+df.columns[6]+'''</th>
                                    </tr>
                                </thead>
                                <tbody>
                                ''' +row_data+ '''
                                </tbody>
                            </table>
                </container>
                <br/>
                '''           
        
        return table
        
    def reindex_date(self):
        #print(self.filename)
        c = self.filename.split('Encaissement')[1].split('_')[0].split("du")
        d1 = c[0].strip().split("-")
        d2 = c[1].strip().split("-")
        d1.reverse()
        d1 = "/".join(d1) 
        d2.reverse()
        d2 = "/".join(d2)

        if d1 != d2:

            self.style = '''<style type="text/css">
                            .tg  {border-collapse:collapse;border-color:#ffc1074d;border-spacing:0;border-style:solid;border-width:1px;}
                            .tg td{background-color:#fff;border-color:#aaa;border-style:solid;border-width:0px;color:#333;
                            font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;word-break:normal;}
                            .tg th{background-color:#f38630;border-color:#aaa;border-style:solid;border-width:0px;color:#fff;
                            font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
                            .tg .tg-dg7a{background-color:#FCFBE3;border-color:inherit;text-align:left;vertical-align:top}
                            .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
                            .tg .tg-0lax{text-align:left;vertical-align:top}
                            .clss {font-weight: bold; font-size: 17px !important; background: #FCFBE3 !important; text-align: center !important}
                            </style>
                        '''

            return f"des journées du <strong>{d1} au {d2}</strong>"
        else:

            self.style = '''<style type="text/css">
                            .tg  {border-collapse:collapse;border-color:#aaaaaa57;border-spacing:0;border-style:solid;border-width:1px;}
                            .tg td{background-color:#EBF5FF;border-color:#aaa;border-style:solid;border-width:0px;color:#333;
                            font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;word-break:normal;}
                            .tg th{background-color:#409cff;border-color:#aaa;border-style:solid;border-width:0px;color:#fff;
                            font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;word-break:normal;}
                            .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
                            .tg .tg-0lax{text-align:left;vertical-align:top}
                            .tg .tg-dg7a{background-color:#D2E4FC;text-align:left;vertical-align:top}
                            .clss {font-weight: bold; font-size: 17px !important; background: #ffc107bd !important; text-align: center !important}
                        </style>
                        '''
            
            return f"de la journée du <strong>{d1}</strong>"
        
    def create_html_email(self,body):
        
        return '''\

                <!DOCTYPE html>
                        <html>
                                <head>
                                    <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
                                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
                                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    ''' + self.style + '''
                                </head>

                                <body bgcolor="#FFF" style="width: 100%; font-family:cursive; font-size:15px;">
                                    <p>Bonjour DC,</p>
                                    <p>Ci-joint le fichier Production vs Encaissement '''+ self.title +''' et en dessous</p>
                                    <p>un résumé des impayés par différentes rubriques.</p>
                                    <br/>

                                    '''+ body +'''
                                    <h3 style="color:red"><strong>NB:</strong>Si certains points de ventes n'apparaissent pas c'est qu'il n'y a pas eu de production.</h3>
                                </body>
                        </html>
                '''

# <h3>RESUME IMPAYES PAR:</h3>

