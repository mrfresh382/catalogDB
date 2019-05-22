#!/usr/bin/env python

# See readme.md for full instructions on running this
# Webapp. This is the Catalog App for
# the FSND written by Doug McDonald
# This is a website for a fictional store at the
# Big Bend national park in Southwest Texas
import os
import sys
import random
import string
import json
import httplib2
import requests

from flask import Flask, render_template, request, \
 redirect, jsonify, url_for, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
from flask import make_response

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from catalogDB_setup import Base, Category, Item, User

app = Flask(__name__)
# Connect to Database and create database session
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
# Needs to be same file name as JSON file downloaded
# from Google OAUTH API website
# Login.html will need to be updated with your Google API id before running on
# your local machine.
APPLICATION_NAME = "Catalog App"

engine = create_engine(
    'sqlite:///catalog-db.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# These are functions to reduce repetitive code
# These are created from the Udacity Full Stack Lessons
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                 'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except (IndexError, KeyError):
        return None


# Use email address for authorization
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# This app uses Google OAuth 2.0 API for login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade \
                                 the auth code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps('error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't\
                match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does \
                not match app's"), 401)
        print "Token's client ID does not match the app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Printing login info for debug purposes
    for a in data:
        print a

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # HTML output is created to show that login is successful
    # User is redirected to the homepage
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height 300px;border-radius: \
            150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    print "Login Success!"
    return output


# Logout function for the app
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # The print lines can be commented or deleted, and are for debug only
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        tempUserName = login_session['username']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        response = make_response(json.dumps('Successfully disconnected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'

        flash("%s has logged out" % tempUserName)
        print "Logout Success!"
        # The current user's name is stored before they logout
        return render_template('logout.html', tempUserName=tempUserName)
    else:
        response = make_response(json.dumps('Failed to revoke token for \
                given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view category Information
@app.route('/category/<int:category_id>/list/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/list/<int:list_id>/JSON')
def itemJSON(category_id, list_id):
    singleItem = session.query(Item).filter_by(category_id=category_id,
                                               id=ist_id).one()
    return jsonify(Item=singleItem.serialize)


@app.route('/category/JSON')
def wholeStoreJSON():
    wholeStore = session.query(Category).all()
    return jsonify(WholeStore=[r.serialize for r in wholeStore])


# Catalog Main page for online store- All catagories shown
# A Public template is rendered for users not logged in
@app.route('/')
@app.route('/category/')
def showCategorys():
    categorys = session.query(Category).order_by(asc(Category.name))
    listOfItemNames = [[]]
    indexOfNames = 0
    # This block of code is giving the mainpage the ability to
    # show individual store items for each category. When
    # the user hovers over the category, a drop down will
    # display of items in that category
    for category in categorys:
        itemList = session.query(Item).filter_by(category=category).all()
        for name in itemList:
            listOfItemNames[indexOfNames].append(name.name)
            listOfItemNames.append([])
        indexOfNames += 1
    if 'username' not in login_session:
        return render_template(
            'publiccategories.html', category=categorys,
            listOfItemNames=listOfItemNames)
    else:
        return render_template(
            'categories.html', category=categorys,
            user_id=login_session['user_id'],
            listOfItemNames=listOfItemNames)


# Create a new category
# If the user is not logged in and types in the URL, they will
# be redirected to the login page. If they get past that,
# then a Javascript alert will be displayed. This is the
# same process for Delete and Edit functions also.
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        flash('Please login to create a category')
        return redirect('/login')
    if request.method == 'POST' and login_session['user_id']:
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategorys'))
    elif not login_session['user_id']:
        return "<script> function myFunc() { alert('You are not logged in \
                to create a category. Please login and stop trying to \
                break in.');} </script><body onload='myFunc()'>"
    else:
        return render_template('newcategory.html')


# Edit a category name
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        flash('Please login to edit a category')
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return "<script> function myFunc() { alert('You are not authorized to\
                edit this category. Please create your own category.');}\
            </script><body onload='myFunc()'>"
    if request.method == 'POST' and login_session['user_id']:
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showList', category_id=editedCategory.id))
    else:
        return render_template('editcategory.html', category=editedCategory,
                               user_id=login_session['user_id'])


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()

    # The items in a category must be also deleted, otherwise, they
    # will later appear in new categorys. Per discussion on the
    # Udacity knowledge forum, this may be handled a different way.

    itemsToDelete = session.query(Item).filter_by(
        category_id=category_id).all()
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script> function myFunc() { alert('You are not \
                authorized to delete from this category. \
                Please create your own category.');}</script><body \
                onload='myFunc()'>"
    if request.method == 'POST' and login_session['user_id']:
        session.delete(categoryToDelete)
        for itemToDelete in itemsToDelete:
            session.delete(itemToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategorys', category_id=category_id))
    else:
        return render_template(
            'deletecategory.html',
            category=categoryToDelete, user_id=login_session['user_id'])


# Show a single category list of store items
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/list/')
def showList(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    creator = getUserInfo(category.user_id)

    # This block of code determines if the user is logged in
    # , will display a Login link if they are NOT logged in
    # , and deplay a Logout link if they are logged in on the
    # list page
    try:
        if creator.id == login_session['user_id']:
                mustLogin = False
        # print "client must login = false"
        else:
            mustLogin = True
            # print "client must login = true"
    except (IndexError, KeyError):
        mustLogin = True
        # print "indexerror for login"

    if 'username' not in login_session or creator.id \
            != login_session['user_id']:
        return render_template(
                'publiclist.html',
                items=items,
                category=category,
                creator=creator, mustLogin=mustLogin)
    else:
        return render_template('list.html', items=items, category=category,
                               creator=creator, mustLogin=mustLogin)


# Create a new store item
@app.route('/category/<int:category_id>/list_id/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session['user_id']:
        return "<script> function myFunc() { alert('You are not authorized to \
                create items. Please create your own category.');} \
                </script><body onload='myFunc()'>"
    if request.method == 'POST' and login_session['user_id']:
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'], category_id=category_id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item Successfully Created : %s' % (newItem.name))
        return redirect(url_for('showList', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


# Edit a store item
@app.route('/category/<int:category_id>/list/<int:list_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(Item).filter_by(id=list_id).one()
    if request.method == 'POST' and login_session['user_id']:
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        # The two if statements below correct a bug where changing the
        # decription or price to a
        # blank entry will not change the database entry to an empty
        # string. This logic is not applied to the name.
        if request.form['description'] == '':
            editedItem.description = ''
        if request.form['price'] == '':
            editedItem.price = ''
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showList', category_id=category_id))
    else:
        return render_template(
            'edititem.html', category_id=category_id,
            list_id=list_id, item=editedItem)


# Delete an individual item
@app.route('/category/<int:category_id>/list/<int:list_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    tempCategory = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=list_id).one()
    if request.method == 'POST' and login_session['user_id']:
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showList', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
