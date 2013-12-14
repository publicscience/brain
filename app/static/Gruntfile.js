module.exports = function(grunt) {

    grunt.initConfig({

        /*== Development ================================================*/

        // Server
        connect: {
            server: {
                options: {
                    port: 8989
                }
            }
        },

        // Watch
        watch: {
            // Setup a LiveReload server.
            options: { livereload: true },
            files: [
                'js/vendor/libs/**/*',
                'js/**/*.js',
                'css/**/*.scss',
                'css/**/*.sass',
                '**/*.jade',
                'src/icons/*',
                'assets/**/*',

                // Ignore:
                '!css/exts/_icons.scss'
            ],
            tasks: ['sass', 'jade', 'fontcustom']
        },

        // Compile SASS/SCSS
        // Since all other stylesheets are @import-ed in index.scss,
        // that's the only one we need to compile.
        sass: {
            app: {
                files: {
                    'css/index.css': 'css/index.sass' 
                }
            }
        },

        // Compile Jade templates.
        jade: {
            compile: {
                options: {
                    pretty: true,
                    client: false
                },
                files: [{
                    expand: true,
                    cwd: '.',
                    src: [
                        '**/*.jade',
                        '!inc/**/*.jade',
                        '!node_modules/**/*.jade'
                    ],
                    dest: '.',
                    ext: '.html'
                }]
            }
        },

        bower: {
            main: {
                rjsConfig: 'js/config.js'
            }
        },

        // JS linting with JSHint.
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            files: [
                'js/**/*.js',
                '!js/vendor/**/*.js'
            ]
        },

        csslint: {
            main: {
                options: {
                    csslintrc: '.csslintrc'
                },
                src: ['css/index.css']
            }
        },

        shell: {
            // Compile Font Custom font.
            fontcustom: {
                command: 'fontcustom compile src/icons'
            }
        },
        copy: {
            // Copy Font Custom fonts to proper place.
            fontcustom: {
                files: [
                    {src: ['src/icons/fontcustom/*.woff'], dest: 'css/fonts/icons.woff'},
                    {src: ['src/icons/fontcustom/*.eot'],  dest: 'css/fonts/icons.eot'},
                    {src: ['src/icons/fontcustom/*.svg'],  dest: 'css/fonts/icons.svg'},
                    {src: ['src/icons/fontcustom/*.ttf'],  dest: 'css/fonts/icons.ttf'}
                ]
            },

            // Copy over files for release.
            release: {
                files: [
                    {
                        src: [
                            '.htaccess',
                            'favicon.ico',
                            '404.html',
                            'crossdomain.xml',
                            'humans.txt',
                            'robots.txt'
                        ],
                        dest: 'release/'
                    }
                ]
            }
        },
        replace: {
            // Replace Font Custom CSS.
            fontcustom: {
                src: ['src/icons/fontcustom/fontcustom.css'],
                dest: ['css/exts/_icons.scss'],
                replacements: [{
                    from: /fontcustom_[^.]+/g,
                    to: 'fonts/icons'
                }, {
                    from: 'fontcustom',
                    to: 'icons'
                }]
            },

            // Replace for release.
            release: {
                src: ['index.html'],
                dest: ['release/index.html'],
                replacements: [{
                    from: '/js/vendor/bower/requirejs/require.js',
                    to: 'js/main.js'
                }, {
                    from: ' data-main="/js/main"',
                    to: ''
                }]
            }
        },


        /*== Release ================================================*/

        // Clean out the release directory
        // to remove old files.
        clean: {
            release: ['release/'],
            cleanup: ['release/js/vendor']
        },

        // Optimize RequireJS scripts.
        requirejs: {
            compile: {
                options: {
                    almond: true,                       // Use Almond instead of RequireJS.
                    appDir: 'js',
                    mainConfigFile: 'js/config.js',
                    dir: 'release/js',
                    baseUrl: '../js',
                    modules: [
                        {
                            // Module names are relative to baseUrl.
                            name: 'config',
                            include: ['jquery',
                                      'modernizr'
                            ]
                        },
                        {
                            name: 'main',
                            exclude: ['config']
                        }
                    ]
                }
            }
        },

        // Minify CSS.
        cssmin: {
            options: {
                report: 'gzip'
            },
            files: {
                expand: true,
                cwd: '.',
                src: ['css/index.css'],
                dest: 'release/'
            }
        },

        // Compress PNG and JPG images.
         imagemin: {
             main: {
                 options: {
                     optimizationLevel: 3,              // Optimization level (png).
                     progressive: true                  // Loseless conversion to progressive (jpg).
                 },
                 files: [{
                     expand: true,
                     cwd: 'assets/images',
                     src: '{,*/}*.{png,jpg,jpeg}',
                     dest: 'release/assets/images'
                 }]
             }
         }

    });

    // Define grunt tasks
    // =======================================
    grunt.registerTask('default', ['sass', 'jade', 'connect', 'watch']);
    grunt.registerTask('fontcustom', ['shell:fontcustom', 'copy:fontcustom', 'replace:fontcustom']);
    grunt.registerTask('release', ['jshint', 'csslint', 'clean:release', 'replace:release', 'copy:release', 'cssmin', 'imagemin', 'requirejs', 'clean:cleanup']);

    // Load grunt packages
    // =======================================
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-jade');
    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-csslint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-bower-requirejs');
    grunt.loadNpmTasks('grunt-requirejs');
    grunt.loadNpmTasks('grunt-text-replace');
    grunt.loadNpmTasks('grunt-shell');

};
