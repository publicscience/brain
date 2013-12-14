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

        $('[data-method=delete]').on('click', function(e) {
            e.preventDefault();

            var link = $(this),
                url = $(this).attr('href');
            if (confirm('Are you sure you want to delete this mentor?')) {
                $.ajax(url, {
                    type: 'DELETE',
                    success: function() {
                        link.parent().remove();
                    }
                });
            }

            return false;
        });
    });

});
