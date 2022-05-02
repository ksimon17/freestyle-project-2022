# Recipe Generator and Nutrition App - Freestyle Project (Python)

Welcome to the repository of the Recipe Generator App! Please follow the instructions below to implement this program on your own.

# Installation/Setup 

Navigate to an appropriate space on your Desktop to store your code:
```sh
cd ~/Desktop/freestyle-project-2022/
```

Use Anaconda to create and activate a new virtual environment, perhaps called "freestyle-env":
```sh
conda create -n freestyle-env python=3.8
conda activate freestyle-env
```

Then, within an active virtual environment, install package dependencies:
```sh
pip install -r requirements.txt
```

# Setup 

## SendGrid API Key Setup

First, [sign up for a SendGrid account](https://app.sendgrid.com/login?redirect_to=%2Fsettings%2Fapi_keys), then follow the instructions to complete your "Single Sender Verification", clicking the confirmation email to verify your account. 
NOTE: some users in the passed have reported issues with using yahoo-issued, university-issued, or work-issued emails in the past. Consequently, if you run into similar issues when attempt to set up your SendGrid account, perhaps consider using a personal Gmail account. 

Then, [create your SendGrid API Key with "full access" permissions](https://app.sendgrid.com/login?redirect_to=%2Fsettings%2Fapi_keys). Once you create your SendGrid API Key, we will want to store the API Key in an environment variable in the .env file called ```SENDGRID_API_KEY```. Also set an environment variable called ```SENDER_ADDRESS``` to be the same email address as the single sender address you just associated with your SendGrid account.

Use a ".env" file approach to manage these files, as mentioned in the ".env file approach" section below.

## Google Services Setup

This app requires a few Google services for user authentication and data storage. Follow the instructions below to setup these services.

### Google Cloud Project

Visit the [Google Cloud Console](https://console.cloud.google.com). Create a new project, and name it. After it is created, select it from the project selection dropdown menu.

### Google OAuth Client

Visit the [API Credentials](https://console.cloud.google.com/apis/credentials) page for your Google Cloud project. Click the button with the plus icon to "Create Credentials", and choose "Create OAuth Client Id".

Click to "Configure Consent Screen". Leave the domain info blank, and leave the defaults / skip lots of the setup for now. If/when you deploy your app to a production server, you can return to populating this info (or you will be using a different project).

Return to actually creating the "OAuth Client Id". Choose a "Web application" type, give it a name, and set the following "Authorized Redirect URIs" (for now, while the project is still in development):

  + http://localhost:5000/auth/google/callback

After the client is created, note the `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`, and set them as environment variables (see configuration section below).

### Firebase Project
Visit the [Google Firebase Console](https://console.firebase.google.com/) to create a new Firebase project. When you create the project:

  1. Select the Google Cloud project you just created from the dropdown.
  2. Enable Google Analytics.
  3. Configure Google Analytics:
     1. Choose an existing Google Analytics account or create a new one.
     2. Automatically create a new property in this account.

### Google Analytics

From the Firebase project's "Analytics Dashboard" menu, find the web property that was created during the previous step.

If there was an issue and you don't see anything, no worries - you can click the web icon to "Add Firebase to your web app". Give the app a name and register it (hosting not necessary).

You should now be able to visit [Google Analytics](https://analytics.google.com/) and find the web property you created. From Google Analytics, visit the web property's admin settings, specifically the "Data Streams" tab, and click on the stream created by Firebase. Click to enable "enhanced measurement".Note the "Measurement Id" (e.g. "G-XXXXXXXXXX"), and use this value for the `GA_TRACKER_ID` environment variable (see "Environment Variables" section below).


### Firestore Database Setup

Follow [this guide](https://firebase.google.com/docs/firestore/quickstart) to create a Firestore database for the Firebase project you just created. When you create the database, "start in test mode".

### Google Cloud Service Account Credentials

To fetch data from the Firestore database (and use other Google APIs), the app will need access to a local "service account" credentials file.

From the [Google API Credentials](https://console.cloud.google.com/apis/credentials) page, find the service account created during the Firebase project setup process (it should be called something like "firebase-adminsdk"), or feel free to create a new service account.

For the chosen service account, create new JSON credentials file as necessary from the "Keys" menu, then download the resulting JSON file into the root directory of this repo, specifically named "google-credentials.json".

# Configuration

## Environment Variables - ".env" File Approach
You must set up a local file named ".env" that is outside the root directory of the project. In this file, you will be able to store the necessary environment variables to run the program. For the purposes of the shopping-cart program, the following code will suffice:
```sh
# this is the .env file

# SendGrid 
SENDGRID_API_KEY="____________"
SENDER_ADDRESS="____________"

SECRET_KEY="____________"

# Google AUTH
GOOGLE_CLIENT_ID="____________"
GOOGLE_CLIENT_SECRET="___________"

# Google Analytics
GA_TRACKER_ID="UA-XXXXXXX-1"
```
Note that you will need to update the values above variables to match the API keys and credentials that you create after following the instructions in the Setup section above. 

## Usage

### Firebase Service

After configuring the Firestore database and populating it with products, you should be able to test out the app's ability to fetch products (and generate new orders):

```sh
python -m app.firebase_service
```

### Web Application

You can also run the app on your local web server (then visit localhost:5000 in a browser) via the following code in terminal:

```sh
FLASK_APP=web_app flask run
```

## Deploying

See the [Deployer's Guide](/DEPLOYING.md) for instructions on deploying to a production server hosted by Heroku.


## [License](/LICENSE.md)