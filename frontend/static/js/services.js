angular.module('LobRolodex.services', [])
.factory('formattingService', function() {
    service = {};

    service.formatName = function(address) {
        if (address.name) {
            return address.name;
        }
        return address.company;
    };
    
    service.formatAddress = function(address) {
        if (address.address_line2) {
            return address.address_line1 + ' ' + address.address_line2;
        }
        return address.address_line1;
    };

    service.formatMailingAddress = function(address) {
        var value = address.address_line1;
        if (address.address_line2) {
            value += '\n' + address.address_line2;
        }
        if (address.address_country == 'United States') {
            value += '\n' + address.address_city + ', ' + address.address_state + ' ' + address.address_zip;
        } else {
            if (address.address_city) {
                value += '\n' + address.address_city + ', ' + address.address_country;
            } else {
                value += '\n' + address.address_country;
            }
        }
        return value;
    };
    
    service.formatLocation = function(address) {
        if (address.address_country == 'United States') {
            return address.address_city + ', ' + address.address_state;
        };
        return address.address_country;
    };
    
    service.redirectToSendCardView = function(address) {
        window.location = 'address/' + address.id + '/send';
    };
    
    service.getRemoveAddressUrl = function(address) {
        return 'address/' + address.id + '/remove';
    };

    return service;
});
