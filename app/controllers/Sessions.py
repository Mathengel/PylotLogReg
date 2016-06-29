from system.core.controller import *

class Sessions(Controller):

    def index(self):
        return self.load_view("index.html")

    def home(self):
        return self.load_view("home.html")


    def register(self):
        self.load_model("User")
        create_status = self.models['User'].registerUser(request.form)

        if create_status['status'] == True:
            session['currentUser'] = create_status["user"]
            return redirect('/home')

        else:
            print create_status['errors']
            for message in create_status['errors']:
                    flash(message[0], message[1])
            return redirect('/')


    def login(self):
        self.load_model("User")
        user = self.models['User'].loginUser(request.form)

        if user['status'] == True:
            session['currentUser'] = user["user"]
            return redirect('/home')
        else:
            flash("Invalid Login information, double check your email and password as a match was not found.", "loginerror")
            return redirect('/')

    def logout(self):
        print session
        session.pop('currentUser', None)
        return redirect('/')

