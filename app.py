import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Game State
game_state = {'target': random.randint(1, 100), 'attempts': 0, 'max_attempts': 10}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guess Number Game</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #1e1e1e; color: #ffffff; margin: 0; }
        .card { background: #2d2d2d; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center; width: 320px; }
        input[type="number"] { width: 80%; padding: 10px; margin: 10px 0; font-size: 16px; border-radius: 6px; border: 1px solid #444; background: #1e1e1e; color: #fff; text-align: center; }
        button { padding: 10px 20px; font-size: 14px; border: none; border-radius: 6px; background-color: #007acc; color: white; cursor: pointer; margin-top: 5px; }
        button:hover { background-color: #005999; }
        button:disabled { background-color: #555; cursor: not-allowed; }
        .feedback { font-weight: bold; margin-top: 15px; height: 24px; }
        .attempts { font-size: 12px; color: #aaa; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Guess Number Game</h2>
        <p>I'm thinking of a number between 1 and 100.</p>
        <input type="number" id="guessInput" placeholder="Enter number" min="1" max="100">
        <br>
        <button id="submitBtn" onclick="makeGuess()">Submit Guess</button>
        <div class="feedback" id="feedback">Take your first guess!</div>
        <div class="attempts" id="attempts">Attempts: 0/10</div>
        <br>
        <button id="resetBtn" onclick="resetGame()" style="display:none; background-color: #28a745;">New Game</button>
    </div>

    <script>
        async function makeGuess() {
            const input = document.getElementById('guessInput');
            const val = input.value;
            if (!val) return;

            const res = await fetch('/guess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ guess: parseInt(val) })
            });
            const data = await res.json();

            const feedback = document.getElementById('feedback');
            feedback.innerText = data.message;
            feedback.style.color = data.status === 'win' ? '#4caf50' : data.status === 'lose' ? '#f44336' : '#ff9800';
            document.getElementById('attempts').innerText = `Attempts: ${data.attempts}/${data.max_attempts}`;

            if (data.status === 'win' || data.status === 'lose') {
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('guessInput').disabled = true;
                document.getElementById('resetBtn').style.display = 'inline-block';
            }
            input.value = '';
        }

        async function resetGame() {
            await fetch('/reset', { method: 'POST' });
            document.getElementById('submitBtn').disabled = false;
            document.getElementById('guessInput').disabled = false;
            document.getElementById('resetBtn').style.display = 'none';
            document.getElementById('feedback').innerText = 'Take your first guess!';
            document.getElementById('feedback').style.color = '#ffffff';
            document.getElementById('attempts').innerText = 'Attempts: 0/10';
        }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)


@app.route('/guess', methods=['POST'])
def guess():
  data = request.get_json()
  user_guess = data.get('guess')
  game_state['attempts'] += 1

  if user_guess < game_state['target']:
    status = 'low'
    msg = 'Too Low! Try higher.'
  elif user_guess > game_state['target']:
    status = 'high'
    msg = 'Too High! Try lower.'
  else:
    status = 'win'
    msg = f"Correct! You won in {game_state['attempts']} attempts!"

  if (
      status != 'win'
      and game_state['attempts'] >= game_state['max_attempts']
  ):
    status = 'lose'
    msg = f"Game Over! The target number was {game_state['target']}."

  return jsonify({
      'status': status,
      'message': msg,
      'attempts': game_state['attempts'],
      'max_attempts': game_state['max_attempts'],
  })


@app.route('/reset', methods=['POST'])
def reset():
  game_state['target'] = random.randint(1, 100)
  game_state['attempts'] = 0
  return jsonify({'status': 'ok'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)