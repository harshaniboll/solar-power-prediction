
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");

    if (!form) {
        console.error("Prediction form not found!");
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const status = document.getElementById("prediction-status");
        const result = document.getElementById("prediction-value");
        const note = document.getElementById("prediction-note");

        const payload = {
            ambient_temperature: Number(document.getElementById("ambient").value),
            module_temperature: Number(document.getElementById("module").value),
            irradiation: Number(document.getElementById("irradiation").value),
            hour: Number(document.getElementById("hour").value),
            month: Number(document.getElementById("month").value)
        };

        if (Object.values(payload).some(v => !Number.isFinite(v))) {
            status.textContent = "Please enter valid values in all fields.";
            return;
        }

        status.textContent = "Calculating solar power...";
        result.textContent = "—";
        note.textContent = "";

        try {
            const response = await fetch(
                "http://127.0.0.1:5000/api/predict",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Prediction failed");
            }

            result.textContent = Number(data.prediction).toFixed(2);
            note.textContent = "Predicted AC power output (dataset units)";
            status.textContent = "Prediction successful!";
        } catch (error) {
            console.log("PREDICT CLICKED — submitting form");
            console.error(error);
            status.textContent =
                "Prediction failed. Check that the Python server is running.";
        }
    });
});
