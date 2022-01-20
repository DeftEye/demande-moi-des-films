# Handle action around a specific user: manage its movies, its questions, etc.


class User:

    def __init__(self, sender_id):
        self.id = sender_id
        # Variables used to follow at what step is the user
        self.latest_movie_asked = None
        self.questions_before_recommendation = 5
        # Variables used for the first algorithm
        self.good_ratings = []
        self.bad_ratings = []
        self.neutral_ratings = []
        # Variables used for the second algorithm
        self.ratings = dict()
        self.clusters = [[],[],[],[],[],[],[],[],[],[]]

    def has_been_asked_a_question(self):
        return self.latest_movie_asked is not None

    def answer_yes(self):
        self.good_ratings.append(self.latest_movie_asked)
        self.questions_before_recommendation -= 1

    def answer_no(self):
        self.bad_ratings.append(self.latest_movie_asked)
        self.questions_before_recommendation -= 1

    def answer_neutral(self):
        self.neutral_ratings.append(self.latest_movie_asked)

    def should_make_recommendation(self):
        return self.questions_before_recommendation is 0

    def set_pending_question(self, movie):
        self.latest_movie_asked = movie

    def reset_remaining_questions_number(self):
        self.questions_before_recommendation = 5
        self.latest_movie_asked = None

    def process_message(self, message):
        # If nothing is asked to the user, do nothing
        if self.latest_movie_asked is None:
            return

        # Clean space excess and set to lowercase
        clean_message = message.lower().strip()
        if clean_message in ["1","2","3","4","5"]:
            self.ratings[self.latest_movie_asked] = int(clean_message)
            self.questions_before_recommendation -= 1


