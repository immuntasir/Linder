from flaskext.mysql import MySQL
from flask import Flask, render_template, json, request,redirect,session,jsonify
from werkzeug import generate_password_hash, check_password_hash
import abc, six



#@linderApp.route('/favicon.ico')
#def favicon():
    #return send_from_directory(os.path.join(app.root_path, 'static'),
     #                          'favicon.ico', mimetype='image/vnd.microsoft.icon')

###########################################
### App Initialization
###########################################
linderApp = Flask(__name__)
linderApp.secret_key = 'why would I tell you my secret key?'

class Linder:
    def __init__(self):
        pass
###########################################
### The Single Database
###########################################
class SingleDatabase:
    class __SingleDatabase:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    __mysql = None
    __cursor = None
    __con = None
    def __init__(self, app):
        if not SingleDatabase.__mysql:
            # MySQL configurations
            self.__mysql = MySQL()
            app.config['MYSQL_DATABASE_USER'] = 'root'
            app.config['MYSQL_DATABASE_PASSWORD'] = '1234qwer'
            app.config['MYSQL_DATABASE_DB'] = 'Linder'
            app.config['MYSQL_DATABASE_HOST'] = 'localhost'
            self.__mysql.init_app(app)
    
        else:
            pass
    def getDatabase(self):
        return self
    def connect(self):
        return self.__mysql.connect()
    def getCursor(self):
        print("in the method")
        self.__con = self.__mysql.connect()
        self.__cursor = self.__con.cursor()
        print("Got the cursor here in the method")
        return self.__cursor
    def getCon(self):
        self.__con = self.__mysql.connect()
        return self.__con
    def closeCursor(self):
        self.__cursor.close()
    def closeCon(self):
        self.__cursor.close()
    def commit(self):
        self.__con.commit()
###########################################
singleDatabase = SingleDatabase(linderApp).getDatabase()

@linderApp.route('/')
def main():
    
    return render_template('index.html')
###########################################



##########################
###This section will implement the abstract factory pattern. 
###There will be two factories, which will create users 
###and devices respectively.
#########################

@six.add_metaclass(abc.ABCMeta)
class AbstractFactory:
    """
    Declare an interface for operations that create abstract product
    objects.
    """

    @abc.abstractmethod
    def create_product_a(self):
        pass

    @abc.abstractmethod
    def create_product_b(self):
        pass

        
################################################
## The following methods will create buyer and 
## seller, using the factory pattern.
##
################################################        

#Concrete Factory #1 - This will create new users
class UserFactory(AbstractFactory):
    """
    Implement the operations to create concrete product objects.
    """

    def create_product_a(self):
        return BuyerProduct()

    def create_product_b(self):
        return SellerProduct()
        
#Concrete Factory #2 - This will create new devices
class DeviceFactory(AbstractFactory):
    """
    Implement the operations to create concrete product objects.
    """

    def create_product_a(self):
        return LaptopProduct()

    def create_product_b(self):
        return MobileProduct()



@six.add_metaclass(abc.ABCMeta)
class AbstractProductA:
    """
    Declare an interface for a type of product object.
    """

    @abc.abstractmethod
    def createProduct(self, list):
        pass
    def addToDB(self, cursor):
        pass

# User
class BuyerProduct(AbstractProductA):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """

    def createProduct(self, list):
        print(list)
        self._name = str(list[0])
        self._username = str(list[1])
        self._email = str(list[2])
        self._mobile = str(list[3])
        self._usertype = 0
        self._password = str(list[4])
        self._latitude = float(list[5])
        self._longitude = float(list[6])
        
    def addToDB(self, cursor):
        cursor.callproc('sp_createUser',(self._name,  self._username, self._email, self._mobile, self._usertype, self._password, 
                                            self._latitude, self._longitude))
        return cursor.fetchall()

class LaptopProduct(AbstractProductA):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """

    def createProduct(self, list):
        self._model = list['inputModel']
        self._owner = session.get('user')            
        self._processor = list['inputProcessor']
        self._ram = list['inputRAM']
        self._storage = list['inputStorage']
        self._price = list['inputPrice']
        self._additional = list['inputAdditional']
        
    def addToDB(self, cursor):
        cursor.callproc('sp_createLaptop',(self._owner,  self._model, self._processor, self._ram, self._storage, self._price, 
                                            self._additional))
        return cursor.fetchall()

@six.add_metaclass(abc.ABCMeta)
class AbstractProductB():
    """
    Declare an interface for a type of product object.
    """

    @abc.abstractmethod
    def createProduct(self, list):
        pass
    def addToDB(self, cursor):
        pass

