module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            // Load the directory tree from local files and creates an JSON file
            "/tmp/syd_relative_s1.json" : "syd_relative/scenario_1",
            "/tmp/syd_geo_s1.json" : "syd_geo/scenario_1",
            "/tmp/melb_geo_s2.json" : "melb_geo/scenario_2",
            "/tmp/current_all_s3.json" : "current_all/scenario_3"
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
            "http://admin:8185050@localhost:5984/twitter%2Ftest%2Frelative" : "/tmp/syd_relative_s1.json",
            "http://admin:8185050@localhost:5984/twitter%2Ftest%2Fgeo" : "/tmp/syd_geo_s1.json", 
            "http://admin:8185050@localhost:5984/twitter%2Ftest%2Fgeo" : "/tmp/melb_geo_s2.json", 
            "http://admin:8185050@localhost:5984/twitter%2Fcurrent%2Fall" : "/tmp/current_all_s3.json"
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};

