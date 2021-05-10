module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            // Load the directory tree from local files and creates an JSON file
            "/tmp/syd_relative_s1.json" : "syd_relative/scenario_1"
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
            "http://admin:admin@172.17.0.4:5984/twitter" : "/tmp/syd_relative_s1.json"
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};

