
angular.module('LobRolodex.controllers', ['angularUtils.directives.dirPagination'])
.controller('HomeController', ['$scope', '$http', 'formattingService', function($scope, $http, formattingService) {
    $scope.formatting = formattingService;

    $scope.addresses = [];
    $scope.totalAddresses = 0;
    $scope.addressesPerPage = 5;
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

    $scope.redirectToSendCardView = function(address) {
        window.location = 'address/' + address.id + '/send';
    };

    $scope.getRemoveAddressUrl = function(address) {
        return 'address/' + address.id + '/remove';
    };
}])
.controller('NewAddressController', function($scope) {
    $scope.country = 'US';

    // Need this hack because the bootstrap form helpers do some weird stuff
    // that breaks angular databinding to the select.
    document.getElementById("countriesSelect").onchange = function(event) {
        country = event.target.value;
        $scope.country = country;
    };
})
.controller('AddressController', ['$scope', 'formattingService', function($scope, formattingService) {
    $scope.formatting = formattingService;
}])
.controller('SendPostcardController', ['$scope', 'formattingService', function($scope, formattingService) {
    $scope.formatting = formattingService;
}]);
