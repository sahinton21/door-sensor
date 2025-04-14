//This is the controller for the index page. It mostly deals with logging users in and creating new accounts
//We will handle logging users in by sending them to the right page

var app = angular.module('myApp', []);
app.controller("IndexController", function($http, $scope, $q){


  //This is the scope variable for the door
  $scope.door;

  $scope.doorFlag = false;

  // This is the function to load the status of the door on start
  $scope.loadDoor = function(){

    //Make the GET request
    $http.get("/door").then(function(response){

      //
      $scope.door = response.data;

      //Now we can show off the status of our door

      // Put some flag to show some more content
      if($scope.door.status == 'Open'){
        $scope.doorFlag = true;
      }
      else{
        $scope.doorFlag = false;
      }


    });
  }

  //Send an HTTP post that will alert the arduino
  $scope.armDoor = function(){

    //Create a JSON object
    var status = {"state":"Alert"};

    $http.put("/door/alarm", status).then(function(response){ 
      // we expect a 200 and should update the user content
      console.log("Arming");
      location.reload();
    });
  }
  $scope.disarmDoor = function(){

    var status = {"state":"Closed"};

    $http.put("/door/alarm", status).then(function(response){ 
      // we expect a 200 and should update the user content
      console.log("Disarming");
      location.reload();
    });
  }

  $scope.loadDoor();

  
});