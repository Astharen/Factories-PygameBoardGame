from abstract_classes.presenter import Presenter
from data.constants import button_text_all_lang


class MainMenuPresenter(Presenter):

    def __init__(self, model, app):
        super().__init__(model)
        self.window_name = 'main_menu'
        self.app = app

    def set_view(self, view):
        super().set_view(view)
        view.start()

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

    def change_to_game(self, is_ia):
        self.app.set_window('game', is_ia=is_ia, language=self.get_language())
