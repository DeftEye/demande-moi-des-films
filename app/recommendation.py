# coding: utf-8

# All the recommandation logic and algorithms goes here
from random import choice
import collections
from app.User import User
from sklearn.cluster import KMeans
import numpy as np


class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings

        genres = []
        for movie_id in self.movies:
            movie = self.movies[movie_id]
            genres.append([movie.adventure, movie.action, movie.animation, movie.children, movie.comedy, movie.crime, movie.documentary, movie.drama, movie.fantasy, movie.film_noir, movie.horror, movie.musical, movie.mystery, movie.romance, movie.sci_fi,movie.thriller, movie.war, movie.western, movie.unknown]) 
        movies_genres = np.array(genres, dtype=object) 

        self.kmeans = KMeans(n_clusters = 10).fit(movies_genres)
        self.movie_cluster = {}
        i = 0

        for movie_id in self.movies:
            self.movie_cluster[movie_id] = self.kmeans.labels_[i]
            i += 1 

        self.user_cluster_matrix = []
        self.process_ratings_to_users()

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            user.clusters[self.movie_cluster[rating.movie]].append(rating.score)

        for randomUser in self.test_users:
            thisUser = self.test_users[randomUser]
            for i in range(10): 
                if len(thisUser.clusters[i]) > 0:
                    thisUser.clusters[i] = sum(thisUser.clusters[i])/len(thisUser.clusters[i])
                else :
                    thisUser.clusters[i] = 2.5
            mean = sum(thisUser.clusters)/10
            var = sum((l-mean)**2 for l in thisUser.clusters) / len(thisUser.clusters)
            for i in range(10):
                thisUser.clusters[i] = (thisUser.clusters[i] - mean)/var
            self.user_cluster_matrix.append([thisUser, thisUser.clusters])
        
                
            
            

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        sortedUsers = sorted(self.compute_all_similarities(user), key=lambda l: l[1], reverse = True)
        closests_users = []
        for i in range(5):
            closests_users.append(self.test_users[sortedUsers[i][0]])
        print(closests_users)
        recommended_movies = self.get_best_movies_from_users(closests_users)
        recommendation_text = ""
        for movie in recommended_movies:
                recommendation_text += "," + movie.title

        return "Vos recommandations : " + recommendation_text


    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        similarity = 0
        nb_films_rated_by_both = 0

        if hasattr(user_a, 'good_ratings'):
            for likedMovie in user_a.good_ratings:
                if hasattr(user_b, 'good_ratings') and likedMovie in user_b.good_ratings:
                    similarity += 1 
                    nb_films_rated_by_both += 1 
                elif hasattr(user_b, 'bad_ratings') and likedMovie in user_b.bad_ratings:
                    similarity -= 1
                    nb_films_rated_by_both += 1
        if hasattr(user_a, 'bad_ratings'):
            for dislikedMovie in user_a.bad_ratings:
                if hasattr(user_b, 'good_ratings') and dislikedMovie in user_b.good_ratings:
                    similarity -= 1 
                    nb_films_rated_by_both += 1 
                elif hasattr(user_b, 'bad_ratings') and dislikedMovie in user_b.bad_ratings:
                    similarity += 1
                    nb_films_rated_by_both += 1    
        if nb_films_rated_by_both == 0:
            return 0
        else :
            return similarity/nb_films_rated_by_both

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        self.process_ratings_to_users()
        all_similarities = []
        for randomUser in self.test_users.keys():
            all_similarities.append([randomUser, self.get_similarity(user, self.test_users[randomUser])])
        return all_similarities

    @staticmethod
    def get_best_movies_from_users(users):
        movieList = []
        for randomUser in users:
            if hasattr(randomUser, 'good_ratings'):
                for movie in randomUser.good_ratings:
                    movieList.append(movie)
        print("------------------------------------------------------------")
        movies = [item for item, count in collections.Counter(movieList).items() if count > 1]
        return movies

    @staticmethod
    def get_user_appreciated_movies(user):

        return []

    @staticmethod
    def get_user_norm(user):

        return 1

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []

