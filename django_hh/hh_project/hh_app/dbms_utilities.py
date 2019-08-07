#!/usr/bin/env python
# coding: utf-8

# # The Happiest Hour
# - Madi Gwynn
# - Brian Smith-Eitches
# 
# ## Set Up

# In[168]:


import sqlite3
import json


# In[169]:


# Connect/Create(if does not exist) to a database formatted as a sqlite database 
db=sqlite3.connect("./happy_hour.db")


# In[170]:


cursor = db.cursor()


# ## Create Database Tables

# In[171]:


cursor.execute('''
    CREATE TABLE regions(
        rid INTEGER PRIMARY KEY,
        title TEXT)
''')
db.commit()


# In[172]:


cursor.execute('''
    CREATE TABLE users(
        uid INTEGER PRIMARY KEY,
        name TEXT,
        admin INTEGER)
''')
db.commit()


# In[173]:


cursor.execute('''
    CREATE TABLE bars(
        bid INTEGER PRIMARY KEY,
        name TEXT,
        region_id INTEGER,
        manager_id INTERGER,
        address TEXT,
        phone_number TEXT,
        approved INTEGER,
        FOREIGN KEY(region_id) REFERENCES regions(rid),
        FOREIGN KEY(manager_id) REFERENCES users(uid)
        )
''')
db.commit()


# In[174]:


cursor.execute('''
    CREATE TABLE bar_features(
        bfid INTEGER PRIMARY KEY,
        bar_id INTEGER,
        feature_id INTEGER,
        FOREIGN KEY(bar_id) REFERENCES bars(bid),
        FOREIGN KEY(feature_id) REFERENCES features(fid))''')
db.commit()


# In[175]:


cursor.execute('''
    CREATE TABLE features(
        fid INTEGER PRIMARY KEY,
        feature TEXT,
        description TEXT)
''')
db.commit()


# In[176]:


cursor.execute('''
    CREATE TABLE happy_hours(
        hhid INTEGER PRIMARY KEY, 
        day_of_week VARCHAR(2), 
        start_time TIME, 
        end_time TIME,
        bar_id INTEGER,
        drinks INTEGER,
        food INTEGER,
        menu_pdf TEXT,
        FOREIGN KEY(bar_id) REFERENCES bars(bid))
''')
db.commit()


# In[177]:


cursor.execute('''
    CREATE TABLE reviews(
        rid INTEGER PRIMARY KEY, 
        user_id INTEGER,
        bar_id INTEGER,
        star_count INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(uid), 
        FOREIGN KEY(bar_id) REFERENCES bars(bid))
''')
db.commit()


# # Functions for implementation

# # Create 
# - User (self) BRIAN
# - Regions (admin) BRIAN
# - Bars (managers, default to *unvetted*) MADI
# - Happy Hours (managers) MADI
# - Features (admin) BRIAN
# - Reviews (users) MADI 
# - BarFeatures (managers) BRIAN

# In[178]:


def create_user(name, admin=False):
    cursor.execute('''INSERT INTO users(name, admin)
                  VALUES(?,?)''', (name, admin))
    db.commit()


# In[179]:


def create_region(title):
    cursor.execute('''INSERT INTO regions(title) VALUES(:title)''',
                   {'title':title})
    
    db.commit()
    


# In[180]:


def create_feature(feature, description):
    cursor.execute('''INSERT INTO features(feature, description) 
                    VALUES(?,?)''', (feature, description))
    db.commit()
    
    


# In[181]:


def create_bar_feature(bar_id, feature_id):
    cursor.execute('''INSERT INTO bar_features(bar_id, feature_id)
                    VALUEs(?,?)''', (bar_id, feature_id))
    db.commit()


# In[182]:


#create_bar function 
def create_bar(name, region_id, manager_id, address, phone_number, approved=False):
    cursor.execute('''INSERT INTO bars(name, region_id, manager_id, address, phone_number, approved) 
                    VALUES(?,?,?,?,?,?)''', (name, region_id, manager_id, address, phone_number, approved))
    db.commit()
    


# In[183]:


#create_happy_hours function 
def create_happy_hour(day_of_week, start_time, end_time, bar_id, drinks, food, menu_pdf):
    cursor.execute('''INSERT INTO happy_hours(day_of_week, start_time, end_time, bar_id, drinks, food, menu_pdf) 
                    VALUES(?,?,?,?,?,?,?)''', (day_of_week, start_time, end_time, bar_id, drinks, food, menu_pdf))
    db.commit()
    