class SellerProduct(AbstractProductB):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """
    def createProduct(self, list):
        self._name = str(list[0])
        self._username = str(list[1])
        self._email = str(list[2])
        self._mobile = str(list[3])
        self._usertype = 1
        self._password = str(list[4])
        self._latitude = float(list[5])
        self._longitude = float(list[6])
        
    def addToDB(self, cursor):
        cursor.callproc('sp_createUser',(self._name,  self._username, self._email, self._mobile, self._usertype, self._password, 
                                            self._latitude, self._longitude))
        return cursor.fetchall()


class MobileProduct(AbstractProductB):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """

    def createProduct(self, list):
        self._model = list['inputModel']
        self._owner = session.get('user')            
        self._processor = list['inputProcessor']
        self._ram = list['inputRAM']
        self._storage = list['inputStorage']
        self._camera = list['inputCamera']
        self._price = list['inputPrice']
        self._additional = list['inputAdditional']
    def addToDB(self, cursor):
        cursor.callproc('sp_createMobile',(self._owner,  self._model, self._processor, self._ram, self._storage, self._camera, self._price, 
                                            self._additional))
        return cursor.fetchall()
     
        

        
@linderApp.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _mobile = request.form['inputMobile']
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']
        _usertype = request.form['inputUserType']
        _latitude = request.form['lat']
        _longitude = request.form['lng']
        print("here")
        if _name and _email and _password and _username and _usertype:
            userFactory = UserFactory()    
            # All Good, let's call MySQL
            print("andHere")
            cursor = singleDatabase.getCursor()
            print(cursor)
            #_hashed_password = generate_password_hash(_password)
            _hashed_password = _password
            print(_usertype)
            if _usertype == "seller":
                print("here")
                newUserCreator = userFactory.create_product_b()
            else:
                print("hereasfais")
                newUserCreator = userFactory.create_product_a()
                print("still good")
            print("creating")    
            newUserCreator.createProduct([_name,_username,_email, _mobile, _hashed_password, _latitude, _longitude])
            print("adding")
            print(cursor)
            data = newUserCreator.addToDB(cursor)
            
            print(len(data))
            if len(data) is 0:
                singleDatabase.commit()
                #json.dumps({'message':'User created successfully !'})
                return redirect('/showSignIn')
            else:
                return render_template('signup.html',param = 'Wrong Input!')
                #return json.dumps({'error':str(data[0])})
            singleDatabase.closeCursor()
            singleDatabase.closeCon()
        else:
            return render_template('signup.html',param = 'Enter the required fields!')
            #return json.dumps({'error':'Enter the required fields'})

    except Exception as e:
        print("shes")
        return render_template('signup.html',param = 'Error')
        #return json.dumps({'error':str(e)})



################################################
## The following methods will add new laptop or 
## mobile, using the factory pattern.
##
################################################        





################################
### The following section will
### add a laptop to the database
###
################################
@linderApp.route('/addDevice',methods=['POST'])
def addDevice():
    try:
        print("here")
        if session.get('user'):
            list = request.form
            cursor = singleDatabase.getCursor()
            
            deviceFactory = DeviceFactory()    
            print('lets trye')
            print(list)
            print(list['devicetype'])
            if list['devicetype'] == "laptop":
                print('here for the laptops')
                newDevice = deviceFactory.create_product_a()
            else:
                print('here for the mobiles')
                newDevice = deviceFactory.create_product_b()
            print("done")
            newDevice.createProduct(list)
            data = newDevice.addToDB(cursor)
            if len(data) is 0:
                singleDatabase.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        singleDatabase.closeCursor()
        singleDatabase.closeCon()





#######
#This section will implement the search interface.
#This will use the strategy pattern
#######

class SearchStrategy:
    def Search(self, list):
        pass

class LaptopSearch(SearchStrategy):
    def Search(self, list):
        cursor = singleDatabase.getCursor()
        cursor.callproc('sp_getLaptopBySpecs', (list[0], list[1], list[2], list[3], list[4]))
        print("here...")
        laptops = cursor.fetchall()
        print("so...")
        laptops_dict = []
        for laptop in laptops:
            print("looping")
            
            laptop_dict = {
                    'Id': laptop[0],
                    'Owner' : laptop[1],
                    'Model' : laptop[2],
                    'Processor' : laptop[3],
                    'RAM' : laptop[4],
                    'Storage' : laptop[5],
                    'Condition' : laptop[6],
                    'Price' : laptop[7],
                    'Additional' : laptop[8],
            }
            
            laptops_dict.append(laptop_dict)
        print("here...")
        print("Number of laptops: " + str(len(laptops_dict)))
        
        return laptops_dict

