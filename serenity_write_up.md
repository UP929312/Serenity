# Serenity: A virtual AI therapist

End goals:

- As immersive as possible (excluding uncanny voices or faces)
- The ability to respond relatively quickly to avoid long awkward pauses (less than 5 seconds).

Units:

- Speech to Text (user)
- Text to Speech (bot)
- Digital face animation with expressions
- Facial reading, to gather additiona user emotion data
- Natural pauses and mannerisms (to avoid it sounding too robotic)
- The ability to remember everything the user has done so far, to build a report (store in fast vector database)
- Refer back to previous sessions, to track/measure progress (temporal awareness)

Sub tasks:

- Build it's own list of goals for the user, which they can slowly check off when progressing
- The AI should permanently remember previous conversations, and refer back to them when needed.
- All learned facts about the user should also be included in the report, and used to help the user.

Tensor storage:

We need to store the data the the user inputs while chatting with a bot. This data will be used to train the bot, and also to build a report for the user.
The messages wil be stored in one hot encoding, [explanation](https://machinelearningmastery.com/why-one-hot-encode-data-in-machine-learning/),
[Medium article](https://medium.com/vector-database)
