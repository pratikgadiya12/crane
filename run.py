from crane.app import create_app

create_app().run(host="0.0.0.0", port=5001, ssl_context=('/home/randalap/crane/localhost.crt', '/home/randalap/crane/localhost.key'))
