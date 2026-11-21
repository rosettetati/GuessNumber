using System;
using System.Drawing;
using System.Windows.Forms;

namespace GuessNumber
{
    public partial class Form1 : Form
    {
        private int secretNumber;
        private int attemptsLeft;
        private const int MaxAttempts = 7;
        private Random random = new Random();

        public Form1()
        {
            InitializeComponent();
            StartNewGame();
        }

        private void StartNewGame()
        {
            secretNumber = random.Next(1, 101);
            attemptsLeft = MaxAttempts;

            lblFeedback.Text = "Make your first guess!";
            lblFeedback.ForeColor = Color.DarkBlue;
            lblAttempts.Text = $"Attempts remaining: {attemptsLeft}";

            txtGuess.Text = "";
            txtGuess.Enabled = true;
            btnGuess.Enabled = true;
            txtGuess.Focus();
        }

        private void BtnGuess_Click(object sender, EventArgs e)
        {
            if (!int.TryParse(txtGuess.Text, out int playerGuess) || playerGuess < 1 || playerGuess > 100)
            {
                lblFeedback.Text = "Invalid input! Enter a number from 1 to 100.";
                lblFeedback.ForeColor = Color.DarkRed;
                txtGuess.Clear();
                txtGuess.Focus();
                return;
            }

            attemptsLeft--;
            lblAttempts.Text = $"Attempts remaining: {attemptsLeft}";

            if (playerGuess == secretNumber)
            {
                lblFeedback.Text = $"Correct! You guessed {secretNumber}!";
                lblFeedback.ForeColor = Color.Green;
                EndGame();
            }
            else if (attemptsLeft <= 0)
            {
                lblFeedback.Text = $"Game Over! The number was {secretNumber}.";
                lblFeedback.ForeColor = Color.Red;
                EndGame();
            }
            else if (playerGuess < secretNumber)
            {
                lblFeedback.Text = $"{playerGuess} is too LOW! Try higher.";
                lblFeedback.ForeColor = Color.DarkOrange;
            }
            else
            {
                lblFeedback.Text = $"{playerGuess} is too HIGH! Try lower.";
                lblFeedback.ForeColor = Color.DarkOrange;
            }

            txtGuess.Clear();
            txtGuess.Focus();
        }

        private void EndGame()
        {
            txtGuess.Enabled = false;
            btnGuess.Enabled = false;
        }

        private void BtnReset_Click(object sender, EventArgs e)
        {
            StartNewGame();
        }
    }
}