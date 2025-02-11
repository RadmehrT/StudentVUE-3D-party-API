from StudentVUE_API import StudentVUE_API


new_Session = StudentVUE_API()

new_Session.set_username("")
new_Session.set_password("")

new_Session.set_json_file_name("course_history")

new_Session.run()

if str(input("Delete json of course history?: ")) == "y":
    new_Session.delete_json_file(new_Session.get_json_file_name())
    
new_Session.get_username()
new_Session.get_password()    