# In[184]:


def create_review(user_id, bar_id, star_count):
    cursor.execute('''INSERT INTO reviews(user_id, bar_id, star_count) 
                    VALUES(?,?,?)''', (user_id, bar_id, star_count))
    db.commit()    


# # Display (READ)
# - Only show bars & its HH's that have been approved BRIAN. Done.
# - Users Filter by bar attributes BRIAN Done.
#     - Review ratings
#     - Bar_features
#     - Regions
# - For **High Level = BAR** : Link up (JSON) bar name, happy hour days, drinks/food disc?, region, reviews MADI TODO
# - For **LOW LEVEL = HH**: include each happy hour separated by happy hour entry, pdf, bar info from above, phone, address BRIAN Done.

# In[185]:


# returns approved bars
def all_approved_bars():
    cursor.execute('''SELECT bid FROM bars 
                        WHERE approved = True''')
    approved_bars = cursor.fetchall()
    
    approved_ids = []
    for id in approved_bars:
        approved_ids.append(id[0])
    return approved_ids


# In[186]:


# returns approved happy hours
def all_approved_hhs():
    cursor.execute('''SELECT hhid FROM happy_hours JOIN bars on bar_id = bid WHERE approved = True''')
    approved_hhs = cursor.fetchall()
    
    approved_ids = []
    for id in approved_hhs:
        approved_ids.append(id[0])
    return approved_ids


# In[187]:


# filter bars by regions
def bars_in_regions(region_ids = None):
    if not region_ids:
        return all_approved_bars()
    
    bar_ids = []
    
    for region_id in region_ids:
        cursor.execute('''SELECT bid FROM bars WHERE region_id = (:region_id) AND approved = True''',
                  {'region_id':region_id})
        region_bars = cursor.fetchall()
        for id in region_bars:
            bar_ids.append(id[0])
            
    return bar_ids


# In[188]:


# filter bars by features
def bars_with_features(feature_ids = None):
    if not feature_ids:
        return all_approved_bars()
    
    bar_ids = []
    
    for feature_id in feature_ids:
        cursor.execute('''SELECT bid FROM bars JOIN bar_features on bid = bar_id WHERE
                        feature_id = (:feature_id) AND approved = True''',
                      {'feature_id':feature_id})
        feature_bars = cursor.fetchall()
        for id in feature_bars:
            bar_ids.append(id[0])
            
    return bar_ids


# In[189]:


# filter bars that meet minimum ratings
def bars_with_rating(min_rating = 0):
    if min_rating == 0:
        return all_approved_bars()
    
    cursor.execute('''SELECT bid FROM bars JOIN reviews on bid = bar_id WHERE approved = True
                    GROUP BY bid HAVING AVG(star_count) >= (:min_rating)''',
                    {'min_rating':min_rating})
    
    bar_ids = []
    rated_bars = cursor.fetchall()
    for id in rated_bars:
        bar_ids.append(id[0])

    return bar_ids


# In[190]:


#REGION IDS AND FEATURE IDS IS ALWAYS A LIST WHEN SOMETHING IS CHOSEN
# filter bars that meet all region, feature, and minimum rating requirements
def filter_bars(region_ids = None, feature_ids = None, min_rating = 0):
    
    filtered_bar_ids = list(set(bars_in_regions(region_ids)) & set(bars_with_features(feature_ids)) & set(bars_with_rating(min_rating))) 
    
    #create a list of bar dictionaries
    bars = [display_bar(bar_id) for bar_id in filtered_bar_ids]
    json_object = json.dumps({'bars':bars})
    
    return json_object    


# In[191]:


# output of this function is a dictionary - can later be converted to a json object 
def display_bar(bar_id):
    #create empty dictionary
    bar = {}
    
    #add bar name and region to dictionary
    cursor.execute('''SELECT name, title FROM bars JOIN regions ON region_id = rid
                        WHERE bid=(:bid) ''', {'bid':bar_id})
    bar_info = cursor.fetchone()
    bar['name'] = bar_info[0]
    bar['region'] = bar_info[1]
    
    #add happy hour days, if drinks and food are discounted to dictionary 
    cursor.execute('''SELECT day_of_week, drinks, food FROM happy_hours
                        WHERE bar_id=(:bar_id)''', {'bar_id':bar_id})
    hh_info = cursor.fetchall()
    hh_days = []
    drinks_check = "FALSE"
    food_check = "FALSE"
    
    for hh in hh_info:
        hh_days.append(hh[0])
        if hh[1] == 1:
            drinks_check = "TRUE"
        if hh[2] == 1:
            food_check = "TRUE"
    
    bar['days'] = hh_days
    bar['drinks'] = drinks_check
    bar['food'] = food_check
    
    #add reviews score to dictionary 
    cursor.execute('''SELECT AVG(star_count) FROM reviews 
                        WHERE bar_id=(:bar_id)''', {'bar_id':bar_id})
    star_counts = cursor.fetchone()
    bar['reviews'] = star_counts[0]

    #return dictionary 
    return bar