class MobileSearch(SearchStrategy):
    def Search(self, list):
        cursor = singleDatabase.getCursor()
        cursor.callproc('sp_getMobileBySpecs', (list[0], list[1], list[2], list[5], list[3], list[4]))
        mobiles = cursor.fetchall()
        mobiles_dict = []
        for mobile in mobiles:
            print("looping")
            mobile_dict = {
                    'Id': mobile[0],
                    'Owner' : mobile[1],
                    'Model' : mobile[2],
                    'Processor' : mobile[3],
                    'RAM' : mobile[4],
                    'Storage' : mobile[5],
                    'Camera' : mobile[6],
                    'Price' : mobile[7],
                    'Additional' : mobile[8]
            }
            
            mobiles_dict.append(mobile_dict)
        print("here...")
        print("Number of mobiles: " + str(len(mobiles_dict)))
        
        return mobiles_dict

#if __name__ == "__main__":
 #   strat0 = deviceFinderStrategy()
  #  strat1 = deviceFinderStrategy(executeReplacement1)
   # strat2 = deviceFinderStrategy(executeReplacement2)

 #   strat0.executeSearch()
  #  strat1.executeSearch()
   # strat2.executeSearch()


##############################################
@linderApp.route('/showAddDevice')
def showAddDevice():
    return render_template('addDevice.html')


##############################################
@linderApp.route('/showDeviceSearch')
def showDeviceSearch():
    return render_template('deviceSearch.html')



@six.add_metaclass(abc.ABCMeta)
class Component():
    """
    Define the interface for objects that can have responsibilities
    added to them dynamically.
    """

    @abc.abstractmethod
    def search(self):
        pass


@six.add_metaclass(abc.ABCMeta)
class Decorator(Component):
    """
    Maintain a reference to a Component object and define an interface
    that conforms to Component's interface.
    """

    def __init__(self, component):
        self._component = component

    @abc.abstractmethod
    def search(self):
        pass


class DistanceDecorator(Decorator):
    """
    Add responsibilities to the component.
    """

    def search(self, listOfSpecs):
        devices_dict = self._component.search(listOfSpecs)
        cursor = singleDatabase.getCursor()
        print("HERE")
        for device in devices_dict:
            _user = session.get('user')
            cursor.callproc('sp_getLatLng', (_user, ) )
            my_distance = cursor.fetchall()
            cursor.callproc('sp_getLatLng', (device['Owner'], ) )
            distance = cursor.fetchall()
            print("Loc : " )
            print(distance[0][0])
            print(distance[0][1])
           
            device['Distance'] = (str(vincenty(my_distance, distance).kilometers) + "kilometers")  
            geolocator = Nominatim()
            
            location = geolocator.reverse(distance[0])
            print(location.address)
 
        singleDatabase.closeCursor()
        singleDatabase.closeCon()
        return devices_dict


class MainSearch(Component):
    """
    Define an object to which additional responsibilities can be
    attached.
    """

    def search(self, listOfSpecs):
        _model = listOfSpecs['inputModel']
        _processor = listOfSpecs['inputProcessor']
        _ram = listOfSpecs['inputRAM']
        _storage = listOfSpecs['inputStorage']
        _price = listOfSpecs['inputPrice']
        _type = listOfSpecs['devicetype']
        speclist = [_model, _processor, _ram, _storage, _price]
        
        if type == 'mobile' :
            _camera = request.form['inputCamera']
            speclist.append(_camera)
            searcher = MobileSearch()
        else :
            searcher = LaptopSearch() 
        
        devices_dict = searcher.Search(speclist)
        return devices_dict

@linderApp.route('/deviceSearcher',methods=['POST'])
def deviceSearcher():
    try:
        listOfSpecs = request.form
        
        
        mainSearch = MainSearch()
        distanceDecorator = DistanceDecorator(mainSearch)
        devices_dict = distanceDecorator.search(listOfSpecs)
        
        return render_template('searchResults.html', laptop_dict = devices_dict, type = listOfSpecs['devicetype'])
            
        
        
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        singleDatabase.closeCursor()



