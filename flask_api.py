from flask import Flask, request


app = Flask(__name__)




users = [
  {
    'username':'Andre3000',
    'email':'outkast@email.com',
    'country':[{'name':'Chile'},
               {'location':'South America'},
               {'highlights': ['skiing', 'patagonia', 'Valparaiso', 'stargazing']}]
  },
  {
    'username':'MrPresi',
    'email':'presi@email.com',
    'country':[{'name':"Morocco"},
               {'location':'Africa'},
               {'highlights': ['Sahara Desert', 'Jamaa el Fna', 'hiking', 'explore the medinas']}]
  },
   {
    'username':'WonderWoman',
    'email':'wonder@email.com',
    'country':[{'name':"Cuba"},
             {'location':'Caribbean'},
             {'body': ['Valle de Vinales', 'tour in classic car', 'caberet show', 'explore Old Havana']}]
   }
]


#heading
@app.route('/<username>')
def intro(username):
    return f"<header>Welcome to <b>Wonderlust</b>, {username}, your digital travel guide!</header>"

#get users
@app.get('/user') #get/retrieve info
def get_users():
    return {'users': users}, 200

#add new user
@app.post('/user') #create/send info
def create_user():
  user_data = request.get_json() #created username and email
  user_data['country'] = [] #to add country into data create a dict
  users.append(user_data) #append new person's info to users
  print(users)
  return user_data, 201

#update name of a country
@app.put('/user') #edit/update info
def update_user():
    user_data = request.get_json()
    new_name = user_data.get('new name') #.get = built in function that outputs a dict value
    for user in users:
        if 'country' in user and 'name' in user['country'][0] and user['country'][0]['name'] == 'Cuba':
            user['country'][0]['name'] = new_name
            return user, 200
    return user, 200


#delete item in highlight list
@app.delete('/user') #delete info
def delete_user():
    user_data = request.get_json()
    for user in users:
        if user['country']['highlights'][0] == user_data['country']['highlights'][0]:
            users.pop()
            print(users)
    return {'message':f'{user_data["country"]["highlights"][0]} is deleted'}, 202
        
        
        
        # user = list(filter(lambda user: user['country']['highlights'][0] == user_data['country']['highlights'][0], users))
        # user.pop(['country']['highlights'][0])
        # print(users)
        # return user, 200


if __name__ == '__main__':
    app.run()