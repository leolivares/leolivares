SELECT title FROM movies WHERE strftime('%Y',release_date) = '1996' and strftime('%m',release_date) = '02';
SELECT occupations.name , count(users.occupation_id) as Count FROM users , occupations WHERE users.occupation_id = occupations.id Group By occupations.id Order by Count Desc Limit 5;
SELECT genres.name , AVG(ratings.rating) FROM ratings , genres , genres_movies WHERE ratings.movie_id = genres_movies.movie_id and genres_movies.genre_id = genres.id Group By genres.id;
SELECT movies.title FROM movies , ratings , users WHERE movies.id = ratings.movie_id and ratings.user_id = users.id and users.age < 35 Group By movies.id Order By Count(ratings.rating) DESC Limit 10;
SELECT AVG(users.age) FROM (SELECT ratings.rating , ratings.user_id FROM ratings Group By ratings.user_id HAVING AVG(ratings.rating) > 2.5) as ratings , users WHERE users.id = ratings.user_id and users.gender = "F" Group By users.gender;
