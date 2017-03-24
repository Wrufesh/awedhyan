var gulp = require('gulp');
var path = require('path');
var sass = require('gulp-sass');
// var coffee = require('gulp-coffee');
var sourcemaps = require('gulp-sourcemaps');

// var babel = require("gulp-babel");
// var concat = require("gulp-concat");


gulp.task('styles', function () {
    gulp.src('app/src/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('app/static/public/'));
});


// gulp.task('coffee', function () {
//     gulp.src('src/**/*.coffee')
//         .pipe(coffee({bare: true}))
//         .pipe(gulp.dest('static/public'));
// });
//
//
// gulp.src('src/**/*.coffee')
//     .pipe(sourcemaps.init())
//     .pipe(coffee({bare: true}))
//     .pipe(sourcemaps.write('./maps'))
//     .pipe(gulp.dest('static/public'));

// gulp.task("babel", function () {
//     return gulp.src("src/**/*.jsx", { base: 'src'})
//         .pipe(sourcemaps.init())
//         .pipe(babel())
//         // .pipe(concat(sourceFileName + ".js"))
//         .pipe(sourcemaps.write("./maps"))
//         .pipe(gulp.dest('static/public'));
// });

//Watch task
gulp.task('default', function () {
    gulp.watch('app/src/sass/**/*.scss', ['styles']);
    // gulp.watch('src/coffee/**/*.coffee', ['coffee']);
    // gulp.watch("src/**/*.js",['babel']);
});