################################################
### This method will fetch all the laptops
### Posted by the current user
@linderApp.route('/getLaptopByUser')
def getLaptop():
    try:
        if session.get('user'):
            _user = session.get('user')
            print("Fetching...")
            
            cursor = singleDatabase.getCursor()
            print("user = " + str(_user))
            cursor.callproc('sp_getDeviceByUser',(_user,))
            print("here...")
            laptops = cursor.fetchall()
            print("so...")
            laptops_dict = []
            for laptop in laptops:
                print("looping")
                laptop_dict = {
                        'Id': laptop[0],
                        'Owner' : laptop[1],
                        'Model' : laptop[2],
                     'Processor' : laptop[3],
                        'RAM' : laptop[4],
                        'Storage' : laptop[5],
                        'Condition' : laptop[6],
                        'Price' : laptop[7],
                        'Additional' : laptop[8]
                }
                
                laptops_dict.append(laptop_dict)
            print("here...")
            #print("Number of laptops: " + str(laptops_dict.size()))
            return json.dumps(laptops_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        singleDatabase.closeCursor()

################################################



#####################################################




#####################################################

#####################################################

@linderApp.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
@linderApp.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@linderApp.route('/userHome')
def userHome():
    try:
        if session.get('user'):
            _user = session.get('user')
            print("Fetching...")
            cursor = singleDatabase.getCursor()
            print("user = " + str(_user))
            cursor.callproc('sp_getDeviceByUser',(_user,))
            print("here...")
            laptops = cursor.fetchall()
            print("so...")
            laptops_dict = []
            for laptop in laptops:
                print("looping")
                laptop_dict = {
                        'Id': laptop[0],
                        'Owner' : laptop[1],
                        'Model' : laptop[2],
                        'Processor' : laptop[3],
                        'RAM' : laptop[4],
                        'Storage' : laptop[5],
                        'Condition' : laptop[6],
                        'Price' : laptop[7],
                        'Additional' : laptop[8],
                        'Type' : laptop[9]
                }
                
                laptops_dict.append(laptop_dict)
            print("here...")
            #print("Number of laptops: " + str(laptops_dict.size()))
            return render_template('userHome.html', listOfDevices = laptops_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        singleDatabase.closeCursor()
    

@linderApp.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')
@linderApp.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        
         # connect to mysql
        cursor = singleDatabase.getCursor()
        print(cursor)
        cursor.callproc('sp_validateLogin',(_username, _password))
        data = cursor.fetchall()
        if len(data) > 0:
            session['user'] = data[0][0]
            return redirect('/userHome')
        else:
            return render_template('error.html',error = 'HAHAHAHAHA.')
                

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        singleDatabase.closeCursor()
        singleDatabase.closeCon()


#############################################################################

#### The following section uses the strategy pattern
#### to recommend laptops and mobiles

#############################################################################

@six.add_metaclass(abc.ABCMeta)
class ListRecommendations:    
    def getRecommendations(self): 
        pass

class ListMobileRecommendations(ListRecommendations):
    def getRecommendations(self):
        try:
            if session.get('user'):
                _user = session.get('user')
                print("Fetching...")
                cursor=singleDatabase.getCursor()
                print("Grabbed cursor")
                cursor.callproc('sp_getMobileRecommendation', (_user,))
                print("Got recommendations")
                devices = cursor.fetchall()
            else:
                devices=list()
        except Exception as e:
            print("Exception Occurred")                
            devices=list()

        finally:
            singleDatabase.closeCursor()
            singleDatabase.closeCon()
            return devices

    
class ListLaptopRecommendations(ListRecommendations):
    def getRecommendations(self):
        try:
            if session.get('user'):
                _user = session.get('user')
                print("Fetching...")
                cursor=singleDatabase.getCursor()
                print("Grabbed cursor")
                cursor.callproc('sp_getLaptopRecommendation', (_user,))
                devices = cursor.fetchall()
                print("Got Recommendations")
            else:
                devices=list()
        except Exception as e:
            print("Exception Occurred")                
            devices=list()

        finally:
            singleDatabase.closeCursor()
            singleDatabase.closeCon()
            return devices

@linderApp.route('/recommendedlaptops')
def recommendedLaptops():
    try:
        recommender=ListLaptopRecommendations()                
        laptops = recommender.getRecommendations()
        print("so...")
        laptops_dict = []
        for laptop in laptops:
            print("looping")
            laptop_dict = {
            'Id': laptop[0],
            'Owner' : laptop[1],
            'Model' : laptop[2],
            'Processor' : laptop[3],
            'RAM' : laptop[4],
            'Storage' : laptop[5],
            'Condition' : laptop[6],
            'Price' : laptop[7],
            'Additional' : laptop[8]
            }
            laptops_dict.append(laptop_dict)
        print("here...")
        print("Number of laptops: " + str(len(laptops_dict)))
        return render_template('laptoprecommendationResults.html', laptop_dict = laptops_dict)    
    except Exception as e:
        return render_template('error.html', error = str(e))
    

@linderApp.route('/recommendedmobiles')
def recommendedmobiles():
        try:
            print("Came here.")        
            recommender=ListMobileRecommendations()                
            print("Came here..")        
            mobiles = recommender.getRecommendations()
            print("Came here...")
            mobiles_dict = []          
            for mobile in mobiles:
                print("looping")
                mobile_dict = {
                'Id': mobile[0],
                'Owner' : mobile[1],
                'Model' : mobile[2],
                'Processor' : mobile[3],
                'RAM' : mobile[4],
                'Storage' : mobile[5],
                'Camera' : mobile[6],
                'Price' : mobile[7],
                'Additional' : mobile[8]
                }
            mobiles_dict.append(mobile_dict)
          
            print("here...")
            print("Number of mobiles: " + str(len(mobiles_dict)))
            return render_template('mobilerecommendationResults.html', mobile_dict = mobiles_dict)    
        except Exception as e:
            return render_template('error.html', error = str(e))


@linderApp.route('/subscribeToLaptop',methods=['POST','GET'])
def subscriptionLaptop():
    try:
        if session.get('user'):
            _user = session.get('user')
            type(_user)
            my_id = request.form['my_id']
            cursor=singleDatabase.getCursor()
            #print("USER= " + _user + " laptop id" + my_id)
            print ( int(_user))
            print ( int(my_id))
            cursor.callproc('sp_addLaptopSubscription', (int(_user), int(my_id)))                
            print("Subscription Added")
            return render_template("subscription.html", message = 'Subscribed successfully')
        else:
            print "No user"
    except:
        print("Exception Raised")    
        return render_template("error.html", error = 'You already subscibed here')
    finally:
        singleDatabase.commit()
        singleDatabase.closeCursor()
        singleDatabase.closeCon()
        
@linderApp.route('/subscribeToMobile',methods=['POST','GET'])
def subscriptionMobile():
    try:
        if session.get('user'):
            _user = session.get('user')
            type(_user)
            my_id = request.form['my_id']
            cursor=singleDatabase.getCursor()
            #print("USER= " + _user + " laptop id" + my_id)
            print ( int(_user))
            print ( int(my_id))
            cursor.callproc('sp_addMobileSubscription', (int(_user), int(my_id)))                
            print("Subscription Added")
            return render_template("subscription.html", message = 'Subscribed successfully')
        else:
            print "No user"
    except:
        print("Exception Raised")    
        return render_template("error.html", error = 'You already subscibed here')
    finally:
        singleDatabase.commit()
        singleDatabase.closeCursor()
        singleDatabase.closeCon()
        


def removeMobile(dev_id):
    cursor=singleDatabase.getCursor()
    
    cursor.callproc('sp_getSubscribedUsersMobile', (dev_id,))
    print "Ashche"
    emails=cursor.fetchall()
    for email in emails:
        print email
    cursor.callproc('sp_deleteMobileSubscription', (dev_id,))
    print "Deleted"
    cursor.callproc('sp_deleteMobile', (dev_id,))
    print "Deleted 2"
    singleDatabase.commit()
    singleDatabase.closeCursor()
    singleDatabase.closeCon()
    return redirect('/userHome')


def removeLaptop(dev_id):
    cursor=singleDatabase.getCursor()
    cursor.callproc('sp_getSubscribedUsersLaptop', (dev_id,))
    emails=cursor.fetchall()
    for email in emails:
        print str(email)
    cursor.callproc('sp_deleteLaptopSubscription', (dev_id,))
    cursor.callproc('sp_deleteLaptop', (dev_id,))
    singleDatabase.commit()
    singleDatabase.closeCursor()
    singleDatabase.closeCon()
    return redirect('/userHome')

@linderApp.route('/removeDevice', methods=['POST','GET'])
def removeDevice():
    _user = session.get('user')
    dev_type = request.form['dev_type']
    dev_id = request.form['dev_id']
    print int(dev_id)
    if int(dev_type)==0: 
        return removeMobile(int(dev_id))
    else: 
        return removeLaptop(int(dev_id))

if __name__ == "__main__":
    linderApp.run(host = '0.0.0.0', port=6969)

