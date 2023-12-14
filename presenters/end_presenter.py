from abstract_classes.presenter import Presenter


class EndPresenter(Presenter):

    def get_vs_ai(self):
        return self.model.vs_ai

    def get_language(self):
        return self.model.language

    def get_ending_text(self):
        return self.model.choose_ending_text()

    def change_to_game(self, vs_ai):
        self.app.set_window('game', vs_ai=vs_ai, language=self.get_language())
