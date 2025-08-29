from django.shortcuts import render
import random

# Constants for the game.
WORD_LENGTH = 5
MAX_ATTEMPTS = 6

def start_action(request):
    """
    Handles GET and POST for the start page.
    GET: Returns the start page with a welcome message.
    POST: Validates the target word and initializes the game.
    """
    if request.method == "GET":
        context = {"message": "Welcome to Wordish!"}
        return render(request, "wordish/start.html", context)
    
    try:
        target = _process_word_parameter(request.POST, "target")
        context = _compute_game_context(target, guesses=[])
        return render(request, "wordish/game.html", context)

    except ValueError as e:
        context = {"message": f"Error invalid: {str(e)}"}
        return render(request, "wordish/start.html", context)
    except Exception as e:
        context = {"message": f"Error invalid: Unexpected error: {str(e)}"}
        return render(request, "wordish/start.html", context)


def game_action(request):
    """
    Processes guess submissions and updates the game state.
    Validates that required hidden fields have not been tampered with.
    """
    if request.method == "GET":
        return render(
            request,
            "wordish/start.html",
            {"message": "Error invalid: You're hacking. Try again!"}
        )
    
    required_fields = ["old-guesses", "target", "new-guess"]
    for f in required_fields:
        if f not in request.POST:
            return render(
                request,
                "wordish/start.html",
                {"message": "Error invalid: Malformed hidden field detected."}
            )

    target = request.POST.get("target", "").strip().upper()
    new_guess = request.POST.get("new-guess", "").strip().upper()
    message_field = request.POST.get("message", "") 
    old_guesses_raw = request.POST.get("old-guesses", "")

    if not target:
        return render(
            request,
            "wordish/start.html",
            {"message": "Error invalid: Target word is missing."}
        )
    if not new_guess:
        return render(
            request,
            "wordish/start.html",
            {"message": "Error invalid: No guess submitted."}
        )

    try:
        target = _process_word_parameter(request.POST, "target")
        old_guesses = _process_old_guesses(request.POST)

        for guess in old_guesses:
            if len(guess) != WORD_LENGTH or not guess.isalpha():
                return render(
                    request,
                    "wordish/start.html",
                    {"message": "Error invalid: Invalid game state due to tampered hidden fields."}
                )
        
        if not (target.isalpha() and len(target) == WORD_LENGTH):
            return render(
                request,
                "wordish/start.html",
                {"message": "Error invalid: Corrupted target word."}
            )

        if message_field.strip() not in ["", "Error: Missing required form fields."]:
            return render(
                request,
                "wordish/start.html",
                {"message": "Error invalid: Malformed hidden field detected."}
            )

    except ValueError as e:
        return render(
            request,
            "wordish/start.html",
            {"message": f"Error invalid: Invalid input: {e}"}
        )
    
    except Exception:
        return render(
            request,
            "wordish/start.html",
            {"message": "Error invalid: Unexpected issue. Try again!"}
        )

    try:
        new_guess = _process_word_parameter(request.POST, "new-guess")
        context = _compute_game_context(target, old_guesses + [new_guess])
    except ValueError as e:
        context = _compute_game_context(target, old_guesses)
        context["message"] = f"Error invalid: Invalid input: {e}"
    except Exception:
        return render(
            request,
            "wordish/start.html",
            {"message": "Error invalid: Unexpected issue. Try again!"}
        )
    
    return render(request, "wordish/game.html", context)


def _process_word_parameter(post_data, key):
    """
    Validates that the word parameter is exactly 5 uppercase letters.
    Raises ValueError if validation fails.
    """
    word = post_data.get(key, "").strip().upper()
    if len(word) != WORD_LENGTH:
        raise ValueError("Invalid input. Word must be exactly 5 letters.")
    if not all('A' <= char <= 'Z' for char in word):
        raise ValueError(f"Invalid input. Invalid character in {key}. Only A-Z allowed.")
    return word


def _process_old_guesses(post_data):
    """
    Extracts previous guesses from the hidden field and returns a list of non-empty guesses.
    """
    guesses = post_data.get("old-guesses", "").split(",")
    return [g for g in guesses if g]


def _compute_game_context(target, guesses):
    """
    Computes the game board matrix and message based on the target word and previous guesses.
    Returns a context dictionary for rendering the game page.
    """
    matrix = []
    for row in range(MAX_ATTEMPTS):
        row_data = []
        if row < len(guesses):
            guess = guesses[row]
            colors = _determine_colors(guess, target)
            for col in range(WORD_LENGTH):
                row_data.append({
                    "id": f"cell_{row}_{col}",
                    "letter": guess[col],
                    "color": colors[col]
                })
        else:
            for col in range(WORD_LENGTH):
                row_data.append({
                    "id": f"cell_{row}_{col}",
                    "letter": "",
                    "color": "blank"
                })
        matrix.append(row_data)

    # Determine the message to display on the game page.
    if not guesses:
        game_message = "Input a guess to start the game!"
    elif guesses and guesses[-1] == target:
        game_message = "🎉 Congratulations! You win!"
    elif len(guesses) >= MAX_ATTEMPTS:
        game_message = f"Game Over! You lose! The target word was {target}."
    else:
        game_message = "Keep guessing!"

    return {
        "message": game_message,  # using 'message' instead of 'status'
        "matrix": matrix,
        "target": target,
        "old_guesses": ",".join(guesses),
    }


def _determine_colors(guess, target):
    """
    Determines the color coding for each letter:
    - "correct": letter is in the correct position.
    - "misplaced": letter is in the word but in the wrong position.
    - "wrong": letter is not in the target.
    """
    colors = ["wrong"] * WORD_LENGTH
    target_counts = {}
    for letter in target:
        target_counts[letter] = target_counts.get(letter, 0) + 1

    # First pass: find correct letters
    for i in range(WORD_LENGTH):
        if guess[i] == target[i]:
            colors[i] = "correct"
            target_counts[guess[i]] -= 1

    # Second pass: find misplaced letters
    for i in range(WORD_LENGTH):
        if colors[i] == "wrong" and guess[i] in target_counts and target_counts[guess[i]] > 0:
            colors[i] = "misplaced"
            target_counts[guess[i]] -= 1

    return colors