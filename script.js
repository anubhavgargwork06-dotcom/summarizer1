const button = document.getElementById("summarizeBtn");
const statusEl = document.getElementById("status");
const summaryBox = document.getElementById("summaryBox");

button.addEventListener("click", async () => {
    const text = document.getElementById("inputText").value.trim();
    const numSentences = document.getElementById("numSentences").value;

    if (!text) {
        alert("Please paste some text.");
        return;
    }

    button.disabled = true;
    statusEl.textContent = "Summarizing...";
    summaryBox.textContent = "";

    try {
        const response = await fetch("/summarize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                num_sentences: numSentences
            })
        });

        const data = await response.json();

        if (data.error) throw new Error(data.error);

        summaryBox.textContent = data.summary;
        statusEl.textContent = "Done!";
    } catch (err) {
        statusEl.textContent = "Error: " + err.message;
    } finally {
        button.disabled = false;
    }
});
