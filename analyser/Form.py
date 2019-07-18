
import re

class Formalyse:
    def __init__(self,htmlText,url):
        self.text = self.setFormText(htmlText)
        self.tag = self.setFormStartTag(self.text)
        self.name = self.setFormField(self.tag,"name=")
        self.action = self.setFormField(self.tag,"action=")
        self.params = self.setParams(self.text.split(self.tag,1)[1])
        self.url = url
        self.path, self.file = self.pathFinder(self.url)
        self.actionUrl = self.setActionUrl(self.url,self.path,self.action)

    def setFormField(self,text,textBox):
        '''
            Get input field names from HTML form

            :param text: form text
            :param textBox: form tag name
            :return: form name
        '''
        delimiter='\"'
        
        if (text.find(textBox+delimiter)!=-1):
            formName = text.split(textBox+delimiter,1)[1]
            return formName.split(delimiter,1)[0]
        else:
            delimiter = '\''
            if (text.find(textBox+delimiter)!=-1):
                formName = text.split(textBox+delimiter,1)[1]
                return formName.split(delimiter,1)[0]
        return ""
            

    def setFormText(self, text):
        '''
            Get HTML form from page source

            :param text: page source
            :return: HTML form
        '''
        startFormText = text.split('<form',1)[1] # After <form>
        formText = startFormText.split('/form>',1)[0] # Before </form>
        return formText

    def setFormStartTag(self,text):
        '''
            Get form tag (header)

            :param text: HTML form
            :return: form header
        '''
        return text.split('>',1)[0] # <form> delimiter text

    
    def setParams(self,text):
        '''
            Search the 'name="' string within the page code to get the name of all inputs fields

            :param text: HTML form text after header tag
            :return: form input fields list with name and range
        '''
        # Define the index of fields
        textBox = 'name='
        delimiter = '\''
        fieldPos = [m.start() for m in re.finditer(textBox+delimiter, text)]
        if len(fieldPos) == 0:
            delimiter = '\"'
            fieldPos = [m.start() for m in re.finditer(textBox+delimiter, text)]
        fieldPos = [x+6 for x in fieldPos]
        
        # With the index of all names, copy them to a list 
        paramNames = self.getFieldValue(text,fieldPos,delimiter)            
        
        minLength = 'minlength='
        maxLength = 'maxlength='
        ranges = []
        for param in paramNames:
            tempText = text.rsplit(textBox+delimiter+param+delimiter,1)[1]
            tempText = tempText.split('>',1)[0]
            if(tempText.find(minLength)!=-1):
                minValue = tempText.split(minLength+delimiter,1)[1]
                minValue = minValue.split(delimiter,1)[0]
                if(tempText.find(maxLength)!=-1):
                    maxValue = tempText.split(maxLength+delimiter,1)[1]
                    maxValue = maxValue.split(delimiter,1)[0]
                else:
                    maxValue = minValue                       
            elif(tempText.find(maxLength)!=-1):
                maxValue = tempText.split(maxLength+delimiter,1)[1]
                maxValue = maxValue.split(delimiter,1)[0]
                minValue = maxValue
            else:
                minValue = 0
                maxValue = 11 # CPF
            ranges.append((minValue,maxValue))
        # minValue = 0
        return dict(zip(paramNames,ranges))

    def getFieldValue(self,textOrigin,positions,delimiter):
        '''
            Get input field minimum and maximum values

            :param textOrigin: input field on html source
            :param positions: all input field locations
            :param delimiter: used delimiter on html source
            :return: array of input fields with values
        '''
        fields = []
        for index in positions:
            fieldValue = textOrigin[index:]
            fieldValue = fieldValue.split('>',1)[0]
            startField = textOrigin[:index]
            startField = startField.rsplit('<',1)[1]
            if (fieldValue.find('type=\"submit\"')==-1 and fieldValue.find('type=\'submit\'')==-1) and (startField.find('type=\"submit\"')==-1 and startField.find('type=\'submit\'')==-1): ## CHECH THIS
                fieldValue = fieldValue.split(delimiter,1)[0]
                fields.append(fieldValue)
        return fields

    def setActionUrl(self, url, path,action):
        '''
            Define action url of a HTML form

            :param url: HTML form source url
            :param path: url path
            :param action: url action found on HTML form source
            :return: complete url action
        '''
        if action[0] == '?':
            return url + action
        else:
            return path + '/' + action
        
    def pathFinder(self, url):
        return tuple(url.rsplit('/',1))