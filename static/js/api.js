/** Save the result of a game. */
export async function saveScore(name, score) {
  const response = await fetch("/api/score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, score }),
  });
  return response.json();
}

/** Get the top 10 results. */
export async function getLeaderboard() {
  const response = await fetch("/api/leaderboard");
  const data = await response.json();
  return data.leaderboard;
}