# In[192]:


# output of this function is a dictionary - can later be converted to a json object 
# calls the display_bar function 
def display_bar_hhs(bar_id):
    
    #create bar dictionary 
    bar = display_bar(bar_id)
    
    #create happy hour list
    hh = []
    
    cursor.execute('''SELECT hhid FROM happy_hours
                        WHERE bar_id=(:bar_id)''', {'bar_id':bar_id})
    hh_ids = cursor.fetchall()
    
    for hh_id in hh_ids:
        #create a happy hour info dictionary for each happy hour
        hh_dict = {}
        
        cursor.execute('''SELECT day_of_week, start_time, end_time, drinks, food, menu_pdf FROM happy_hours
                        WHERE hhid=(:hhid)''', {'hhid':hh_id[0]})
        
        hh_info = cursor.fetchone()
        
        hh_dict['day'] = hh_info[0]
        hh_dict['start'] = hh_info[1]
        hh_dict['end'] = hh_info[2]
        hh_dict['drinks_discount'] = hh_info[3]
        hh_dict['food_discount'] = hh_info[4]
        hh_dict['menu'] = hh_info[5]
        
        hh.append(hh_dict)
    
    bar['happy_hours'] = hh
    
    #return dictionary
    return bar


# # Edit (UPDATE) *Identical to Create*
# - User (self) BRIAN
# - Regions (admin) BRIAN
# - Bars (managers, admin) MADI
#     - Also admin approval
# - Happy Hours (managers) MADI
# - Features (admin) BRIAN
# - Reviews (users) MADI
# - BarFeatures (managers) BRIAN **Achieved via add feature and delete feature**

# In[193]:


def edit_user(uid, name, admin=False):
    cursor.execute('''UPDATE users SET name=(:name), admin=(:admin)
                  WHERE uid=(:uid)''', {'uid':uid,'name':name,'admin':admin})
    db.commit()


# In[194]:


def edit_region(rid, title):
    cursor.execute('''UPDATE regions SET title=(:title)
                  WHERE rid=(:rid)''', {'rid':rid,'title':title})
    db.commit()


# In[195]:


def edit_feature(fid, feature, description):
    cursor.execute('''UPDATE features SET feature=(:feature), description=(:description)
                  WHERE fid=(:fid)''', {'fid':fid,'feature':feature,'description':description})
    db.commit()


# In[196]:


def edit_bar(bid, name, region_id, manager_id, address, phone_number):
    cursor.execute('''UPDATE bars SET name=(:name), region_id=(:region_id), manager_id=(:manager_id), address=(:address), phone_number=(:phone_number)
                  WHERE bid=(:bid)''', {'bid':bid,'name':name,'region_id':region_id, 'manager_id':manager_id, 'address':address, 'phone_number':phone_number})
    db.commit()


# In[197]:


def approve_bar(bid, approved=True):
    cursor.execute('''UPDATE bars SET approved=(:approved)
                        WHERE bid=(:bid)''', {'bid':bid,'approved':approved})
    db.commit() 


# In[198]:


def edit_happy_hour(hhid, day_of_week, start_time, end_time, bar_id, drinks, food, menu_pdf):
    cursor.execute('''UPDATE happy_hours SET day_of_week=(:day_of_week), start_time=(:start_time), end_time=(:end_time), bar_id=(:bar_id), drinks=(:drinks), food=(:food), menu_pdf=(:menu_pdf)
                  WHERE hhid=(:hhid)''', {'hhid':hhid,'day_of_week':day_of_week,'start_time':start_time,'end_time':end_time,'bar_id':bar_id,'drinks':drinks,'food':food,'menu_pdf':menu_pdf})
    db.commit()


# In[199]:


