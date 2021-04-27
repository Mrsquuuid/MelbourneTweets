module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            // Load the directory tree from local files and creates an JSON file
            "/tmp/app.json": "designs" 
          }
        }
      },
      "couch-push": {
        options: {
          user: process.env.user,
          pass: process.env.pass
        },
        twitter: {
          files: {
            // Deploy the JSON file to CouchDB
            "http://admin:8185050@localhost:5984/twitter%2Fcity%2Fperth": "/tmp/app.json" 
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};

