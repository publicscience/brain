require(['config'], function() {
    'use strict';

    require([
            'jquery',
            'modernizr'
    ], function($, ø) {
        // Do stuff.
        console.log('main.js has loaded.');
        console.log('running jQuery version ' + $().jquery + '.');
        console.log('running Modernizr version ' + ø._version + '.');
    });

});
