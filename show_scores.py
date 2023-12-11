def display_scores(self):
    """Display the scores using letters (H, O, R, S, E)."""
    scores = {
        0: '', 1: 'H', 2: 'HO', 3: 'HOR', 4: 'HORS', 5: 'HORSE'
    }

    p1_score = scores[self.p1.score]
    p2_score = scores[self.p2.score]

    print(f"{self.p1.name}: {p1_score}")
    print(f"{self.p2.name}: {p2_score}")
