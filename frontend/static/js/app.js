var app = angular.module('LobRolodex',
        [
        'LobRolodex.homeControllers'
        ]
)
.config(['$interpolateProvider', '$locationProvider', function($interpolateProvider, $locationProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
    $locationProvider.html5Mode(true);
}]);