def edit_review(rid, bar_id, star_count):
    cursor.execute('''UPDATE reviews SET bar_id=(:bar_id), star_count=(:star_count)
                        WHERE rid=(:rid)''', {'rid':rid,'bar_id':bar_id, 'star_count':star_count})
    db.commit() 


# # Delete
# - User (admin) BRIAN
# - Regions (admin) BRIAN
# - Bars (managers) MADI
#     - Call delete all happy hours
#     - Call delete on all bar features
# - Happy Hours (managers) MADI
# - Features (admin) BRIAN
#     - Remove all barfeatures with that feature
# - Reviews (users) MADI
# - BarFeatures (managers) BRIAN

# In[200]:


#only admins can call this in the interface
def delete_user(user_id):
    cursor.execute('''DELETE FROM users WHERE
                  uid=(:user_id)''', {'user_id':user_id})
    db.commit()


# In[201]:


def delete_region(region_id):
    cursor.execute('''DELETE FROM regions
                    WHERE rid=(:rid)''', {'rid':region_id})
    
    db.commit()
    


# In[202]:


def delete_feature(feature_id):
    cursor.execute('''DELETE FROM bar_features WHERE feature_id=(:feature_id)''', {'feature_id':feature_id})
    cursor.execute('''DELETE FROM features WHERE fid=(:feature_id)''',{'feature_id':feature_id})
    db.commit()
    
    


# In[203]:


def delete_bar_feature(bar_id, feature_id):
    cursor.execute('''DELETE FROM bar_features WHERE bar_id=(:bar_id) AND feature_id=(:feature_id)
                    ''', {'bar_id':bar_id, 'feature_id':feature_id})
    db.commit()


# In[204]:


def delete_bar(bar_id):
    cursor.execute('''DELETE FROM bar_features WHERE bar_id=(:bar_id)''', {'bar_id':bar_id})
    cursor.execute('''DELETE FROM happy_hours WHERE bar_id=(:bar_id)''', {'bar_id':bar_id})
    cursor.execute('''DELETE FROM bars WHERE bid=(:bar_id)''', {'bar_id':bar_id})
    db.commit()


# In[205]:


def delete_happy_hour(hhid):
    cursor.execute('''DELETE FROM happy_hours WHERE hhid=(:hhid)''', {'hhid':hhid})
    db.commit()


# In[206]:


def delete_review(rid):
    cursor.execute('''DELETE FROM reviews WHERE rid=(:rid)''', {'rid':rid})
    db.commit()


# # Seeding/Testing

# ## Create

# In[207]:


create_user("Hopdoddy Manager")
create_user("Able's Manager")
create_user("Pluckers Manager")
create_user("The Local Manager")
create_user("Student")


# In[208]:


cursor.execute('''SELECT * FROM users''')
cursor.fetchall()


# In[209]:


create_region("Domain")
create_region("6th Street")
create_region("West Campus")
create_region("Rainy St")


# In[210]:


cursor.execute('''SELECT * FROM regions''')
cursor.fetchall()


# In[211]:


create_feature("Pool","Pool where customers can drink and swim")
create_feature("Restaurant", "The bar has a restaurant")
create_feature("Pool Table", "This bar has pool tables to play games")


# In[212]:


cursor.execute('''SELECT * FROM features''')
cursor.fetchall()


# In[213]:


create_bar("Hopdoddy",1, 1, "My Address", "1234567890")
create_bar("Rio Rooftop", 2, 2, "My Address", "1234567890")
create_bar("Cain and Able's", 3, 3, "My Address", "1234567890")
create_bar("Pluckers", 3, 4, "My Address", "1234567890")
create_bar("The Local", 3, 5, "My Address", "1234567890")


# In[214]:


cursor.execute('''SELECT * FROM bars''')
cursor.fetchall()


# In[215]:


create_bar_feature(1,2)
create_bar_feature(2,1)
create_bar_feature(3,3)
create_bar_feature(4,2)
create_bar_feature(5,3)


# In[216]:


cursor.execute('''SELECT * FROM bar_features''')
cursor.fetchall()


# In[217]:


create_happy_hour("M", "17:00", "19:00", 1, True, True, "./menus/hopdoddy_menu.pdf")
create_happy_hour("T", "17:00", "19:00", 1, True, True, "./menus/hopdoddy_menu.pdf")
create_happy_hour("W", "17:00", "19:00", 1, True, True, "./menus/hopdoddy_menu.pdf")
create_happy_hour("Th", "17:00", "19:00", 1, True, True, "./menus/hopdoddy_menu.pdf")
create_happy_hour("F", "17:00", "19:00", 1, True, True, "./menus/hopdoddy_menu.pdf")

