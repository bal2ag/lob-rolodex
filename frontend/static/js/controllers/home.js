angular.module('LobRolodex.homeControllers', ['angularUtils.directives.dirPagination'])
.controller('HomeController', function($scope, $http) {
    $scope.addresses = [];
    $scope.totalAddresses = 0;
    $scope.addressesPerPage = 10;
    getResultsPage(1);

    $scope.pagination = {
        current: 1
    };

    $scope.pageChanged = function(newPage) {
        getResultsPage(newPage);
    };

    function getResultsPage(pageNumber) {
        $http.get('/ajax/addresses',
            {params: {
                page: pageNumber,
                limit: $scope.addressesPerPage
            }}).then(
            function success(response) {
                $scope.addresses = response.data.addresses;
                $scope.totalAddresses = response.data.total;
            }, function error(response) {
                console.log(response);
            }
        );
    };
});
