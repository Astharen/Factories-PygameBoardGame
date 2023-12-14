from abstract_classes.presenter import Presenter
from data.constants import button_text_all_lang


class MainMenuPresenter(Presenter):

    def set_next_language(self):
        languages = list(button_text_all_lang.keys())
        index = languages.index(self.get_language())
        new_index = index + 1
        if new_index > (len(languages) - 1):
            new_index = 0
        language = languages[new_index]
        self.model.language = language
        self.view.change_button_text(language)

    def get_language(self):
        return self.model.language

    def change_to_game(self, vs_ai):
        self.app.set_window('game', vs_ai=vs_ai, language=self.get_language())
