from abstract_classes.presenter import Presenter


class GamePresenter(Presenter):

    def get_tile_mapping(self):
        return self.model.board.tile_mapping
