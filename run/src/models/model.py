#!/usr/bin/env python3

import sqlite3
import time

from flask import session
from random import randint
from time import gmtime, strftime, sleep

from ..mappers.opencursor import OpenCursor

class User:
    def __init__(self, row={}, username='', password=''):
        if username:
            self.check_cred(username,password)
        else:
            self.row_set(row)

    def __enter__(self):
        return self

    def __exit__(self,exception_type,exception_value,exception_traceback):
        sleep(randint(10,10000)/10000)

    def row_set(self,row={}):
        row           = dict(row)
        self.pk       = row.get('pk')
        self.username = row.get('username')
        self.password = row.get('password')
        self.age      = row.get('age')
        self.gender   = row.get('gender')

    def check_cred(self,username,password):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user WHERE
                  username=? and password=?; """
            val = (username,password)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})

    def check_un(self,username):
        with OpenCursor() as cur:
            SQL = """ SELECT username FROM user WHERE
                  username=?; """
            val = (username,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return True
        else:
            return False

    def login(self,password):
        with OpenCursor() as cur:
            cur.execute('SELECT password FROM user WHERE username=?;',(self.username,))
            if password == cur.fetchone()['password']:
                return True
            else:
                return False

    def create_user(self,username,password,age,gender):
        self.username = username
        self.password = password
        self.age      = age
        self.gender   = gender
        with OpenCursor() as cur:
            SQL = """ INSERT INTO user(
                username,password,age,gender) VALUES (
                ?,?,?,?); """
            val = (self.username,self.password,self.age,self.gender)
            cur.execute(SQL,val)
    
    def favoriteShoe(self,shoename,pk):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user_favorites WHERE  
                user_pk = ? and shoename= ?; """
            val = (pk,shoename)
            cur.execute(SQL,val)
            data = cur.fetchone()
        if data:
            print("Already Saved")
            return False
        else:
            userFav          = UserFavorites()
            userFav.shoename = shoename
            userFav.user_pk  = pk
            userFav.save()
    
    def display_favorites(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user_favorites WHERE
                  user_pk=?; """
            val = (self.pk,)
            cur.execute(SQL,val)
            row = cur.fetchall()
        if row:
            favorite_list=[]
            for rows in row:
                shoe = rows['shoename']
                favorite_list.append(shoe)
            return favorite_list
        else:
            favorite_list=[]
            return favorite_list
    
    def display_shoebox(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM shoebox WHERE
                  user_pk=?; """
            val = (self.pk,)
            cur.execute(SQL,val)
            row = cur.fetchall()
        if row:
            shoebox = {}
            key=0
            for rows in row:
                shoebox[key] = {
                    'shoename': rows['shoename'],
                    'type': rows['type'],
                    'date': rows['date'],
                    'price_bought': rows['price_bought'],
                    'price_sold': rows['price_sold'],
                    'pk': rows['pk']
                }
                key+=1
            return shoebox
        else:
            shoebox={}
            return shoebox

    def get_pk(self,username):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user WHERE
                  username=?; """
            val = (username,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return row['pk']
        else:
            return False

    def insert_preferences(self,brands,colors,pk):
        userPref = UserPreferences()
        userPref.brand   = brands
        userPref.color   = colors
        userPref.user_pk = pk
        userPref.save()
    
    def add_to_box(self,type,shoename,date,price_bought,pk,price_sold=''):
        print(pk)
        if type == 'Buy':
            box = ShoeBox()
            box.shoename = shoename
            box.type = 'BUY'
            box.date = date
            box.price_bought = price_bought
            box.price_sold = 0
            box.user_pk = pk
            box.save()
        else:
            box = ShoeBox()
            box.shoename = shoename
            box.type = 'SELL'
            box.date = date
            box.price_bought = price_bought
            box.price_sold = price_sold
            box.user_pk = pk
            box.save()
    
    def get_preferences(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user_preferences WHERE
                  user_pk=?; """
            val = (self.pk,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            brands = row['brand'].split('-')
            colors = row['color'].split('-')
            return [brands,colors]
        else:
            return False

class ShoeView:

    def __init__(self,row={},shoename=''):
        if shoename:
            self.check_shoe(shoename)
        else:
            self.row_set(row)

    def row_set(self,row={}):
        row              = dict(row)
        self.pk          = row.get('pk')
        self.shoename    = row.get('shoename')
        self.click_count = row.get('click_count')
    
    def check_shoe(self,shoename):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM shoes_viewed WHERE
                  shoename=?; """
            val = (shoename,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})
    
    def trending_list(self):
        with OpenCursor() as cur:
            SQL = """ SELECT shoename FROM shoes_viewed 
            ORDER BY click_count DESC limit 40; """
            cur.execute(SQL)
            data = cur.fetchall()
            trending_list=[]
            for row in data:
                shoename = row['shoename']
                trending_list.append(shoename)
            return trending_list

    def __bool__(self):
        return bool(self.pk)
    
    def save(self,shoeName):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE shoes_viewed SET 
                    shoename = ?, click_count = ?
                    WHERE shoename=?; """
                val = (self.shoename, (self.click_count+1), self.shoename)
                cur.execute(SQL, val)
        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO shoes_viewed (
                    shoename, click_count)
                    VALUES (?, ?); """
                val = (shoeName, 1)
                cur.execute(SQL, val)
                self.pk = cur.lastrowid

class UserFavorites:

    def __init__(self, row={}):
        row           = dict(row)
        self.pk       = row.get('pk')
        self.shoename = row.get('shoename')
        self.user_pk  = row.get('user_pk')

    def __bool__(self):
        return bool(self.pk)
    
    def save(self):
        with OpenCursor() as cur:
            SQL = """ INSERT INTO user_favorites(
                shoename,user_pk
                ) VALUES (?,?); """
            val = (self.shoename,self.user_pk)
            cur.execute(SQL,val)
    
    def remove(self,shoename):
        with OpenCursor() as cur:
            SQL = """ REMOVE FROM user_favorites WHERE 
                shoename=? and user_pk=?; """
            val = (shoename,self.pk)
            cur.execute(SQL,val)

    def __repr__(self):
        output = 'Account: {}, Shoe: {}'
        return output.format(self.account_pk,self.shoename)

class UserPreferences:

    def __init__(self, row={}):
        row           = dict(row)
        self.pk       = row.get('pk')
        self.brand    = row.get('brand')
        self.color    = row.get('color')
        self.user_pk  = row.get('user_pk')

    def __bool__(self):
        return bool(self.pk)
    
    def check_against_all(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user_preferences; """
            cur.execute(SQL,)
            data = cur.fetchall()
            check_list = []
            for row in data:
                brands = row['brand'].split('-')
                colors = row['color'].split('-')
                user_pk = row['user_pk']
                check_list,append([brands,colors,user_pk])
            return check_list

    def save(self):
        with OpenCursor() as cur:
            SQL = """ INSERT INTO user_preferences(
                brand,color,user_pk
                ) VALUES (?,?,?); """
            val = (self.brand,self.color,self.user_pk)
            cur.execute(SQL,val)

    def __repr__(self):
        output = 'Account: {}, Brand: {}, Color: {}'
        return output.format(self.user_pk,self.brand,self.color)

class ShoeBox:

    def __init__(self, row={}):
        row               = dict(row)
        self.pk           = row.get('pk')
        self.shoename     = row.get('shoename')
        self.type         = row.get('type')
        self.date         = row.get('date')
        self.price_bought = row.get('price_bought')
        self.price_sold   = row.get('price_sold')
        self.user_pk      = row.get('user_pk')

    def __bool__(self):
        return bool(self.pk)
    
    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE shoebox SET 
                    shoename=?, type=?, date=?, price_bought=?, price_sold=?, user_pk=?
                    WHERE shoename=?; """
                val = (self.shoename, self.type, self.date, self.price_bought, self.price_sold, self.user_pk)
                cur.execute(SQL, val)
        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO shoebox (
                    shoename, type, date, price_bought, price_sold, user_pk)
                    VALUES (?, ?, ?, ?, ?, ?); """
                val = (self.shoename, self.type, self.date, self.price_bought, self.price_sold, self.user_pk)
                cur.execute(SQL, val)
                self.pk = cur.lastrowid

    # def __repr__(self):
    #     output = 'Account: {}, Brand: {}, Color: {}'
    #     return output.format(self.user_pk,self.brand,self.color)