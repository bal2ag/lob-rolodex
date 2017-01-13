angular.module('LobRolodex.controllers', ['angularUtils.directives.dirPagination'])
.controller('HomeController', function($scope, $http) {
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

    $scope.formatName = function(address) {
        if (address.name) {
            return address.name;
        }
        return address.company;
    };

    $scope.formatAddress = function(address) {
        if (address.address_line2) {
            return address.address_line1 + ' ' + address.address_line2;
        }
        return address.address_line1;
    };

    $scope.formatLocation = function(address) {
        if (address.address_country == 'United States') {
            return address.address_city + ', ' + address.address_state;
        };
        return address.address_country;
    };

    $scope.redirectToSendCardView = function(address) {
        console.log(address);
        window.location = 'address/' + address.id + '/send';
    };

    $scope.getRemoveAddressUrl = function(address) {
        return 'address/' + address.id + '/remove';
    };
})
.controller('NewAddressController', function($scope) {
    $scope.country = 'US';

    // Need this hack because the bootstrap form helpers do some weird stuff
    // that breaks angular databinding to the select.
    document.getElementById("countriesSelect").onchange = function(event) {
        country = event.target.value;
        $scope.country = country;
    };
});
