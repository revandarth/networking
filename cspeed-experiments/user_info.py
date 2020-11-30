import os.path
from enum import Enum
import readline

class ConnType(Enum):
    dial_up = 0
    cable = 1
    dsl = 2
    fiber = 3
    wireless_broadband = 4
    mobile = 5
    satellite = 6
    company_nw = 7
    public = 8
    other = 9
    
class UserInfo:
    
    userDataFile = str('user_data.txt')
    
    def __init__(self):
        self.countryList = ['Afghanistan', 'Aland_Islands', 'Albania', 'Algeria', 'American_Samoa', 
                            'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua_and_Barbuda', 
                            'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 
                            'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 
                            'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia_and_Herzegovina', 
                            'Botswana', 'Bouvet_Island', 'Brazil', 'British_Indian_Ocean_Territory', 
                            'Brunei_Darussalam', 'Bulgaria', 'Burkina_Faso', 'Burundi', 'Cambodia', 
                            'Cameroon', 'Canada', 'Cape_Verde', 'Cayman_Islands', 
                            'Central_African_Republic', 'Chad', 'Chile', 'China', 'Christmas_Island', 
                            'Cocos_(Keeling)_Islands', 'Colombia', 'Comoros', 'Congo', 
                            'Congo,_The_Democratic_Republic_of_The', 'Cook_Islands', 'Costa_Rica', 
                            "Cote_D'ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech_Republic', 'Denmark', 
                            'Djibouti', 'Dominica', 'Dominican_Republic', 'Ecuador', 'Egypt', 
                            'El_Salvador', 'Equatorial_Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 
                            'Falkland_Islands_(Malvinas)', 'Faroe_Islands', 'Fiji', 'Finland', 'France', 
                            'French_Guiana', 'French_Polynesia', 'French_Southern_Territories', 'Gabon', 
                            'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 
                            'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 
                            'Guinea-bissau', 'Guyana', 'Haiti', 'Heard_Island_and_Mcdonald_Islands', 
                            'Holy_See_(Vatican_City_State)', 'Honduras', 'Hong_Kong', 'Hungary', 'Iceland', 
                            'India', 'Indonesia', 'Iran,_Islamic_Republic_of', 'Iraq', 'Ireland', 
                            'Isle_of_Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 
                            'Kazakhstan', 'Kenya', 'Kiribati', "Korea,_Democratic_People's_Republic_of",
                             'Korea,_Republic_of', 'Kuwait', 'Kyrgyzstan', 
                             "Lao_People's_Democratic_Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia',
                             'Libyan_Arab_Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao',
                             'Macedonia,_The_Former_Yugoslav_Republic_of', 'Madagascar', 'Malawi', 
                             'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall_Islands', 'Martinique', 
                             'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 
                             'Micronesia,_Federated_States_of', 'Moldova,_Republic_of', 'Monaco', 
                             'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 
                             'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands_Antilles', 
                             'New_Caledonia', 'New_Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 
                             'Norfolk_Island', 'Northern_Mariana_Islands', 'Norway', 'Oman', 'Pakistan', 
                             'Palau', 'Palestinian_Territory,_Occupied', 'Panama', 'Papua_New_Guinea', 
                             'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 
                             'Puerto_Rico', 'Qatar', 'Reunion', 'Romania', 'Russian_Federation', 'Rwanda', 
                             'Saint_Helena', 'Saint_Kitts_and_Nevis', 'Saint_Lucia', 
                             'Saint_Pierre_and_Miquelon', 'Saint_Vincent_and_The_Grenadines', 'Samoa', 
                             'San_Marino', 'Sao_Tome_and_Principe', 'Saudi_Arabia', 'Senegal', 'Serbia', 
                             'Seychelles', 'Sierra_Leone', 'Singapore', 'Slovakia', 'Slovenia', 
                             'Solomon_Islands', 'Somalia', 'South_Africa', 
                             'South_Georgia_and_The_South_Sandwich_Islands', 'Spain', 'Sri_Lanka', 
                             'Sudan', 'Suriname', 'Svalbard_and_Jan_Mayen', 'Swaziland', 'Sweden', 
                             'Switzerland', 'Syrian_Arab_Republic', 'Taiwan,_Province_of_China', 
                             'Tajikistan', 'Tanzania,_United_Republic_of', 'Thailand', 'Timor-leste', 
                             'Togo', 'Tokelau', 'Tonga', 'Trinidad_and_Tobago', 'Tunisia', 'Turkey', 
                             'Turkmenistan', 'Turks_and_Caicos_Islands', 'Tuvalu', 'Uganda', 'Ukraine', 
                             'United_Arab_Emirates', 'United_Kingdom', 'United_States', 
                             'United_States_Minor_Outlying_Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu',
                              'Venezuela', 'Viet_Nam', 'Virgin_Islands,_British', 'Virgin_Islands,_U.S.',
                               'Wallis_and_Futuna', 'Western_Sahara', 'Yemen', 'Zambia', 'Zimbabwe','Other']

        self.ispList = ['PLDT','StarHub','MTN_Network_Solutions',
                        'WorldCall','Unitel','UPC_Polska','BT',
                        'TeliaSonera','Comcast','Nifty','France_Telecom/Orange',
                        'Telekom_Srbija','Vodafone','EnterNet','LINKdotNET',
                        'Hong_Kong_Broadband_Network_Limited','Ethio_Telecom','SingTel','Telecom_Austria',
                        'Link3','Tangerine','Bayantel','H@inet',
                        'Angola_Telecom','Telekom_Malaysia','Vivacom','Afribone',
                        'Hathway','Yahoo_Japan','TE_Data','TVCable',
                        'Cats-net','AYA','Libero','MTNL',
                        'AsiaInfo','Lanka_Bell','BTCL','PCCW-HKT_Telephone_Limited',
                        'Volia','Telkom_Internet','EUNet','VIPNET',
                        'Web_Africa','Globe','Copaco','SFR',
                        'VNPT','Digicel','Angkornet','MEO',
                        'Sunrise','Zuku','Planet_Online','Arnet',
                        'Uzbektelecom','Sharq','Netia','Ringo',
                        'Ukrtelecom','M1','Fullrate','Orange',
                        'GVT_(Power)','SBB','Telecom_Italia','Etisalat',
                        'Pakistan_Telecommunication_Company_Limited','Togotelecom','FGC','China_Unicom',
                        'Cotas','Kyrgyz_Telecom','SLT','Simply_WIreless',
                        'China_Telecom','Entel','MWEB','Verizon',
                        'True','Nepal_Telecom_Company','Fastweb','Comteco',
                        'TalkTalk','Menara','Sonatel','InTech_Online',
                        'UPC','Maxis_Communications','3BB','Go',
                        'EZECOM','Beeline','Beltelecom','Movistar',
                        'Ziggo','Topnet','kbro','KPN',
                        'LG_Uplus','Forthnet','Camtel','Tele2Austria',
                        'Bharti','Orange_Mali','Taiwan_Broadband_Communications','Telmex/Claro',
                        'T-Com','Sahal_Telecom','Telekom_Slovenije','Tedata',
                        'ER-Telecom','NOS','SK_broadband','Slovak_Telecom-_T-COM',
                        'Axxess_DSL','Com_Hem','ISP','Three',
                        'Superonline','ipNX','UNE-EPM','iiNet',
                        'East_Telecom','Tiscali','NET','Internode',
                        'Telus_Communications','ShaTel','Netone','Kabel_Deutschland',
                        'Bell_Canada','Eastera','Tele2','First_Media',
                        'Hexabyte','Cote_d\'Ivoire_Telecom','Umniah/Batelco_Jordan','Special_Communication_Organisation',
                        'Telmex','TelOne','CobraNet','Zamtel',
                        'UPC_Austria','Time_Warner','Claro','Telenet',
                        'TTCL','VTR','Sonera','Dialog',
                        'Time','Tricom','O2_(Alice)','Oi_(Velox)',
                        'Kanakoo','Telefonica_Brasil_(Speedy)','Rogers_Communications','Insta_Telecom',
                        'Inter','Belgacom','Optus','TTNet',
                        'Izzi','TeleYemen','TDC','Tellas_(Wind)',
                        'Rostelecom','Cablecom','Romtelecom','012_Smile',
                        'Sudanet','WorldLink','Saima_Telecom','You_see',
                        'Jupiter_Telecommunications','Swisscom','Elisa','Telefonica_O2',
                        'Gnet','Cotel','Chunghwa_Telecom','TOT',
                        'Indosat_Mega_Media','Orange_Internet','Hot','Telstra_BigPond',
                        'Hormuud','Viettel','Babilon-T','Deutsche_Telecom',
                        'Datak_Telecom','Blizoo','ONO','IntraNS',
                        'UPC_Slovakia','Megacable','Virgin_Media','AT&T',
                        'NatCom','IBW','Telefonica_(Movistar)','Netnam',
                        'CNT','Syrian_Computer_Society_(SCS)','STC','Shaw_Communications',
                        'Djaweb','Telefonica_de_Argentina_(Speedy)','Libya_Telecom_&_Technology_(LTT)','T2',
                        'Spectranet','MPT_{Myanmar]','KT_Olleh','Tigo',
                        'AsahiNet','Telia-Stofa','Sonitel','Bezeq',
                        'FiberTel','Rio_Media','Telenor_Denmark','ZOL',
                        'Ecuadortelecom_(Claro)','Claro_(El_Salvador)','OTE','Isocel',
                        'Blueline','Claro_Chile','Uganda_Telecom','Empresa_de_Telecomunicaciones_de_Bogota_(ETB)',
                        'Onatel','Other']
        self.init()
        
    def init(self):
        self.country = ""
        self.state = ""
        self.city = ""
        self.isp = ""
        self.connType = ConnType.other
        self.dwn_bw = -1
        self.up_bw = -1
        self.price = -1
        
    def complete_country(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s 
                                for s in self.countryList
                                if s and s.startswith(text.title())]
            else:
                self.matches = self.countryList[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response
    
    def complete_isp(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s 
                                for s in self.ispList
                                if s and s.startswith(text)]
            else:
                self.matches = self.ispList[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response
    
    def null_complete(self, text, state):
        return None
        
    def connection_is_paid_type(self, conType):
        return conType != ConnType.company_nw and conType != ConnType.public
    
    def getCountry(self):
        # use readline library in a hackish manner for providing a list of countries
        readline.set_completer(UserInfo().complete_country)
        readline.parse_and_bind('tab: complete')
                       
        while self.country == "":         
            self.country = input("""(Use TAB to get suggestions and ENTER to select, type \'Other\' if you cannot find your country)
Enter the country you live in: """)
        
        # afterwards turn off auto-completion
        readline.set_completer(UserInfo().null_complete)
        readline.parse_and_bind('tab: complete')
        
        if self.country == "Other":
          self.country = input('Enter your country: ')

    def getIsp(self):
        # use readline library in a hackish manner for providing a list of countries
        readline.set_completer(UserInfo().complete_isp)
        readline.parse_and_bind('tab: complete')
                       
        while self.isp == "":         
            self.isp = input("""(Use TAB to get suggestions and ENTER to select, type \'Other\' if you cannot find your ISP)
Select your ISP (Internet Service Provider): """)
        
        # afterwards turn off auto-completion
        readline.set_completer(UserInfo().null_complete)
        readline.parse_and_bind('tab: complete')
        
        if self.isp == "Other":
            self.isp = input('Enter your ISP: ')	  
    
    def country_has_states(self,country):
        if country.find("United_States") != -1:
            return True
        elif country.find("Canada") != -1:
            return True
        elif country.find("India") != -1:
            return True
        elif country.find("Germany") != -1:
            return True
        elif country.find("Australia") != -1:
            return True
        else:
            return False
        
    def IsValidUserInfo(self):
        
        if self.country == "":
            return False
        if self.country_has_states(self.country) and self.state == "":
            return False
        if self.city == "":
            return False
        if self.connection_is_paid_type(self.connType):
          if self.price == -1 :
            return False
          elif self.dwn_bw == -1:
            return False
          elif self.up_bw == -1:
            return False
          elif self.isp == "":
            return False
        
        return True
        
    def getConnectionType(self):
        
        connTypeChosen = False
        
        while connTypeChosen == False:
            print ('\t\t0 - Dial-up')
            print ('\t\t1 - Cable')
            print ('\t\t2 - DSL/ADSL - ISDN')
            print ('\t\t3 - Fiber-to-the-home')
            print ('\t\t4 - Wireless Broadband')
            print ('\t\t5 - Mobile/cellular network')
            print('\t\t6 - Satellite')
            print ('\t\t7 - University/Company network')
            print ('\t\t8 - Public WiFi')
            print ('\t\t9 - Other')
            
            connType = input('Select connection type. Enter a number corresponding to one of the above choices: ')
            if connType.isdigit() and int(connType) >= 0 and int(connType) <= 9:
                self.connType = ConnType(int(connType))
                connTypeChosen = True
    
    def getUserInfo(self):   

        self.getCountry()
        
        if self.country_has_states(self.country):
            while self.state == "":
                self.state = input('Enter the state you live in: ')
                if "".join(self.state.split()).isalpha() == False:
                    self.state = ""
                    
        while self.city == "":
            self.city = input('Enter the city you live in: ')
            if "".join(self.city.split()).isalpha() == False:
                self.city = ""
        
        self.getConnectionType()                
               
        if self.connection_is_paid_type(self.connType): 
  
          self.getIsp()
          
          while self.dwn_bw == -1 or self.dwn_bw.isnumeric() == False:
            self.dwn_bw = input('Enter your download bandwidth in Mbps: ')
          self.dwn_bw = int(self.dwn_bw)
          
          while self.up_bw == -1 or self.up_bw.isnumeric() == False:
            self.up_bw = input('Enter your upload bandwidth in Mbps: ')
          self.up_bw = int(self.up_bw) 
            
          while self.price == -1 or self.price.isnumeric() == False:
            self.price = input('Enter your monthly internet price (in local currency): ')
          self.price = int(self.price) 
                    
    def getUserInfoFromFile(self):
        
        infile = open(UserInfo.userDataFile, "r")
        
        # read everything optimistically, check at the end 
        
        # get country
        line = infile.readline()
        if len(line) > 1 and line.find("Country") != -1:
            tokens = line.split()
            if len(tokens) == 2:
                self.country = tokens[1].strip()
            
        # get state
        line = infile.readline()
        if len(line) > 1 and line.find("State") != -1:
            tokens = line.split()
            if len(tokens) == 2:
                self.state = tokens[1].strip()
            
        # get city
        line = infile.readline()
        if len(line) > 1 and line.find("City") != -1:
            tokens = line.split()
            if len(tokens) == 2:
                self.city = tokens[1].strip()
            
        # get connection type
        line = infile.readline()
        if len(line) > 1 and line.find("Connection") != -1:
            tokens = line.split()
            if len(tokens) == 2 and tokens[1].strip().isnumeric():
                self.connType = ConnType(int(tokens[1].strip()))
                
        # get isp
        line = infile.readline()
        if len(line) > 1 and line.find("ISP") != -1:
          tokens = line.split()
          if len(tokens) == 2:
            self.isp = tokens[1].strip()
                    
        # get download speed
        line = infile.readline()
        if len(line) > 1 and line.find("Download") != -1:
            tokens = line.split()
            if len(tokens) == 2 and tokens[1].strip().isnumeric():
                self.dwn_bw = int(tokens[1].strip())
                
        # get upload speed
        line = infile.readline()
        if len(line) > 1 and line.find("Upload") != -1:
            tokens = line.split()
            if len(tokens) == 2 and tokens[1].strip().isnumeric():
                self.up_bw = int(tokens[1].strip())
                
        # get price information
        line = infile.readline()
        if len(line) > 1 and line.find("Price") != -1:
            tokens = line.split()
            if len(tokens) == 2 and tokens[1].strip().isnumeric():
                self.price = int(tokens[1].strip())
                
        infile.close()
       
        return self.IsValidUserInfo()

    
    def verifyUserInfo(self):
        self.printToConsole()
        response = input("\nIs the information above correct? Type Yes or No\n")
        if response.lower().find("yes") == -1:
            self.init() # re-initialize
            self.getUserInfo()
        else:
            self.printToFile() #re-writing to be safe
    
    def printToConsole(self): 
                
        print("\n\nCountry : " + self.country)
        print("State : " + self.state)
        print("City : " + self.city)
        print("Connection : " + self.connType.name)
        print("ISP : " + self.isp)
        print("Download speed : " + str(self.dwn_bw) + " Mbps")
        print("Upload speed : " + str(self.up_bw) + " Mbps")
        print("Internet service price : " + str(self.price))

    def printToFile(self):
        try:
            outfile = open(UserInfo.userDataFile,'w')
            outfile.write("Country " + self.country.replace(' ','_') + "\n")
            outfile.write("State " + self.state.replace(' ','_') + "\n")
            outfile.write("City " + self.city.replace(' ', '_') + "\n")
            outfile.write("Connection "  + str(self.connType.value) + "\n")
            outfile.write("ISP " + self.isp.replace(' ','_') + "\n")
            outfile.write("Download " + str(self.dwn_bw) + "\n")
            outfile.write("Upload " + str(self.up_bw) + "\n")
            outfile.write("Price " + str(self.price) + "\n")
            outfile.close()

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))     
            
           
        
def main():
    userInfo = UserInfo()
    if os.path.exists(UserInfo.userDataFile) and userInfo.getUserInfoFromFile():
        userInfo.verifyUserInfo()
    else:
        userInfo.init()
        userInfo.getUserInfo()
    
    userInfo.printToFile()
    
if __name__ == '__main__':
    main()    

