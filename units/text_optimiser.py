WORD_MAPPING = {
    "and": "&",
    # "for": "4",
    # "to": "2",
    # "too": "2",
    "you": "u",
    "are": "r",
    "your": "ur",
    "be": "b",
    "see": "c",
    "oh": "o",
    "why": "y",
    "wrap": "rap",
    "bread": "bred",
    "know": "no",
    "lead": "led",
    "read": "red",
    "scent": "sent",
    "would": "wood",
    "some": "sum",
    "missed": "mist",
    "none": "nun",
    "you're": "ur",
    "queue": "cue",
    "heard": "herd",
    "aren't": "aunt",
    "weight": "wait",
    "high": "hi",
    "sight": "site",
    "knows": "nose",
    "whole": "hole",
    "buy": "by",
    "add": "ad",
    "choose": "chews",
    "chord": "cord",
    "eye": "I",
    "phase": "faze",
    "fined": "find",
    "forth": "4th",
    "knead": "need",
    "leased": "least",
    "bee": "b",
    "where": "wear",
    ### These were generated from: https://7esl.com/homonyms/
    "allowed": "aloud",
    "aural": "oral",
    "baize": "bays",
    "berry": "bury",
    "billed": "build",
    "census": "sense",
    "choral": "coral",
    "done": "dun",
    "earn": "urn",
    "farther": "father",
    "foreword": "forward",
    "hour": "our",
    "knew": "new",
    "knight": "night",
    "levee": "levy",
    "links": "lynx",
    "might": "mite",
    "oar": "or",
    "passed": "past",
    "rouse": "rows",
    "sauce": "seen",
}


class TextOptimiser:
    """
    This class will take an input string and optimises it for lower character count, giving us\n
    more space with ElevenLabs, which gives 10k chars per account per month.\n
    By using this, we can increase the amount of free words we get, normally about 3-5% effective
    """

    def __init__(self, text: str, print_improvement: bool = False, disabled: bool = False) -> None:
        self.text = text
        self.print_improvement = print_improvement
        if disabled:
            self.optimised_text = text
            return
        self.optimise_text()

    def optimise_text(self) -> str:
        self.optimised_text = self.text
        for longer, shorter in WORD_MAPPING.items():
            for i in range(2):
                if i == 1:
                    longer = longer.capitalize()
                    shorter = shorter.capitalize()
                if self.optimised_text.startswith(longer + " "):
                    self.optimised_text = self.optimised_text.replace(longer + " ", shorter + " ")
                self.optimised_text = self.optimised_text.replace(" " + longer + " ", " " + shorter + " ")
        if self.print_improvement:
            amount_saved = len(self.text) - len(self.optimised_text)
            print(f"Improvement:\nOriginal had {len(self.text)} chars, optimised has {len(self.optimised_text)} chars")
            print(f"That's a {round(100-(len(self.optimised_text)/len(self.text))*100, 2)}% improvement, of {amount_saved} chars")
        return self.optimised_text.strip()


if __name__ == "__main__":
    optimised = TextOptimiser("Why are you for democracy and can you see why it's bad?", True).optimised_text
    print(f"Optimised text: {optimised}")
    optimised = TextOptimiser(" ".join(WORD_MAPPING.keys()), True).optimised_text
    print(f"Optimised text: {optimised}")
    with open("assets/files/bee_movie_script.txt", "r", encoding="utf-8") as f:
        bee_movie = f.read()
    bee_movie_optimised = TextOptimiser(bee_movie, True).optimised_text
    # print(f"Optimised text: {bee_movie_optimised}")
