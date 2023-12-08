class EndModel:
    def __init__(self):
        self.language = None
        self.winner = None
        self.vs_ai = None

    def start(self, language, winner, vs_ai):
        self.language = language
        self.winner = winner
        self.vs_ai = vs_ai

    def choose_ending_text(self):
        if self.winner is None:
            if self.language == 'Spanish':
                text = 'Todos han perdido.'
            elif self.language == 'English':
                text = 'Everybody have lost.'
        else:
            if self.language == 'Spanish':
                name = self.winner.name.replace('player', '')
                text = f'El jugador {name} gana!'
            elif self.language == 'English':
                name = self.winner.name.replace('player', '')
                text = f'Player {name} won!'
        return text
