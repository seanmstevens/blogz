var gulp = require('gulp');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('styles', function() {
    gulp.src('assets/**/*.css')
        .pipe(autoprefixer({
            browsers: ['last 15 versions']
        }))
        .pipe(gulp.dest('static'));
})

gulp.task('watch', function() {
    gulp.watch('assets/**/*.css', ['styles']);
})
