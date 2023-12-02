class Presenter:
    def __init__(self, model, app):
        self.model = model
        self.view = None
        self.app = app

    def start(self, view):
        self.set_view(view)

    def set_view(self, view):
        self.view = view
        self.view.set_presenter(self)
