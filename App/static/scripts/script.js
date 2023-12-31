angular.module("App", [])  // Define an Angular module named "App" with no dependencies.
    .controller("SearchCtrl", function ($scope, $http) {

        // Initialize an empty array to store search results.
        $scope.results = [];

        // Define a function for handling the search operation.
        $scope.search = function () {
            $scope.results = [];  // Clear previous search results.

            // Modify the CSS properties of the <ul> element using jQuery.
            $("ul").css({
                marginTop: "500px",
                opacity: 0
            });

            if ($scope.searchTerm) {
                // Define the query api
                var api = "/kg_math/search?q="

                var requestUrl = api + $scope.searchTerm
                // Sending our request
                $http({
                    method: 'GET',
                    url: requestUrl
                })
                    .then(response => response.data)
                    .then(data => {
                        // No result, query failed.
                        if (data.length == 0) {
                            alert(`查询失败! 没有找到 ${$scope.searchTerm}`)
                            return;
                        }
                        var notifyString = "查询成功!\n\n";
                        // Redener result for each entity 
                        data.forEach(entity => {
                            // Result is a textbook
                            if (entity.isTextbook) {
                                var knowledges = entity.knowledge
                                knowledges.forEach(result => {
                                    $scope.results.push({
                                        title: result.name,
                                        body: result.label
                                    });
                                })
                                notifyString += `《${knowledges[0].name}》是一本教科书!\n\n`
                            } else {
                                // Result is an topic or knowledge point
                                var wikiResults = entity.wikipedia
                                wikiResults.forEach(result => {
                                    $scope.results.push({
                                        title: result.title,
                                        body: result.extract,
                                        page: result.url
                                    });
                                })
                                notifyString += getEntityLocation(entity) + '\n\n';
                            }

                        })
                        notifyString += "\n请退出该对话框查看详细结果。"
                        alert(notifyString);
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
        $scope.cancel = function () {
            $scope.searchTerm = "";  // Clear the search term.
            $scope.searched = false;  // Reset the search flag.
            $("input").focus();  // Set focus on the input element.
        };
    });

const locationString = [
    "教材",
    "章节",
    "专题",
    "小专题",
    "知识点"
]

// Get a no textbook entity's location in the textbook.
function getEntityLocation(entity) {
    var level = entity.level;
    var location = Object.values(entity.location);
    var result = `${location[level - 1]}是一个${locationString[level - 1]},`;
    for (var i = 1; i < level; i++) {
        switch (i) {
            case 1:
                result += `它在${location[i - 1]}教材上`
                break;
            case 2:
                result += `${location[i - 1]}章节中`
                break;
            case 3:
                result += `${location[i - 1]}专题下`
                break;
            case 4:
                result += `${location[i - 1]}小专题中`
                break;
            default:
                break;
        }
        if (i != level - 1) {
            result += '的'
        }
    }
    result += "."
    // console.log(result)
    return result
}