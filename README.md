# Wordish Game 🎮

Wordish is a **Wordle-like web-based game** built as part of a three-part homework series.  
This final version (HW3) transitions the game from a purely front-end implementation into a **full Django web application**, with server-side game logic and client-server interactions.

---

## 🚀 Gameplay
- A target word (five letters) is chosen on the **Start Page**.
- Players make guesses on the **Game Page**.
- After each guess:
  - Letters in the correct position are highlighted green.
  - Correct letters in the wrong position are highlighted yellow.
  - Incorrect letters are shown in gray:contentReference[oaicite:0]{index=0}.
- The game ends when:
  - The player guesses the word correctly (win 🎉).
  - The player uses all 6 guesses without success (lose ❌).
- Error messages are displayed if the player enters invalid input or an invalid game state:contentReference[oaicite:1]{index=1}.

---

## ✨ Features
- **Start Page**
  - Input field (`#target_text`) and start button (`#start_button`) to set the target word:contentReference[oaicite:2]{index=2}.
  - Displays welcome/error messages inside `#message`.
- **Game Page**
  - Input for guesses and button to submit.
  - Updated board after each guess, showing colored hints.
  - Game status messages displayed in `#status`.
- **Validation**
  - Ensures all guesses are five-letter words:contentReference[oaicite:3]{index=3}.
  - Invalid words or malformed input show error messages without crashing the app.
- **Stateless Server**
  - No database is used.
  - Game state is passed between client and server on each request, ensuring robustness:contentReference[oaicite:4]{index=4}.

---

## 🛠️ Tech Stack
- **Backend:** [Django 5](https://www.djangoproject.com/) (Python-based web framework):contentReference[oaicite:5]{index=5}
- **Frontend:** HTML5, CSS3
- **Game Logic:** Python (server-side validation & guess checking)
- **Client-Side:** Minimal JavaScript (only from HW2 version):contentReference[oaicite:6]{index=6}
- **Version Control:** Git & GitHub


