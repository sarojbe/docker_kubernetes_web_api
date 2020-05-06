from todolist import app


# @login_manager.user_loader
# def load_user(username):
#     return User.get(username)


if __name__ == "__main__":
    app.run(debug=True,port=5000)
