from flask import Flask, render_template, request, session, redirect, url_for,flash,json,jsonify
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,Column,Integer,String,asc
import bcrypt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:12345@127.0.0.1:3306/userinformations'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)                     #mysql://username:password@server/db

# DATABASE TANIMLAMA
class userinformations(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    Name= db.Column(db.String(15),nullable=False)
    Surname = db.Column(db.String(15),nullable=False)
    UserName= db.Column(db.String(15),unique=True,nullable=False)
    Email = db.Column(db.String(35),unique=True,nullable=False)
    Gender = db.Column(db.String(10),nullable=False)
    Password = db.Column(db.String(100),nullable=False)
    isAdmin = db.Column(db.String(10),nullable=False)
    isBanned = db.Column(db.String(10),nullable=False)
    HobbyID = db.Column(db.Integer,nullable=False)
    isAuthor = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "<userinformations(Name='{0}', Surname='{1}', UserName ='{2}', Email ='{3}', Gender='{4}', Password ='{5}',isAdmin = '{6}',isBanned = '{7}',HobbyID = '{8}',isAuthor = '{9}')>".format(self.Name, self.Surname, self.UserName, self.Email, self.Gender, self.Password,self.isAdmin,self.isBanned,self.HobbyID,self.isAuthor)

class hobbies(db.Model):
    HobbyID = db.Column(db.Integer,primary_key=True)
    HobbyName = db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return "<hobbies(HobbyID='{0}', HobbyName='{1}')>".format(self.HobbyID, self.HobbyName)

class authoringapplications(db.Model):
    AuthoringApplicationID = db.Column(db.Integer,primary_key=True)
    AuthoringExperience = db.Column(db.String(20),nullable=False)
    LinkedinAddress = db.Column(db.String(45),nullable=False)
    ApplicantID = db.Column(db.Integer,nullable=False)
    SpecializationAreaID = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "<authoringapplications(AuthoringApplicationID='{0}', AuthoringExperience='{1}', LinkedinAddress='{2}', ApplicantID='{3}', SpecializationAreaID='{4}')>".format(self.AuthoringApplicationID, self.AuthoringExperience, self.LinkedinAddress, self.ApplicantID, self.SpecializationAreaID)

class articles(db.Model):
    ArticleID = db.Column(db.Integer,primary_key=True)
    ArticleName = db.Column(db.String(25),nullable=False)
    ArticleCategoryID = db.Column(db.Integer,nullable=False)
    ArticleText = db.Column(db.String(600),nullable=False)
    AuthorID = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "<articles(ArticleID='{0}', ArticleName='{1}',ArticleCategoryID='{2}',ArticleText='{3}',AuthorID='{4}')>".format(self.ArticleID, self.ArticleName,self.ArticleCategoryID,self.ArticleText,self.AuthorID)

class articlecategories(db.Model):
    ArticleCategoryID = db.Column(db.Integer,primary_key=True)
    ArticleCategoryName = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return "<articlecategories(ArticleCategoryID='{0}', ArticleCategoryName='{1}')>".format(self.ArticleCategoryID, self.ArticleCategoryName)

class articlecomments(db.Model):
    ArticleCommentID = db.Column(db.Integer,primary_key=True)
    CommentText = db.Column(db.String(500),nullable=False)
    ArticleID = db.Column(db.Integer,nullable=False)
    CommenterID = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "<articlecomments(ArticleCommentID='{0}', CommentText='{1}',ArticleID='{2}',CommenterID='{3}')>".format(self.ArticleCommentID, self.CommentText, self.ArticleID, self.CommenterID)

#ANA SAYFA
@app.route("/", methods = ["GET","POST"])
def home():
    return render_template("home.html")

#REGISTER SAYFASI
@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        regInformationUserName = request.form["username"]
        regInformationEmail = request.form["email"]
        if regInformationEmail and regInformationUserName:
                        #cur = mysql.connection.cursor()
                        #cur.execute("SELECT username FROM userinformations WHERE username=%s OR email=%s", (regInformationUserName,regInformationEmail))
                        #ExistQuery = cur.fetchone()
                        #cur.close()
                        #BÖYLE BİR EMAİL - USERNAME KAYITLI MI?
            ExistsQuery = userinformations.query.filter_by(Email = regInformationEmail).first()              
            if ExistsQuery != None:
                flash('Thıs Email or Username already exists!', 'danger')
                return render_template("register.html")
            else:
                try:
                    regInformationName = request.form["name"]
                    regInformationSurname = request.form["surname"]
                    regInformationGender = request.form["gender"]
                    regInformationHobby = request.form["hobby"]
                    regInformationPassword = request.form["password"].encode('utf-8')

                    hash_password = bcrypt.hashpw(regInformationPassword, bcrypt.gensalt())
                    regInformationHobbyName = hobbies.query.filter_by(HobbyName = regInformationHobby).first()  

                                #cur = mysql.connection.cursor()     # isAdmin ,  isAuthor , isBanned işlemleri default verilip yönetilecek
                                #cur.execute("INSERT INTO userinformations(name, surname, username, email, gender, password) VALUES(%s,%s,%s,%s,%s,%s)", (regInformationName, regInformationSurname, regInformationUserName,regInformationEmail,regInformationGender,hash_password))
                                #mysql.connection.commit()
                                #cur.close()            
                    NewUser = userinformations(
                    Name = regInformationName,
                    Surname = regInformationSurname,
                    UserName = regInformationUserName,
                    Email = regInformationEmail,
                    Gender = regInformationGender,
                    Password = hash_password,
                    HobbyID = regInformationHobbyName.HobbyID
                    )
                    db.session.add(NewUser)
                    db.session.commit()

                    flash('You have successfully registered! You are redirected to login section', 'success')
                    return redirect(url_for('login'))
                except:
                    flash('Please fill the information which is given with (*)')
                    return redirect(url_for('register'))
        else:
            flash('Please fill username and email areas')
            return redirect(url_for('register'))  
    

#LOGIN SAYFASI
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        logInformationEmail = request.form["email"]
        logInformationPassword = request.form["password"].encode('utf-8')
        #logInfoHashPassword = bcrypt.hashpw(logInformationPassword, bcrypt.gensalt())        
        #cur = mysql.connection.cursor()
        #cur.execute("SELECT name, surname FROM userinformations WHERE email=%s AND password=%s", (logInformationEmail,logInfoHashPassword))
        #VerificationQuery = cur.fetchone()
        # cur.close()
        if logInformationEmail and logInformationPassword:
            try:            
                VerfLogin = userinformations.query.filter_by(Email = logInformationEmail).first()
                ### EKLE PASSWORD ###
                # KULLANICININ GIRDIGI PASSWORD, DATABASEDE HASHLENMIS SEKILDE TUTULAN
                if bcrypt.checkpw(logInformationPassword, VerfLogin.Password.encode('utf-8')):
                    if VerfLogin.isBanned != "1":
                        session["Name"] = VerfLogin.Name
                        session["Surname"] = VerfLogin.Surname
                        session["isOnline"] = 1
                        session["isAdmin"] = VerfLogin.isAdmin
                        session["isAuthor"] = VerfLogin.isAuthor
                        session["ID"] = VerfLogin.ID          
                    # Email ve password doğrulamasından sonra dönen veri olursa bilgiler doğru demektir. O userı sessionla
                        return redirect("/")
                    else:
                        return render_template("banned.html")
                else:
                    flash('Informations you have entered are not wrong! Please try again')
                    return redirect('/login')
            except:
                flash('Informations you have entered are not wrong! Please try again')
            return redirect(url_for('login'))
        else:
            flash('Please fill given areas')
            return redirect('/login')
    else:
        return render_template('login.html')

        #login olunca logout cıksın vs. onlara bak login olmayı çöz     

#ADMIN 
@app.route("/admin", methods = ["GET","POST"])
def admin():
    if session['isAdmin'] == "0":
        return redirect(url_for('login'))
    else:
        return render_template('admin.html')

#ADMIN PANEL ---- USER UPDATE
@app.route("/admin/userupdate", methods = ["GET","POST"])
def userupdate():
    if request.method == "POST":
        try:
            UserUpdateUserName = request.form["username"]
            UserUpdateEmail = request.form["email"]
            Requesting = request.form["authorize"]
            Updaterwithusername = userinformations.query.filter_by(UserName = UserUpdateUserName).first() 
            Updaterwithemail = userinformations.query.filter_by(Email = UserUpdateEmail).first()
            if not Updaterwithusername:
                Updater = Updaterwithemail
            else:
                Updater = Updaterwithusername
            #update işlemi email ile mi yapılmak isteniyor yoksa username ile mi?
            if Requesting == "authorize":
                Updater.isAdmin = 1
            elif Requesting == "unauthorize":
                Updater.isAdmin = 0
            elif Requesting == "ban":
                Updater.isBanned = 1
            elif Requesting == "unban":
                Updater.isBanned = 0        
            db.session.commit()
            flash('User have been updated','success')
            return render_template("admin.html")
        except:
            flash('Dear admin please give us an username or an email information and be sure that is correct')
            return redirect(url_for('userupdate'))
    else:
        return render_template("userupdate.html")


# ADMIN PANEL ----  USER DEMANDS
@app.route("/admin/userdemands", methods = ["GET","POST"])
def userdemands():
    if request.method =="POST":
        DemanderUserName = request.form["Uname"]
        if "ACCEPT" in request.form:
            GetDemander = userinformations.query.filter_by(UserName = DemanderUserName).first()            
            GetDemander.isAuthor = 1
            DeleteDemand = authoringapplications.query.filter_by(ApplicantID = GetDemander.ID).delete()
            db.session.commit()
            return redirect(url_for("userdemands"))
        else:
            GetDemander = userinformations.query.filter_by(UserName = DemanderUserName).first()
            DeleteDemand = authoringapplications.query.filter_by(ApplicantID = GetDemander.ID).delete()
            db.session.commit()
            return redirect(url_for("userdemands"))
    else:
        UserDemands = authoringapplications.query.all()
        UserDemandsExpList = []
        UserDemandsLinkList = []
        UserDemandsUnameList = []
        UserDemandsSCategoryList = []
        for i in range(len(UserDemands)):
            UserDemandsExpList.append(UserDemands[i].AuthoringExperience)
            UserDemandsLinkList.append(UserDemands[i].LinkedinAddress)
            ApplicantsOtherInformations = userinformations.query.filter_by(ID = UserDemands[i].ApplicantID).first()
            UserDemandsUnameList.append(ApplicantsOtherInformations.UserName)                             #Kişiyi getir      #Kategoriyi getir
            ApplicantsCategoryInformation = articlecategories.query.filter_by(ArticleCategoryID = UserDemands[i].SpecializationAreaID).first()
            UserDemandsSCategoryList.append(ApplicantsCategoryInformation.ArticleCategoryName)
        return render_template("userdemands.html",  DemandNumber = len(UserDemands), 
                                                    UserDemandsExpList = UserDemandsExpList,
                                                    UserDemandsLinkList = UserDemandsLinkList,
                                                    UserDemandsSCategoryList = UserDemandsSCategoryList,
                                                    UserDemandsUnameList = UserDemandsUnameList)                                                                                 


#BE AUTHOR
@app.route("/beauthor" , methods = ["GET","POST"])
def beauthor():
    if request.method == "POST":
        ApplicantsExperience = request.form["experience"]
        ApplicantsLinkedin = request.form["linkedin"]
        ApplicantsCategory = request.form["specializationcategory"]
        AlreadyApplied = authoringapplications.query.filter_by(ApplicantID = session["ID"]).first()
        if AlreadyApplied:                                                      #Başvuru önceden zaten yapılmışsa işlemi bırak ve article kısmına dön
            flash("You have already applied  for authoring")
            return redirect(url_for('article'))
        else:                                                                                   #Öncesinden bir başvuru yoksa her yer doldurulmuş mu kontrol et
            if  not (ApplicantsCategory and ApplicantsCategory and ApplicantsLinkedin):
                flash("Please fill the given areas")                                                
                return redirect(url_for('beauthor'))
            else:
                ApplicantsLinkedinAddress = "https://www.linkedin.com/in" + ApplicantsLinkedin + "/"
                ApplicantsExperience = ApplicantsExperience + " years"         
                NewAuthoringApplication = authoringapplications(
                    AuthoringExperience = ApplicantsExperience,
                    LinkedinAddress = ApplicantsLinkedinAddress,
                    ApplicantID = session["ID"],
                    SpecializationAreaID = ApplicantsCategory
                    )
                db.session.add(NewAuthoringApplication)
                db.session.commit()
                flash("You have successfully applied!")
                return render_template("article.html")
        return redirect(url_for('article'))
    else:
        SpecializationCategories = articlecategories.query.order_by(asc(articlecategories.ArticleCategoryID)).all()
        SpecializationCategoriesList = []
        for i in range(len(SpecializationCategories)):
            SpecializationCategoriesList.append(SpecializationCategories[i].ArticleCategoryName)
        return render_template("beauthor.html",SpecializationCategoriesList = SpecializationCategoriesList)


#ADD ARTICLE
@app.route("/author/addarticle", methods = ["GET","POST"])
def addarticle():
    if request.method == "POST":
        NewArticleName = request.form["articlename"]
        NewArticleCategoryID = request.form["articlecategory"]
        NewArticleText = request.form["articletext"]
        if NewArticleName and NewArticleCategoryID and NewArticleText:
            VerfExistArticleName = articles.query.filter_by(ArticleName = NewArticleName).first()
            VerfExistArticleText = articles.query.filter_by(ArticleText = NewArticleText).first()
            if VerfExistArticleName or VerfExistArticleText:
                flash("This article name or article text is already exists")
            else:
                NewArticle = articles(
                    ArticleName = NewArticleName,
                    ArticleCategoryID = NewArticleCategoryID,
                    ArticleText = NewArticleText,
                    AuthorID = session["ID"]
                    )
                db.session.add(NewArticle)
                db.session.commit()
            return redirect(url_for('addarticle'))
        else:
            flash('Please fill the areas given below correctly')
            return redirect(url_for('addarticle'))
    else:
        return render_template('addarticle.html')

#DELETE ARTICLE
@app.route("/author/deletearticle", methods = ["GET","POST"])
def deletearticle():
    if request.method == "GET":
        AuthorArticles = articles.query.filter_by(AuthorID = session["ID"]).all()
        Extra = []
        for i in range(len(AuthorArticles)):
            Extra.append(AuthorArticles[i].ArticleName)               
        return render_template('deletearticle.html',Extra = Extra)             
    else:
        try:                     
            DeletingArticle = request.form["delete"]
            print(DeletingArticle)
            DeletingArticleQuery = articles.query.filter_by(ArticleName = DeletingArticle).delete()
            db.session.commit()
            return redirect(url_for('deletearticle'))
        except:
            flash('Please select an article to delete!')
            return redirect(url_for('deletearticle')) 


#ReadArticle
@app.route("/readarticle", methods = ["GET","POST"])
def readarticle():
    if request.method == "GET":
        WholeCategories = articlecategories.query.order_by(asc(articlecategories.ArticleCategoryID)).all()
        WholeCategoriesList = []
        for i in range(len(WholeCategories)):
            WholeCategoriesList.append(WholeCategories[i].ArticleCategoryName)
        #kategoriler çekilip WholeCategoriesList listesine atandı.                
        return render_template('readarticle.html',WholeCategoriesList = WholeCategoriesList) 
    else:
        try:
            Reading = request.form["articlelist"]
            ReplacedEdit = Reading.replace(" ", "").lower()
            session["readingarticle"] = Reading     
            return redirect(url_for('readingarticle',reading_article = ReplacedEdit))
        except:
            flash('Please select an article to read!')
            return redirect(url_for('readarticle')) 
        #return edip tekrar aynı yere geliyoruz.
       

@app.route("/readarticle/<get_article>", methods = ["GET","POST"])
def getarticle(get_article):
    Articles = articles.query.filter_by(ArticleCategoryID = get_article).all()
    ArticleList = []
    for i in range(len(Articles)):
        ArticleList.append(Articles[i].ArticleName)            
    return jsonify({'articlelists':ArticleList})

@app.route("/readingarticle/<reading_article>", methods = ["GET","POST"])
def readingarticle(reading_article):
    ReadingArticle = articles.query.filter_by(ArticleName = session["readingarticle"]).first()
    if request.method == "GET":
        ReadingArticlesComments = articlecomments.query.filter_by(ArticleID = ReadingArticle.ArticleID).all()      # Makaleye yapılan yorumların bilgilerinin hepsi alındı
        ReadingArticlesCommentTextList = []                                                                      #Yorumların text kısımları ve yazan kişinin ID bilgisi alınmak için listeler hazırlandı
        ReadingArticlesCommenterIDList = []
        ReadingArticlesCommenterUsernameList = []
        for i in range(len(ReadingArticlesComments)):
            IsCommenterBanned = userinformations.query.filter_by(ID = ReadingArticlesComments[i].CommenterID).first()
            if IsCommenterBanned.isBanned != "1":                #Banlı olmayan kullanıcıların yorumlarını getir
                ReadingArticlesCommentTextList.append(ReadingArticlesComments[i].CommentText)               #Yorum text kısımları ve yazan kişinin ID bilgisi listelendi
                ReadingArticlesCommenterIDList.append(ReadingArticlesComments[i].CommenterID)
                                                               #Kişinin ID bilgisinden yola çıkılarak Username elde edildi
                CommenterUsernameQuery = userinformations.query.filter_by(ID = ReadingArticlesCommenterIDList[i]).first()
                ReadingArticlesCommenterUsernameList.append(CommenterUsernameQuery.UserName)         # For loop için yorum sayısını da gönderdik
        return render_template('blog/readingarticle.html',ReadingArticle = ReadingArticle,CommenterUserNameList = ReadingArticlesCommenterUsernameList,CommentList = ReadingArticlesCommentTextList,CommentNumber = len(ReadingArticlesCommentTextList))
    else:
        return redirect(url_for('readarticle'))

@app.route("/commentingarticle",methods = ["POST"])
def comment():
    CommentText = request.form["commenttext"]
    if comment:
        CommenterID = session["ID"]
        CommentedArticle = articles.query.filter_by(ArticleName = session["readingarticle"]).first()
        NewComment = articlecomments(
            CommentText = CommentText,
            ArticleID = CommentedArticle.ArticleID,
            CommenterID = session["ID"]
            )
        db.session.add(NewComment)
        db.session.commit()
        ReturningArticle = session["readingarticle"]
        ReplacedReturningArticle = ReturningArticle.replace(" ", "").lower()
        print(ReplacedReturningArticle)
    return redirect(url_for('readingarticle', reading_article = ReplacedReturningArticle))

@app.route("/author/editarticle", methods = ["GET","POST"])
def editarticle():
    if request.method == "GET":
        EditArticle = articles.query.filter_by(AuthorID = session["ID"]).all()
        EditArticleList = []
        for i in range(len(EditArticle)):
            EditArticleList.append(EditArticle[i].ArticleName)             
        return render_template('editarticle.html',EditArticleList = EditArticleList)             
    else:
        try:                     
            EditingArticle = request.form["editarticle"]
            ReplacedEdit = EditingArticle.replace(" ", "").lower()  #url kısmında görünmesin diye bosluklar siliniyor
            session["EditingArticle"] = EditingArticle       ###****url_for ile gönderilemediği için sessionlayıp gönderiyoruz *****######        
            return redirect(url_for('editingarticle',EditingName = ReplacedEdit ))
        except:
            flash("Please select an article")
            return redirect(url_for("editarticle"))

@app.route("/author/editarticle/<EditingName>", methods = ["GET","POST"])
def editingarticle(EditingName):
    EditingArticle = articles.query.filter_by(ArticleName = session["EditingArticle"]).first()
    if request.method == "GET":
        return render_template('blog/editingarticle.html',EditingArticle = EditingArticle)
    else:
        EditedArticleName = request.form["editedarticlename"]
        EditedArticleText = request.form["editedarticletext"]        
        EditingArticle.ArticleName = EditedArticleName
        EditingArticle.ArticleText = EditedArticleText
        db.session.commit()
        return redirect(url_for('editarticle'))

#LOGOUT 
@app.route("/logout", methods = ["GET","POST"])
def logout():
    session.clear()
    return render_template('home.html')

@app.route("/article", methods = ["GET","POST"])
def article():
    return render_template('article.html')

#SON DOKUNUŞ
if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()