create_happy_hour("T", "18:00", "20:00", 2, True, False, "./menus/rio_menu.pdf")
create_happy_hour("Th", "18:00", "20:00", 2, True, False, "./menus/rio_menu.pdf")

create_happy_hour("T", "12:00", "0:00", 3, True, False, "./menus/ables_menu.pdf")
create_happy_hour("W", "12:00", "0:00", 3, True, False, "./menus/ables_menu.pdf")
create_happy_hour("Th", "12:00", "0:00", 3, True, False, "./menus/ables_menu.pdf")

create_happy_hour("W", "17:00", "19:00", 4, True, True, "./menus/pluckers_menu.pdf")

create_happy_hour("M", "17:00", "19:00", 5, True, False, "./menus/local_menu.pdf")
create_happy_hour("T", "17:00", "19:00", 5, True, False, "./menus/local_menu.pdf")
create_happy_hour("W", "17:00", "19:00", 5, True, False, "./menus/local_menu.pdf")
create_happy_hour("Th", "17:00", "19:00", 5, True, False, "./menus/local_menu.pdf")


# In[218]:


cursor.execute('''SELECT * FROM happy_hours''')
cursor.fetchall()


# In[219]:


create_review(5, 1, 5)
create_review(5, 2, 3)
create_review(5, 4, 2)
create_review(5, 1, 2)
create_review(5, 3, 5)


# In[220]:


cursor.execute('''SELECT * FROM reviews''')
cursor.fetchall()


# ## Approve Bars

# In[221]:


approve_bar(1)
approve_bar(3)
approve_bar(4)
approve_bar(5)


# ## Read

# In[222]:


all_approved_bars()


# In[223]:


all_approved_hhs()


# In[224]:


bars_in_regions([1,3])


# In[225]:


bars_in_regions([3])


# In[226]:


bars_with_features([3])


# In[227]:


bars_with_rating(5)


# ## Display

# In[228]:


filter_bars([],[],1)


# In[229]:


filter_bars([3],[])


# In[230]:


display_bar(1)


# In[231]:


display_bar(3)


# In[232]:


display_bar_hhs(1)


# In[233]:


display_bar_hhs(3)


# In[234]:


json_object = json.dumps(display_bar_hhs(3))
print (json_object)


# ## Edit

# In[236]:


edit_user(3, "Hopdoddy Manager 1")
cursor.execute('''SELECT * FROM users''')
cursor.fetchall()


# In[237]:


edit_region(1,'Domain (ATX)')
cursor.execute('''SELECT * FROM regions''')
cursor.fetchall()


# In[238]:


edit_feature(1,'Pool Table',"Play pool/billiards")
cursor.execute('''SELECT * FROM features''')
cursor.fetchall()


# In[239]:


edit_bar(3, "Cain and Able's", 3, 3, "Cain's Address", "1231231234")


# In[240]:


approve_bar(3)
cursor.execute('select * from bars')
cursor.fetchall()


# In[241]:


edit_happy_hour(1, 'M', '17:00', "19:30",bar_id=1, drinks=1, food=1, menu_pdf='./menus/hopdoddy_menu.pdf')


# In[242]:


cursor.execute('SELECT * FROM happy_hours')
cursor.fetchall()


# In[243]:


edit_review(rid=1, bar_id=1, star_count=2)


# In[244]:


cursor.execute('SELECT * FROM reviews')
cursor.fetchall()


# ## Delete

# In[102]:


delete_user(1)
cursor.execute('''SELECT * FROM users''')
cursor.fetchall()


# In[103]:


delete_region(2)
cursor.execute('''SELECT * FROM regions''')
cursor.fetchall()


# In[104]:


delete_feature(1)
cursor.execute('''SELECT * FROM features''')
cursor.fetchall()


# In[107]:


delete_bar_feature(2, 1)
cursor.execute("Select * FROM bar_features")
cursor.fetchall()


# In[108]:


delete_bar(1)
cursor.execute("Select * FROM bars")
cursor.fetchall()


# In[110]:


delete_happy_hour(7)
cursor.execute("Select * FROM happy_hours")
cursor.fetchall()


# In[112]:


delete_review(3)
cursor.execute("Select * FROM reviews")
cursor.fetchall()


# # Close the DB

# In[6]:


db.close()

