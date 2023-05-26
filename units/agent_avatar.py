from units.audio_to_phonemes import PhonemeRow


class AgentAvatar:
    """The avatar of the agent, which will animate based on the phonemes it's saying."""

    def __init__(self) -> None:
        pass

    def animate(self, stream_of_phonemes: list[PhonemeRow]) -> None:
        # print("Animating avatar")
        pass


# https://www.turbosquid.com/3d-models/3d-model-joy-realistic-character---1597570
# Would love to use that, except it's $44

# https://www.turbosquid.com/3d-models/female-rigged-3d-model-1686129
# This would also be cool, but it's $35

# https://www.turbosquid.com/3d-models/young-woman-3d-model-1206633
# This one is $20

# https://www.turbosquid.com/3d-models/nurse-medical-max/978859
# This one is $35, but she's a nurse, which might make her more trustworthy?

# https://www.turbosquid.com/3d-models/3d-model-realistic-young-woman-rigged-biped/1085917
# Free, and kinda alright

# https://studio.blender.org/characters/5d41b19f28b38e1763906a9a/v2/
# Probably the one we'll use, even though he looks kinda odd.

# https://studio.blender.org/characters/einar/v1/
# This guy is kind of fun, but not realistic.

# https://www.turbosquid.com/3d-models/realistic-and-cartoon-woman-3d-model-1886656
# Super good, super expensive

# Using this:
# https://github.com/joeVenner/control-3d-character-using-python
# https://www.youtube.com/watch?v=Z1qyvQsjK5Y
