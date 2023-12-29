angular.module("App", [])  // Define an Angular module named "App" with no dependencies.
  .controller("SearchCtrl", function($scope, $http) {

    // Initialize an empty array to store search results.
    $scope.results = [];

    // Define a function for handling the search operation.
    $scope.search = function() {
      $scope.results = [];  // Clear previous search results.

      // Modify the CSS properties of the <ul> element using jQuery.
      $("ul").css({
        marginTop: "500px",
        opacity: 0
      });

      if ($scope.searchTerm) {
        // Define the Wikipedia API endpoint for search and article retrieval.
        var api = 'http://zh.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrlimit=10&prop=pageimages|extracts&pilimit=max&exintro&explaintext&exsentences=1&exlimit=max&gsrsearch=';
        var cb = '&callback=JSON_CALLBACK';
        var page = 'http://en.wikipedia.org/?curid=';

        // Use AngularJS's $http service to make a JSONP request to the Wikipedia API.
        $http.jsonp(api + $scope.searchTerm + cb)
          .success(function(data) {
            // Process the retrieved data and populate the $scope.results array.
            var results = data.query.pages;
            angular.forEach(results, function(value, key) {
              $scope.results.push({
                title: value.title,
                body: value.extract,
                page: page + value.pageid
              });
            });
          });

        // Use jQuery to animate the <ul> and .search elements.
        $("ul").animate({
          marginTop: "30px",
          opacity: 1
        }, 900);

        $(".search").animate({
          marginTop: "30px"
        }, 800);

        $scope.searched = true;  // Set a flag to indicate that a search has been performed.
      }
    };

    // Define a function to cancel the search.
    $scope.cancel = function() {
      $scope.searchTerm = "";  // Clear the search term.
      $scope.searched = false;  // Reset the search flag.
      $("input").focus();  // Set focus on the input element.
    }
  });
