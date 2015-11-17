# elhacko-flasko

About the imgur stuff:
-
It is a little tricky to set up for the first time.
Our imgur account already has been linked to our app, but if we would want to do it again just follow [this documentation] (https://api.imgur.com/)

**Summary of the instructions (still recommend you to give it a read):**
* Register your app (https://api.imgur.com/oauth2/addclient) - this gives you a CLIENT ID and CLIENT SECRET
* Authorize as an imgur user (fill the params) 
* https://api.imgur.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&response_type=REQUESTED_RESPONSE_TYPE&state=APPLICATION_STATE
* This gives you the PIN number (only needed once for every app)

**Note:**
* In our case the redirect url is not important, we wont be using it, fill it with whatever.
* The `state` param is whatever you want it to be, it would be sent to the redirect url to check transaction was OK. Optional.


**Our app configuration:**
* Go to the `imgur` folder
* Create `imgurconf.py` like this:

```python
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
PIN = 'YOUR PIN'
```
* Create `imgurtokens.py` as an emtpy file like this: `touch imgurtokens.py` from within the `imgur` folder
* Run `python initial_setup.py`
* This will fill the `imgurtokens.py` file - please check (usual issues are file permissions related)
* Now check the `albumconf.py` file, fill it up as desired and save.
* Run `python album_setup.py`
* This will fill the `albumhash.py` file - please check (usual issues are file permissions related)

Now you are all set, we are ready to run `python fapp.py` from the root folder.

