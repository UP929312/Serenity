# Serenity: A virtual AI therapist

End goals:

- As immersive as possible (excluding uncanny voices or faces)
- The ability to respond relatively quickly to avoid long awkward pauses (less than 5 seconds).
- Run on windows 10 and 11 machines immediately, with other platforms to follow.

Units:

- Microphone capturing and storing
- Speech to Text (user)
- Text to Speech (bot)
- Keyboard detection for push to talk
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

Later:

- Different options, such as voices and 3d models, so users can choose their own
- Generate an avatar which will react and be human
- Speech detection to remove the need for push to talk
- Face-ID type situation, so no one else can use your account, repo found [here](https://github.com/ageitgey/face_recognition)
- In the future, asynchronously also do further analysis on the user's input, potentially while Serentity is speaking
- > Flagged things [here](https://www.assemblyai.com/docs/Models/content_moderation#understanding-the-response)
- If the user explicitally mentions their emotions, get confidence score and adjust thresholds
- Check if second highest emotion is high, and use that instead of neutral
- Move processing to our hosted hardware, and have light clients
- Have a single .exe file, so no installation is particularly required

Considerations:

- Rogue AI, what happens if it says something wrong, like reassures suicide
- GDPR, shouldn't be an issue because it's all stored locally, but maybe some key word training, for Deepgram?
- Pricing, which is partially rectified by assets/documents/pricing.md, but more work needs doing.
- Team contributions and split
- Legal "You accept the risks, we don't offer medically graded advice"
